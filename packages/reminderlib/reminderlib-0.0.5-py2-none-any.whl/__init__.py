import logging

from ReminderController.ReminderManagerService import ReminderManagerService
from ReminderNotifier.ReminderNotifier import run_notification_job

__author__ = 'Jayashathiskumar Jayakumar'
__version__ = '0.0.1'
__id__ = '20154810'
reminder_manager = ReminderManagerService()
#event = {'Records': [{'eventID': 'c5a788379c2413cf01c21b9a7796f36a', 'eventName': 'MODIFY', 'eventVersion': '1.1', 'eventSource': 'aws:dynamodb', 'awsRegion': 'us-east-1', 'dynamodb': {'ApproximateCreationDateTime': 1608450710.0, 'Keys': {'id': {'S': 'shathis.jayakumar@gmail.com'}}, 'NewImage': {'likesCount': {'S': '100'}, 'comments': {'L': [{'M': {'commentContent': {'S': 'test comment'}}}, {'M': {'commentContent': {'S': 'test comment2'}}}]}, 'role': {'S': 'Engineer'}, 'id': {'S': 'shathis.jayakumar@gmail.com'}, 'imageKey': {'S': '1234'}, 'name': {'S': 'Jaykumar'}, 'topic': {'S': 'goal'}, 'date': {'S': '22-12-2020'}, 'message': {'S': 'Our goal is to complete the cpp project on 21/12/2020. please be mindful on the release.'}}, 'OldImage': {'likesCount': {'S': '100'}, 'comments': {'L': [{'M': {'commentContent': {'S': 'test comment'}}}, {'M': {'commentContent': {'S': 'test comment2'}}}]}, 'role': {'S': 'Engineer'}, 'id': {'S': 'shathis.jayakumar@gmail.com'}, 'imageKey': {'S': '1234'}, 'name': {'S': 'Jaykumar'}, 'topic': {'S': 'Goal'}, 'time': {'S': '20/12/2020, 01:39:08'}, 'message': {'S': 'test feed content'}}, 'SequenceNumber': '19458800000000024819605292', 'SizeBytes': 530, 'StreamViewType': 'NEW_AND_OLD_IMAGES'}, 'eventSourceARN': 'arn:aws:dynamodb:us-east-1:508575043679:table/NewsFeed/stream/2020-12-20T07:44:14.398'}]}


def save_event_reminder(event, region, table_name):
    """
    This method exposed to the lambda function which passes the event object.
    """
    print("save_event_reminder")
    reminder_manager.split_event_reminder(event, region, table_name)
    return "Success"


if __name__ == '__main__':
 run_notification_job()
