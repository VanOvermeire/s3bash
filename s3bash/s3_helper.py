import boto3


NO_BUCKET = 's3'


def get_s3_client():
    boto3.setup_default_session()
    return boto3.client('s3')


def is_object_name(client, bucket, name):
    try:
        client.get_object(Bucket=bucket, Key=name)
        return True
    except:
        return False


def is_bucket_name(client, name):
    response = client.list_buckets()['Buckets']
    for r in response:
        if name == r['Name']:
            return True
    return False


def put_local_to_s3(client, local, bucket, key):
    with open(local, "rb") as local_file:
        file_as_bytes = local_file.read()
        client.put_object(Body=file_as_bytes, Bucket=bucket, Key=key)


def download_s3_file(bucket, key, location):
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(bucket).download_file(key, location)
    except:
        exit(1)


def handle_create_bucket(client, name):
    print('creating ' + name)
    response = client.create_bucket(name)
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        print('Could not create bucket')
        exit(1)


def handle_delete(client, current_bucket, name):
    if current_bucket == NO_BUCKET and is_bucket_name(name):
        print('delete the bucket' + name)
        response = client.delete_bucket(name)
        if response['ResponseMetadata']['HTTPStatusCode'] != 204:
            exit(1)
    elif is_object_name(current_bucket, name):
        client.delete_object(Bucket=current_bucket, Key=name)
    else:
        exit(1)
