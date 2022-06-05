import io
import os
import hashlib
from typing import List
from xml.dom import ValidationErr


def upload_file_to_s3(
    s3_client,
    file_bytes: bytes,
    s3_uri: str = None,
    bucket_name: str = None, 
    key: str = None,
    prefix: str = None,
    filename: str = None,
) -> None:
    """Uploads a bytefile object to s3.

    Must provide at least one of the following combinations:
      - s3_uri
      - bucket_name and key
      - bucket_name and prefix and filename
    """
    if s3_uri or (bucket_name and key) or (bucket_name and prefix and filename):
        if s3_uri:
            bucket_name = s3_uri.split('/')[2]
            key = '/'.join(s3_uri.split('/')[3:])
        elif prefix and filename:
            key = prefix.strip('/') + '/' + filename.strip('/')
    else:
        raise NameError("""Please provide at least one of the following combinations:
          - s3_uri
          - bucket_name and key
          - bucket_name and prefix and filename
        """)

    s3_client.upload_fileobj(io.BytesIO(file_bytes), bucket_name, key)


def read_file_from_s3(
    s3_client,
    s3_uri: str = None,
    bucket_name: str = None,
    key: str = None,
    prefix: str = None,
    filename: str = None
) -> bytes:
    """Reads a file from s3 and returns as bytes object.

    Must provide at least one of the following combinations:
      - s3_uri
      - bucket_name and key
      - bucket_name and prefix and filename
    """
    if s3_uri or (bucket_name and key) or (bucket_name and prefix and filename):
        if s3_uri:
            bucket_name = s3_uri.split('/')[2]
            key = '/'.join(s3_uri.split('/')[3:])
        elif prefix and filename:
            key = prefix.strip('/') + '/' + filename.strip('/')
    else:
        raise NameError("""Please provide at least one of the following combinations:
          - s3_uri
          - bucket_name and key
          - bucket_name and prefix and filename
        """)

    file_bytes = io.BytesIO()
    s3_client.download_fileobj(bucket_name, key, file_bytes)
    return file_bytes.getvalue()


def copy_file_in_s3(
    s3_client,
    org_s3_uri: str = None,
    org_bucket: str = None, 
    org_key: str = None,
    org_prefix: str = None,
    org_filename: str = None,
    dest_s3_uri: str = None,
    dest_bucket: str = None, 
    dest_key: str = None,
    dest_prefix: str = None,
    dest_filename: str = None
) -> None:
    """Copies a file in s3 to another location in s3.

    Must provide at least one of the following combinations for origin:
      - org_s3_uri
      - org_bucket and org_key
      - org_bucket and org_prefix and org_filename
    And one of the following combinations for destination:
      - dest_s3_uri
      - dest_bucket and dest_key
      - dest_bucket and dest_prefix and dest_filename
    """
    if org_s3_uri or (org_bucket and org_key) or (org_bucket and org_prefix and org_filename):
        if org_s3_uri:
            org_bucket = org_s3_uri.split('/')[2]
            org_key = '/'.join(org_s3_uri.split('/')[3:])
        elif org_prefix and org_filename:
            org_key = org_prefix.strip('/') + '/' + org_filename.strip('/')
    else:
        raise NameError("""Please provide at least one of the following combinations for originating source:
          - org_s3_uri
          - org_bucket and org_key
          - org_bucket and org_prefix and org_filename
        """)

    if dest_s3_uri or (dest_bucket and dest_key) or (dest_bucket and dest_prefix and dest_filename):
        if dest_s3_uri:
            dest_bucket = dest_s3_uri.split('/')[2]
            dest_key = '/'.join(dest_s3_uri.split('/')[3:])
        elif dest_prefix and dest_filename:
            dest_key = dest_prefix.strip('/') + '/' + dest_filename.strip('/')
    else:
        raise NameError("""Please provide at least one of the following combinations for destination:
          - dest_s3_uri
          - dest_bucket and dest_key
          - dest_bucket and dest_prefix and dest_filename
        """)

    copy_source = {'Bucket': org_bucket, 'Key': org_key}
    return s3_client.copy_object(Bucket=dest_bucket, Key=dest_key, CopySource=copy_source)


