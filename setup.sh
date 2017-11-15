#!/usr/bin/env bash

echo "Creating .s3bsh directory and subdirectory"
cd ~
mkdir -p .s3bsh/s3bash

echo "Adding our python scripts to that dir"
cd -
cp s3bash.py ~/.s3bsh/
cp -r s3bash/*.py ~/.s3bsh/s3bash/

echo "Adding empty s3data file"
touch ~/.s3bsh/s3data
echo "Adding bash script to /usr/local/bin"
sudo cp s3bsh.sh /usr/local/bin/s3bsh
