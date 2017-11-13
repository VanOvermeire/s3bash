import json
import sys
import os
import boto3

# TODO commands cat (for reading files), cd (with prefixes?), rm (file), touch (f), > (f), mv or copy (f)
# TODO active the delete, split up file

S3_DIRECTORY_NAME= 'S3_DIRECTORY'
NO_BUCKET = 'NONE'


def get_standard_input_as_list():
    our_stdin_list = []

    if not sys.stdin.isatty():
        our_stdin_list = sys.stdin.read().split('\n')

    return our_stdin_list


def get_additional_arguments_as_list():
    return sys.argv[2:]


def get_s3_client():
    boto3.setup_default_session()
    return boto3.client('s3')


# or use an exported variable
def get_current_s3_directory():
    try:
        return os.environ[S3_DIRECTORY_NAME]
    except KeyError:
        return NO_BUCKET


def handle_list():
    bucket = get_current_s3_directory()

    if bucket == NO_BUCKET:
        response = client.list_buckets()['Buckets']
        for r in response:
            print(r['Name'])
    else:
        response = client.list_objects_v2(Bucket=bucket)

        for r in response['Contents']:
            print(r['Key'])


def list_without_emtpy_elements(names):
    new_names = []
    for name in names:
        if len(name) > 0:
            new_names.append(name)
    return new_names


def handle_delete_buckets(names):
    for name in names:
        handle_delete_bucket(name)


def handle_delete_bucket(name):
    print('deleting ' + name)
    # response = client.delete_bucket(name)
    # if response['ResponseMetadata']['HTTPStatusCode'] != 204:
    #     exit(1)


def handle_create_buckets(names):
    for name in names:
        handle_create_bucket(name)


def handle_create_bucket(name):
    print('creating ' + name)
    response = client.create_bucket(name)
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('Could not create bucket')
        exit(1)


def check_number_of_args(number):
    if len(sys.argv) < number:
        exit(1)


def has_at_least_one_argument(args):
    return len(list(args)) > 0


def is_bucket_name(name):
    response = client.list_buckets()['Buckets']
    for r in response:
        if name in r['Name']:
            return True
    return False


def handle_change_directory(names):
    name = names[0]

    if name == '..':
        os.environ[S3_DIRECTORY_NAME] = NO_BUCKET
    else:
        if is_bucket_name(name):
            os.environ[S3_DIRECTORY_NAME] = name
            print(name)
        else:
            print('Bucket does not exist')
            exit(1)


def handle_read_file(names):
    bucket = get_current_s3_directory()
    name = names[0]

    if not bucket == NO_BUCKET:
        s3_object = client.get_object(Bucket=bucket, Key=name)
        object_as_string = s3_object['Body'].read()
        print(object_as_string)


check_number_of_args(2)
command = sys.argv[1]
arguments = get_standard_input_as_list()
arguments.extend(get_additional_arguments_as_list())
arguments = list_without_emtpy_elements(arguments)
client = get_s3_client()


if command == 'ls':
    handle_list()
elif has_at_least_one_argument(arguments):
    if command == 'mkb':
        handle_create_buckets(arguments)
    elif command == 'rmb':
        handle_delete_bucket(arguments)
    elif command == 'cd':
        handle_change_directory(arguments)
    elif command == 'cat' or command == 'less':
        handle_read_file(arguments)
