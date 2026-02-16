import csv
from faker import Faker
import random
import datetime

fake = Faker('en_IN')

def fake_generate_company_data(record_count=100000): 
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"bulk_company_data_{timestamp}.csv"
    
    company_types = ["software", "it", "manufacturing", "education"]
    
    headers = [
        "company_name", "company_registration_no", "company_type", 
        "company_type_meta", "company_web", "company_logo", 
        "company_email", "company_contact_no", "company_gst_no", 
        "company_pan_no", "company_tin_no", "company_cin_no",
        "meta_founded_year", "meta_employee_count", "meta_headquarters",
        "company_country"
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for i in range(record_count):
            writer.writerow({
                "company_name": f"{fake.company()} {fake.company_suffix()}",
                "company_registration_no": f"REG-{fake.unique.random_number(digits=8, fix_len=True)}",
                "company_type": fake.job(),
                "company_type_meta": random.choice(company_types),
                "company_web": f"https://www.{fake.domain_name()}",
                "company_logo": "https://cdn.example.com/logos/main.png",
                "company_email": fake.company_email(),
                "company_country":fake.country(),      
                "company_contact_no": f"+91-{fake.msisdn()[3:]}",
                "company_gst_no": f"{fake.random_int(10, 35)}AAAAA{fake.random_number(digits=4)}A1Z1",
                "company_pan_no": f"{fake.bothify('?????####?')}".upper(),
                "company_tin_no": f"TIN{fake.random_number(digits=10)}",
                "company_cin_no": f"U{fake.random_number(digits=5)}DL2026PTC{fake.random_number(digits=6)}",
                # Flattened the meta fields to match the headers
                "meta_founded_year": fake.year(),
                "meta_employee_count": fake.random_int(min=10, max=5000),
                "meta_headquarters": fake.city()
                   
            })
            
    return filename
    