def delete_file_in_s3(
    s3_client,
    s3_uri: str = None,
    bucket_name: str = None, 
    key: str = None,
    prefix: str = None,
    filename: str = None
) -> bytes:
    """Deletes a file in s3.

    Must provide at least one of the following combinations:
      - s3_uri
      - bucket_name and key
      - bucket_name and prefix and filename
    """
    if s3_uri or (bucket_name and key) or (bucket_name and prefix and filename):
        if s3_uri:
            bucket_name = s3_uri.split('/')[2]
            key = '/'.join(s3_uri.split('/')[3:])
        elif prefix and filename:
            key = prefix.strip('/') + '/' + filename.strip('/')
    else:
        raise NameError("""Please provide at least one of the following combinations:
          - s3_uri
          - bucket_name and key
          - bucket_name and prefix and filename
        """)

    return s3_client.delete_object(Bucket=bucket_name, Key=key)


def move_file_in_s3(
    s3_client,
    org_s3_uri: str = None,
    org_bucket: str = None, 
    org_key: str = None,
    org_prefix: str = None,
    org_filename: str = None,
    dest_s3_uri: str = None,
    dest_bucket: str = None, 
    dest_key: str = None,
    dest_prefix: str = None,
    dest_filename: str = None
) -> None:
    """Copies a file in s3 to another location in s3 and deletes the original.

    Must provide at least one of the following combinations for origin:
      - org_s3_uri
      - org_bucket and org_key
      - org_bucket and org_prefix and org_filename
    And one of the following combinations for destination:
      - dest_s3_uri
      - dest_bucket and dest_key
      - dest_bucket and dest_prefix and dest_filename
    """
    copy_resp = copy_file_in_s3(
        s3_client,
        s3_uri = org_s3_uri,
        bucket_name = org_bucket, 
        key = org_key,
        prefix = org_prefix,
        org_filename = org_filename,
        dest_s3_uri = dest_s3_uri,
        dest_bucket = dest_bucket, 
        dest_key = dest_key,
        dest_prefix = dest_prefix,
        dest_filename = dest_filename
    )

    delete_resp = delete_file_in_s3(
        s3_client,
        org_s3_uri = org_s3_uri,
        org_bucket = org_bucket, 
        org_key = org_key,
        org_prefix = org_prefix,
        filename = org_filename,
    )

    return copy_resp, delete_resp


def list_s3_objects(
    s3_client,
    s3_uri: str = None,
    bucket_name: str = None, 
    prefix: str = None,
) -> List:
    """Lists files in s3.

    Must provide at least one of the following combinations:
      - s3_uri
      - bucket_name and prefix
    """
    if s3_uri:
        bucket_name = s3_uri.split('/')[2]
        prefix = '/'.join(s3_uri.split('/')[3:])
    elif not (bucket_name and prefix):
        raise NameError("""Please provide at least one of the following combinations:
          - s3_uri
          - bucket_name and prefix
        """)

    response_list = []
    ContinuationToken = None
    while True:
        if ContinuationToken:
            resp = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, ContinuationToken=ContinuationToken)
        else:
            resp = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        if 'Contents' in resp:
            response_list.extend(resp['Contents'])
        if not resp['IsTruncated']:
            break
        ContinuationToken = resp['NextContinuationToken']
    return response_list


def list_s3_object_versions(
    s3_client,
    s3_uri: str = None,
    bucket_name: str = None,
    prefix: str = None,
) -> List:
    """Lists files with all their versions in s3.

    Must provide at least one of the following combinations:
      - s3_uri
      - bucket_name and prefix
    """
    if s3_uri:
        bucket_name = s3_uri.split('/')[2]
        prefix = '/'.join(s3_uri.split('/')[3:])
    elif not (bucket_name and prefix):
        raise NameError("""Please provide at least one of the following combinations:
          - s3_uri
          - bucket_name and prefix
        """)

    response_list = []
    KeyMarker, VersionIdMarker = None, None

    while True:
        if KeyMarker and VersionIdMarker:
            resp = s3_client.list_object_versions(Bucket=bucket_name, Prefix=prefix, KeyMarker=KeyMarker, VersionIdMarker=VersionIdMarker)
        elif KeyMarker:
            resp = s3_client.list_object_versions(Bucket=bucket_name, Prefix=prefix, KeyMarker=KeyMarker)
        elif VersionIdMarker:
            resp = s3_client.list_object_versions(Bucket=bucket_name, Prefix=prefix, VersionIdMarker=VersionIdMarker)
        else:
            resp = s3_client.list_object_versions(Bucket=bucket_name, Prefix=prefix)

        if 'Versions' in resp:
            response_list.extend(resp['Versions'])
        if 'DeleteMarkers' in resp:
            response_list.extend(resp['DeleteMarkers'])
        if not resp['IsTruncated']:
            break
        KeyMarker = resp['NextKeyMarker']
        VersionIdMarker = resp['NextVersionIdMarker']

    return response_list


