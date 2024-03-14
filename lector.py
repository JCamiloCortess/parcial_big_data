import boto3
from bs4 import BeautifulSoup
import csv
import datetime

s3 = boto3.client('s3')

def process_data(event, context):
    raw_file_key = event['Records'][0]['s3']['object']['key']
    raw_file = s3.get_object(Bucket='eltarrito', Key=raw_file_key)
    raw_html = raw_file['Body'].read()
    
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    extracted_data = []
    for listing in soup.find_all('div', class_='listing'):
        price = listing.find('span', class_='price').text
        area = listing.find('span', class_='area').text
        bedrooms = listing.find('span', class_='bedrooms').text
        # Extract additional features as needed
        
        extracted_data.append([price, area, bedrooms])
    
    # Generate current date for file naming
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    csv_file = f"{current_date}.csv"
    csv_path = f"casas/year={current_date[:4]}/month={current_date[5:7]}/day={current_date[8:]}/{csv_file}"
    
    with s3.put_object(Body='', Bucket='bucket-final', Key=csv_path) as csv_object:
        writer = csv.writer(csv_object)
        writer.writerows(extracted_data)
    
    return {'statusCode': 200, 'body': 'Data processed and saved successfully'}
