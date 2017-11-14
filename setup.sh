#!/usr/bin/env bash

echo "Creating .s3bsh directory"
cd ~
mkdir .s3bsh
echo "Adding our python script to that dir"
cd -
cd s3bash
cp s3bash.py ~/.s3bsh/
echo "Adding empty s3data file"
touch s3data
echo "Adding bash script to /usr/local/bin"
sudo cp s3bsh.sh /usr/local/bin/s3bsh
