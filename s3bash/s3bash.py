import sys
import os
import boto3

# TODO commands: '>' (f), mv (f)
# TODO split up file (s3, handlers, checks and this)
# TODO use token to get all objects in bucket (instead of first x); more checks

S3_DIRECTORY_NAME= 'S3_DIRECTORY'
NO_BUCKET = 's3'


def get_s3_client():
    boto3.setup_default_session()
    return boto3.client('s3')


def get_standard_input_as_list():
    our_stdin_list = []

    if not sys.stdin.isatty():
        our_stdin_list = sys.stdin.read().split('\n')
    return our_stdin_list


def get_additional_arguments_as_list():
    return sys.argv[2:]


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


def handle_deletes(names):
    for name in names:
        handle_delete(name)


def handle_delete(name):
    bucket = get_current_s3_directory()
    if bucket == NO_BUCKET and is_bucket_name(name):
        print('delete the bucket' + name)
        response = client.delete_bucket(name)
        if response['ResponseMetadata']['HTTPStatusCode'] != 204:
            exit(1)
    elif is_object_name(bucket, name):
        client.delete_object(Bucket=bucket, Key=name)
    else:
        exit(1)


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


def is_object_name(bucket, name):
    try:
        client.get_object(Bucket=bucket, Key=name)
        return True
    except:
        return False


def is_bucket_name(name):
    response = client.list_buckets()['Buckets']
    for r in response:
        if name == r['Name']:
            return True
    return False


def handle_change_directory(names):
    name = names[0]

    if name == '..':
        set_current_s3_directory(NO_BUCKET)
    else:
        if '/' in name:
            name = str.split(name, '/')[1]

        if is_bucket_name(name):
            set_current_s3_directory(name)
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


def handle_current_directory():
    print(get_current_s3_directory())


def handle_touch_file(names):
    name = names[0]
    bucket = get_current_s3_directory()

    if not bucket == NO_BUCKET and not is_object_name(bucket, name):
        client.put_object(Body=b'', Bucket=bucket, Key=name)
    else:
        exit(1)


# will return whether the FROM is a bucket
def handle_copy(names):
    if len(names) < 2:
        print('not enough arguments')
        exit(1)

    from_location_elements = get_without_leading_forward_slash(str.split(names[0], '/'))
    to_location_elements = get_without_leading_forward_slash(str.split(names[1], '/'))

    is_from_bucket = is_bucket_name(from_location_elements[0])
    is_to_bucket = is_bucket_name(to_location_elements[0])

    # TODO if TO is only a bucket, take the name of the file?

    if is_from_bucket and is_to_bucket:
        client.copy_object(Bucket=to_location_elements[0], Key='/'.join(to_location_elements[1:]),
                           CopySource='/'.join(from_location_elements))
        return True
    elif is_from_bucket:
        download_s3_file(from_location_elements[0], '/'.join(from_location_elements[1:]), names[1])
        return True
    elif is_to_bucket:
        put_local_to_s3(names[0], to_location_elements[0], '/'.join(to_location_elements[1:]))
        return False
    else:
        # or give to normal bash command
        exit(1)


# TODO start using this for cp
# tuple result (bucket, key)
def retrieve_bucket_and_key(path):
    elements = get_without_leading_forward_slash(str.split(path, '/'))
    bucket = elements[0]
    key = '/'.join(elements[1:])
    return bucket, key


def get_without_leading_forward_slash(list_of_elements):
    if len(list_of_elements[0]) == 0:
        return list_of_elements[1:]


def put_local_to_s3(local, bucket, key):
    with open(local, "rb") as local_file:
        file_as_bytes = local_file.read()
        client.put_object(Body=file_as_bytes, Bucket=bucket, Key=key)


def download_s3_file(bucket, key, location):
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(bucket).download_file(key, location)
    except:
        exit(1)


def handle_move(names):
    is_bucket = handle_copy(names)
    get_without_leading_forward_slash(str.split(names[0], '/'))

    if is_bucket:
        print('removing from bucket')
        # TODO client.delete_object(Bucket=bucket, Key=name)
    else:
        os.remove(names[0])


def handle(our_command, our_arguments):
    if our_command == 'ls':
        handle_list()
    elif our_command == 'pwd':
        handle_current_directory()
    elif has_at_least_one_argument(our_arguments):
        if our_command == 'touch':
            handle_touch_file(our_arguments)
        elif our_command == 'mkdir':
            handle_create_buckets(our_arguments)
        elif our_command == 'rm':
            handle_deletes(our_arguments)
        elif our_command == 'cd':
            handle_change_directory(our_arguments)
        elif our_command == 'cat' or our_command == 'less':
            handle_read_file(our_arguments)
        elif our_command == 'cp':
            handle_copy(our_arguments)
        elif our_command == 'mv':
            handle_move(our_arguments)
    else:
        exit(1)


check_number_of_args(2)

command = sys.argv[1]

arguments = get_standard_input_as_list()
arguments.extend(get_additional_arguments_as_list())
arguments = list_without_emtpy_elements(arguments)

client = get_s3_client()

handle(command, arguments)
