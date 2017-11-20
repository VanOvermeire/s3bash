import sys
import os

S3_DIRECTORY_NAME= 'S3_DIRECTORY'
NO_BUCKET = 's3'


def check_number_of_args(number):
    if len(sys.argv) < number:
        exit(1)


def get_additional_arguments_as_list():
    return sys.argv[2:]


def has_at_least_one_argument(args):
    return len(list(args)) > 0


def get_standard_input_as_list():
    our_stdin_list = []

    if not sys.stdin.isatty():
        our_stdin_list = sys.stdin.read().split('\n')
    return our_stdin_list


def get_list_without_emtpy_elements(names):
    new_names = []
    for name in names:
        if len(name) > 0:
            new_names.append(name)
    return new_names


def get_without_leading_forward_slash(list_of_elements):
    if len(list_of_elements[0]) == 0:
        return list_of_elements[1:]
    return list_of_elements


def set_current_s3_directory(name):
    # dir and file were created by setup
    my_file = os.path.expanduser('~/.s3bsh/s3data')
    # just overwrite all contents for now
    with open(my_file, 'w') as s3data:
        s3data.write('DIRECTORY=' + name)


def get_current_s3_directory():
    my_file = os.path.expanduser('~/.s3bsh/s3data')

    with open(my_file, 'r') as s3data:
        for line in s3data.readlines():
            if 'DIRECTORY' in line:
                return line.split('=')[1].replace('\n', '')
    return NO_BUCKET


def retrieve_bucket_and_key(path):
    elements = get_without_leading_forward_slash(str.split(path, '/'))
    bucket = elements[0]
    key = '/'.join(elements[1:])
    return bucket, key

