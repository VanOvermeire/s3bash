# S3 Bash

### Overview

As an experiment, I wrote a python script that presents S3 as if it was part of the local file system,
where you can use stuff like `cd` or `ls` to query the data. 

This example will get all buckets, search for one whose name contains "some-test" and remove it

`s3bsh ls | grep some-test | s3bsh rmb`

Or you can step into the bucket

`s3bsh cd some-example-bucket`

### Commands:

Note that you can't add flags (e.g. `rm -rf`) and implementation of the more complex
commands is basic:
  
`ls`,  
`pwd`,  
`touch`,   
`mkdir` (makes buckets),  
`rm`,  
`cd`,  
`cat`,  
`less`,  
`cp`

### Install

*On Linux or Mac*: run `./setup.sh`  
*Requirement*: boto3 needs to be installed on your pc.
