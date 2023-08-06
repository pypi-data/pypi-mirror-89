import logging
import boto3
from botocore.exceptions import ClientError
from ReminderController.ReminderCategorizer import ReminderCategorizer

class ReminderManagerService:
    
    def create_table(self, table_name, key_schema, attribute_definitions, provisioned_throughput, region):
        
        try:
            dynamodb_resource = boto3.resource("dynamodb", region_name=region)
            self.table = dynamodb_resource.create_table(TableName=table_name, KeySchema=key_schema, AttributeDefinitions=attribute_definitions,
                ProvisionedThroughput=provisioned_throughput)

            # Wait until the table exists.
            self.table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            
        except ClientError as e:
            logging.error(e)
            return False
        return True
        
    def update_table(self, table_name, attribute_definitions, provisioned_throughput, stream_specification, region):
        try:
            dynamodb_resource = boto3.resource("dynamodb", region_name=region)
            table = dynamodb_resource.Table(table_name)
            table.update(StreamSpecification=stream_specification)
        
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def get_insert_record(self, insert_record, region, table):
        ReminderCategorizer().get_new_image_insert(insert_record, region, table)
        return "insert_record"

    def get_modify_record(self, modify_record, region, table):
        ReminderCategorizer().get_new_image_modify(modify_record, region, table)
        return "modify_record"

    def get_delete_record(self, delete_record, region, table):
        ReminderCategorizer().get_new_image_delete(delete_record, region, table)
        return "delete_record"

    def split_event_reminder(self, event, region, table):
        try:
            for record in event['Records']:
                if record['eventName'] == 'INSERT':
                    self.get_insert_record(record, region, table)
                elif record['eventName'] == 'MODIFY':
                    self.get_modify_record(record, region, table)
                elif record['eventName'] == 'REMOVE':
                    self.split_event_reminder(record, region, table)
            return "Success!"
        except ClientError as e:
            logging.error(e) 
            return False

