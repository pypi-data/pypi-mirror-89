from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='reminderlib',
    version='0.0.5',
    description='Sample reminder library for AWS dynamodb',
    py_modules=["test","__init__","ReminderController/ReminderCategorizer","ReminderController/ReminderManagerService","ReminderController/ReminderOccurrence","ReminderDataListener/ReminderDataListerner","ReminderNotifier/ReminderNotifier"],
    package_dir={'':'ReminderManager'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['boto3','botocore','aws-logging-handlers'],
    url='',  
    author='Jayashathiskumar Jayakumar',
    author_email='x20154810@student.ncirl.ie',
    classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
    ],
)