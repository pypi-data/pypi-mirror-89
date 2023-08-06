import boto3
import logging
from time import sleep
from datetime import datetime
from botocore.exceptions import ClientError

def get_an_item(region, table_name):
    try:
        dynamodb_resource = boto3.resource("dynamodb", region_name=region)
        table = dynamodb_resource.Table(table_name)
        response = table.scan()
        data = response['Items']
            
        while 'name' in response:
            response = table.scan(ExclusiveStartKey=response['name'])
            data.extend(response['Items'])

        return response['Items']
        
    except ClientError as e:
        logging.error(e)
        return False
    return True

def store_an_item(region, table_name, item):
        try:
            dynamodb_resource = boto3.resource("dynamodb", region_name=region)
            table = dynamodb_resource.Table(table_name)
            table.put_item(Item=item)
        
        except ClientError as e:
            logging.error(e)
            return False
        return True        

def trigger_notification():
    region = 'us-east-1'
    table_name = "Reminder"
    item = get_an_item(region, table_name)
    item = [{'category': 'goal', 'occurence': '2', 'date': '20-12-2020', 'message': 'Our goal is to complete the cpp project on 21/12/2020. please be mindful on the release.', 'empId': 'shathis.jayakumar@gmail.com'}]
    currentDate = datetime.today().strftime('%-d-%-m-%Y')
    
    for currentItem in item:
        currentItemDate = currentItem['date']
        if currentDate == currentItemDate:
            store_an_item(region, "Notification", currentItem)
    sleep(10)
    run_notification_job()

def run_notification_job():    
    trigger_notification()