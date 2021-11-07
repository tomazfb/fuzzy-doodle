#!/bin/bash

aws cloudformation create-stack --capabilities CAPABILITY_NAMED_IAM --stack-name fuzzy-doodle-environment --template-body file://createawsenvironment.yml --parameters ParameterKey=SourceS3Bucket,ParameterValue=fuzzy-doodle-source
