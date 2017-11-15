import sys
import os
from s3bash import s3_helper, helpers


NO_BUCKET = 's3'


def handle_list():
    bucket = helpers.get_current_s3_directory()

    if bucket == NO_BUCKET:
        names = s3_helper.get_list_of_bucket_names(client)
    else:
        names = s3_helper.get_list_of_objects(client, bucket)

    for name in names:
        print(name)


def handle_change_directory(names):
    name = names[0]

    if name == '..':
        helpers.set_current_s3_directory(NO_BUCKET)
    else:
        # TODO this could be better, separate method
        if '/' in name:
            name = str.split(name, '/')[1]

        if s3_helper.is_bucket_name(client, name):
            helpers.set_current_s3_directory(name)
            print(name)
        else:
            print('Bucket does not exist')
            exit(1)


def handle_read_file(names):
    bucket = helpers.get_current_s3_directory()
    name = names[0]

    if not bucket == NO_BUCKET:
        object_as_string = s3_helper.get_s3_object_as_string(client, bucket, name)
        print(object_as_string)


def handle_current_directory():
    print(helpers.get_current_s3_directory())


def handle_touch_file(names):
    name = names[0]
    bucket = helpers.get_current_s3_directory()

    if not bucket == NO_BUCKET and not s3_helper.is_object_name(client, bucket, name):
        s3_helper.put_empty_s3_object(client, bucket, name)
    else:
        exit(1)


# will return whether the FROM is a bucket
def handle_copy(names):
    if len(names) < 2:
        print('not enough arguments')
        exit(1)

    from_location_elements = helpers.get_without_leading_forward_slash(str.split(names[0], '/'))
    to_location_elements = helpers.get_without_leading_forward_slash(str.split(names[1], '/'))

    is_from_bucket = s3_helper.is_bucket_name(from_location_elements[0])
    is_to_bucket = s3_helper.is_bucket_name(to_location_elements[0])

    # TODO if TO is only a bucket, take the name of the file?

    if is_from_bucket and is_to_bucket:
        s3_helper.copy_object_between_buckets(client, '/'.join(from_location_elements), to_location_elements[0],
                                              '/'.join(to_location_elements[1:]))
        return True
    elif is_from_bucket:
        s3_helper.download_s3_file(from_location_elements[0], '/'.join(from_location_elements[1:]), names[1])
        return True
    elif is_to_bucket:
        s3_helper.put_local_to_s3(client, names[0], to_location_elements[0], '/'.join(to_location_elements[1:]))
        return False
    else:
        # or give to normal bash command
        exit(1)


def handle_move(names):
    is_bucket = handle_copy(names)

    if is_bucket:
        print('removing from bucket') # temp
        bucket, key = helpers.retrieve_bucket_and_key(names[0])
        s3_helper.delete_s3_object(client, bucket, key)
    else:
        os.remove(names[0])


def handle_create_buckets(names):
    for name in names:
        s3_helper.create_bucket(client, name)


def handle_deletes(names):
    for name in names:
        s3_helper.delete_bucket_or_object(client, helpers.get_current_s3_directory(), name)


def handle(our_command, our_arguments):
    if our_command == 'ls':
        handle_list()
    elif our_command == 'pwd':
        handle_current_directory()
    elif helpers.has_at_least_one_argument(our_arguments):
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


helpers.check_number_of_args(2)

command = sys.argv[1]

arguments = helpers.get_standard_input_as_list()
arguments.extend(helpers.get_additional_arguments_as_list())
arguments = helpers.get_list_without_emtpy_elements(arguments)

client = s3_helper.get_s3_client()

handle(command, arguments)
