#!/bin/bash

# Actvate venv and pip install
cd /home/seastco/workspace/earthquake-alert
source venv/bin/activate
pip install -r requirements.txt

# Make lambda_package, copy in source code and packages, zip
mkdir -p lambda_package
cp -r . lambda_package/
cp -r venv/lib/python3.10/site-packages/* lambda_package/ 
cp -r venv/lib64/python3.10/site-packages/* lambda_package/
cd lambda_package
zip -r ../lambda_package.zip .
cd ..
deactivate

# Upload lambda package & publish
aws lambda update-function-code --function-name earthquakeAlert --zip-file fileb:///home/seastco/workspace/earthquake-alert/lambda_package.zip
aws lambda publish-version --function-name earthquakeAlert
rm -rf lambda_package
rm -f lambda_package.zip
