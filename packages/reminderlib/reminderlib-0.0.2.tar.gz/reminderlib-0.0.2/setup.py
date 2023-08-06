from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='reminderlib',
  version='0.0.2',
  description='sample reminder library for AWS dynamodb',
  long_description=open('README.MD').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Jayashathiskumar Jayakumar',
  author_email='x20154810@student.ncirl.ie',
  classifiers=classifiers,
  keywords='reminder', 
  packages=find_packages(),
  install_requires=[''] 
)