def delete_folder_in_s3(
    s3_client,
    s3_uri: str = None,
    bucket_name: str = None,
    prefix: str = None,
) -> bytes:
    """Deletes a folder in s3.

    Must provide at least one of the following combinations:
      - s3_uri
      - bucket_name and prefix
    """
    if s3_uri:
        bucket_name = s3_uri.split('/')[2]
        prefix = '/'.join(s3_uri.split('/')[3:])
    elif not (bucket_name and prefix):
        raise NameError("""Please provide at least one of the following combinations:
          - s3_uri
          - bucket_name and prefix
        """)

    listed_files = list_s3_objects(
        s3_client,
        s3_uri = s3_uri,
        bucket_name = bucket_name,
        prefix = prefix,
    )
    files_to_delete = [{'Key': obj['Key']} for obj in listed_files]

    success = []
    errors = []
    for i in range(0, len(files_to_delete), 1000):
        resp = s3_client.delete_objects(
            Bucket=bucket_name,
            Delete={
                'Objects': files_to_delete[i:i+1000],
            }
        )
        if 'Deleted' in resp:
            success.extend(resp['Deleted'])
        if 'Errors' in resp:
            errors.extend(resp['Errors'])

    return success, errors


def perminently_delete_folder_in_s3(
    s3_client,
    s3_uri: str = None,
    bucket_name: str = None,
    prefix: str = None,
    password: str = None
) -> bytes:
    """Deletes a folder in s3 perminently.

    Must provide at least one of the following combinations:
      - s3_uri
      - bucket_name and prefix
    """
    if not password:
        raise NameError('Please provide password for this sensitive operation')
    elif hashlib.sha224(password.encode('utf-8')).hexdigest() != 'a694b788f26e4613fbdac0fd67c141ace918efa41e9a4ff94116ef43':
        raise ValidationErr('Wrong Password!')


    if s3_uri:
        bucket_name = s3_uri.split('/')[2]
        prefix = '/'.join(s3_uri.split('/')[3:])
    elif not (bucket_name and prefix):
        raise NameError("""Please provide at least one of the following combinations:
          - s3_uri
          - bucket_name and prefix
        """)

    listed_files = list_s3_object_versions(
        s3_client,
        s3_uri = s3_uri,
        bucket_name = bucket_name,
        prefix = prefix,
    )
    files_to_delete = [{'Key': obj['Key'], 'VersionId': obj['VersionId']} for obj in listed_files]

    success = []
    errors = []
    for i in range(0, len(files_to_delete), 1000):
        resp = s3_client.delete_objects(
            Bucket=bucket_name,
            Delete={
                'Objects': files_to_delete[i:i+1000],
            }
        )
        if 'Deleted' in resp:
            success.extend(resp['Deleted'])
        if 'Errors' in resp:
            errors.extend(resp['Errors'])

    return success, errors


def download_s3_folder(
    s3_client,
    local_dir,
    s3_uri: str = None,
    bucket_name: str = None,
    prefix: str = None,
) -> None:
    """Downloads s3 folder to local destination.

    Must provide at least one of the following combinations:
      - s3_uri
      - bucket_name and prefix
    """
    if s3_uri:
        bucket_name = s3_uri.split('/')[2]
        prefix = '/'.join(s3_uri.split('/')[3:])
    elif not (bucket_name and prefix):
        raise NameError("""Please provide at least one of the following combinations:
          - s3_uri
          - bucket_name and prefix
        """)

    objects = list_s3_objects(s3_client, s3_uri, bucket_name, prefix)
    for i, obj in enumerate(objects):
        target = os.path.join(local_dir, os.path.relpath(obj['Key'], prefix))
        print(f'\rDownloading files {i+1}/{len(objects)}...', end='', flush=True)

        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target), exist_ok=True)
        if obj['Key'][-1] == '/':
            continue

        s3_client.download_file(bucket_name, obj['Key'], target)
