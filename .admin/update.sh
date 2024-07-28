#!/bin/bash

# Set up variables
PROJECT_DIR="/home/seastco/workspace/tectonic-alert"
VENV_DIR="${PROJECT_DIR}/venv"
PACKAGE_DIR="${PROJECT_DIR}/lambda_package"
ZIP_FILE="${PROJECT_DIR}/lambda_package.zip"
LAMBDA_FUNCTION_NAME="earthquakeAlert"

# Activate venv and install dependencies
cd "$PROJECT_DIR"
source "${VENV_DIR}/bin/activate"
pip install -r requirements.txt

# Clean up any previous package
rm -rf "$PACKAGE_DIR" "$ZIP_FILE"

# Create package directory and copy source code
mkdir -p "$PACKAGE_DIR"
cp -r config storage sms alerts main.py requirements.txt "$PACKAGE_DIR"
cp -r "${VENV_DIR}/lib/python3.10/site-packages/"* "$PACKAGE_DIR/"
cp -r "${VENV_DIR}/lib64/python3.10/site-packages/"* "$PACKAGE_DIR/"

# Zip the package
cd "$PACKAGE_DIR"
zip -r "$ZIP_FILE" .

# Clean up
deactivate
cd "$PROJECT_DIR"
rm -rf "$PACKAGE_DIR"

# Upload lambda package & publish
aws lambda update-function-code --function-name "$LAMBDA_FUNCTION_NAME" --zip-file fileb://"$ZIP_FILE"
sleep 15
aws lambda publish-version --function-name "$LAMBDA_FUNCTION_NAME"

# Clean up zip file
rm -f "$ZIP_FILE"
