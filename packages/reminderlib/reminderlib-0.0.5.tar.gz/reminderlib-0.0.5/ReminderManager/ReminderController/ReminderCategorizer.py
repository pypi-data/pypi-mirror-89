import logging

from datetime import datetime
from ReminderController.ReminderOccurrence import ReminderOccurrence

class ReminderCategorizer:

	def get_new_image_insert(self, insert_record, region, table):
		if insert_record:
			if insert_record['awsRegion'] == region:
				newItem = insert_record['dynamodb']['NewImage']
				key = insert_record['dynamodb']['Keys']
				obj = {"table":table,"key":key,"item":newItem}
				self.find_date_from_item(obj)
	
	def get_new_image_modify(self, modify_record, region, table):
		if modify_record:
			if modify_record['awsRegion'] == region:
				modifiedItem = modify_record['dynamodb']['NewImage']
				key = modify_record['dynamodb']['Keys']
				obj = {"region":region, "table":table,"key":key,"item":modifiedItem}
				self.find_date_from_item(obj)

	def get_new_image_delete(self, delete_record, region, table):
		if delete_record:
			if delete_record['awsRegion'] == region:
				deletedItem = delete_record['dynamodb']['OldImage']
				key = delete_record['dynamodb']['Keys']
				obj = {"table":table,"key":key,"item":deletedItem}
				self.find_date_from_item(obj)
	
	def find_date_from_item(self, obj):
		if obj:
			if obj['item']['date']:
				date = obj['item']['date']['S']
				dateValueArray = date.split('-')
				day = dateValueArray[0]
				month = dateValueArray[1]
				year = dateValueArray[2]
				currentDate = datetime.today().strftime('%-d-%-m-%Y')
				currentDateArray = currentDate.split('-')
				currentDay = currentDateArray[0]
				currentMonth = currentDateArray[1]
				currentYear = currentDateArray[2]
				if year == currentYear and month >= currentMonth and day >= currentDay:
					if month == currentMonth and day >= currentDay:
						if day == currentDay:
							reminderObj = {"date":date,"duration":"Day","obj":obj}
							self.add_categoty(reminderObj)
							return True
						reminderObj = {"date":date,"duration":"Month","obj":obj}
						self.add_categoty(reminderObj)
						return True
					reminderObj = {"date":date,"duration":"Year","obj":obj}
					self.add_categoty(reminderObj)
					return True
				if year > currentYear:
					reminderObj = {"date":date,"duration":"FYear","obj":obj}
					self.add_categoty(reminderObj)

	def add_categoty(self, reminderObj):
		categories = ["others", "survey", "goal", "birthday", "release", "lifeEvent", "recognition", "celebration"]
		topic = reminderObj['obj']['item']['topic']['S']
		for category in categories:
			if category == topic:
				ReminderOccurrence().set_reminder_item(category, reminderObj)
				return True