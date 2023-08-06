### Sample Reminder Library

## Test the package

1. run 'python setup.py bdist_wheel'
2. run 'install - pip3 install -e .'

## Scripts to upload library

1. Install twine - pip3 install setuptools twine
2. Create a package - 'python setup.py bdist_wheel sdist'
3. Upload - twine upload --repository-url https://upload.pypi.org/legacy/ dist/*   

