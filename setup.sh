#!/usr/bin/env bash

echo "Installing requirements"
pip3 install -r requirements.txt

echo "Creating .s3bsh directory and subdirectory"
cd ~ &> /dev/null
mkdir -p .s3bsh/s3bash

echo "Adding our python scripts to that dir"
cd - &> /dev/null
cp s3bash.py ~/.s3bsh/
cp -r s3bash/*.py ~/.s3bsh/s3bash/

echo "Adding empty s3data file"
touch ~/.s3bsh/s3data
echo "Adding bash script to /usr/local/bin"
sudo cp s3bsh.sh /usr/local/bin/s3bsh
