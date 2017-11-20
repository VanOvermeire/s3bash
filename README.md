# S3 Bash

### Overview

As an experiment, I wrote a python script that presents S3 as if it was part of the local file system.  
So you can just use stuff like `cd` or `ls`. 

This example will get all buckets, search for one whose name contains 'some-test' and remove it

`s3bsh ls | grep some-test | s3bsh rmb`

Or you can step into the bucket like this:

`s3bsh cd some-example-bucket`

And then see all the objects with `ls`

### Commands:

Note that you can't add flags (e.g. `rm -rf`) and implementation of the more complex
commands is basic:
  
`cd`  
`ls`  
`pwd`  
`touch`   
`mkdir` (makes buckets)  
`rm`   
`cat`  
`less`  
`cp`  
`mv`

### Install

*On Linux or Mac*: run `./setup.sh`.   
See requirements.txt for pip requirements

### To Do

- commands?
- use token to get all objects in bucket (instead of first x)  
- more checks
