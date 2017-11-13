# S3 Bash

As an experiment, I wrote a python script that presents S3 as if it was part of the local file system,
where you can use stuff like `cd` or `ls` to query the data. 

This example will get all buckets, search for one whose name contains "some-test" and remove it

`s3bsh ls | grep some-test | s3bsh rmb`

Or you can step into the bucket

`s3bsh cd some-example-bucket`

And query the files with `ls`, or read one with `less` or `cat` 

To install, just run `./setup.sh`. Should work for Linux, might work for Mac. Won't work for windows.
