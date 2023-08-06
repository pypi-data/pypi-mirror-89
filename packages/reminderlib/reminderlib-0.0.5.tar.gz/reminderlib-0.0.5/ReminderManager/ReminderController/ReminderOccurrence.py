import logging
import boto3
from botocore.exceptions import ClientError

class ReminderOccurrence:

    def set_reminder_item(self, category, reminderObj):
        occurence = {"Day":"1", "Month":"2", "Year":"12", "FYear":"0"}
        if reminderObj:
            date = reminderObj['date']
            duration = reminderObj['duration']
            obj = reminderObj['obj']
            region = obj['region']
            table = "Reminder"
            id = obj['key']['id']['S']
            message = obj['item']['message']['S']
            occurenceN = occurence[duration]
            reminderItem = {"id":id, "date":date,"occurence":occurenceN,"message":message,"category":category}
            self.store_an_item_reminder(reminderItem, region, table)
            
    def store_an_item_reminder(self, reminderItem, region, table):
        try:
            print(reminderItem, table, region)
            dynamodb_resource = boto3.resource("dynamodb", region_name=region)
            table = dynamodb_resource.Table(table)
            table.put_item(Item=reminderItem)
        
        except ClientError as e:
            logging.error(e)
            return False
        return True