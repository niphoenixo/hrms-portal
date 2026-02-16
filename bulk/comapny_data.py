from fastapi import Depends
import pandas as pd

import random
import datetime
from sqlalchemy.orm import Session
from database.db import get_db
from models import Company
from custom_response.json_response import CustomJSONResponse
import datetime
from sqlalchemy.orm import Session
import pandas as pd
from pymysql import err

def generate_company_data(oldfilename, df, db: Session):
    chunk_size = 1000
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    newfilename = f"{oldfilename}_{timestamp}.csv"
    
    db_columns = {
        "company_name", "company_email", "company_registration_no", "company_type", 
        "company_type_meta", "company_web", "company_logo", 
        "company_country", "company_contact_no", "company_gst_no", 
        "company_pan_no", "company_tin_no", "company_cin_no", "company_uuid",
        "created_by", "updated_by"
    }

    diff_columns = [col for col in df.columns if col not in db_columns]
    df['company_meta'] = df[diff_columns].to_dict(orient='records')
    
    columns_to_keep = list(db_columns.intersection(df.columns)) + ['company_meta']
    final_records = df[columns_to_keep].head(1).to_dict(orient="records")

    inserted_uuids = []

    try:
        for i in range(0, len(final_records), chunk_size):
            chunk = final_records[i : i + chunk_size]
            
            db.bulk_insert_mappings(Company, chunk, render_nulls=True)
            db.flush()
            
            inserted_uuids.extend([record.get('company_uuid') for record in chunk if record.get('company_uuid')])

        db.commit()
    except Exception as e:
        db.rollback()
        if hasattr(e, 'args') and len(e.args) > 1:
            error_msg = e.args[1]
        else:
            error_msg = e

        return CustomJSONResponse.from_server_error(error_msg,f"Company Bulk Insert failed Exception")
    
    return {
        "status":True,
        "new_file_name": newfilename,
        "records_count": len(inserted_uuids),
        "diff_headers": diff_columns
    }
    