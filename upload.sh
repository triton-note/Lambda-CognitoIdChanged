#!/bin/bash

NAME="TritonNote-CognitoIdChanged"
ZIPFILE="code.zip"

rm "$ZIPFILE"
zip -r "$ZIPFILE" *.py
echo

echo "Uploading ${ZIPFILE} to ${NAME}"
aws lambda update-function-code --function-name ${NAME} --zip-file "fileb://${ZIPFILE}"
echo

echo "Testing ${NAME}"
aws lambda invoke --invocation-type RequestResponse --function-name ${NAME} --payload file://test-input.json test-output.json
cat test-output.json
echo
