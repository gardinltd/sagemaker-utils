import io
from typing import List

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
        elif bucket_name and prefix and filename:
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
        elif bucket_name and prefix and filename:
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
        elif org_bucket and org_prefix and org_filename:
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
        elif dest_bucket and dest_prefix and dest_filename:
            dest_key = dest_prefix.strip('/') + '/' + dest_filename.strip('/')
    else:
        raise NameError("""Please provide at least one of the following combinations for destination:
          - dest_s3_uri
          - dest_bucket and dest_key
          - dest_bucket and dest_prefix and dest_filename
        """)

    copy_source = {'Bucket': org_bucket, 'Key': org_key}
    s3_client.copy_object(Bucket=dest_bucket, Key=dest_key, CopySource=copy_source)


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
        elif bucket_name and prefix and filename:
            key = prefix.strip('/') + '/' + filename.strip('/')
    else:
        raise NameError("""Please provide at least one of the following combinations:
          - s3_uri
          - bucket_name and key
          - bucket_name and prefix and filename
        """)
    
    s3_client.delete_object(Bucket=bucket_name, Key=key)


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
    copy_file_in_s3(
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

    delete_file_in_s3(
        s3_client,
        org_s3_uri = org_s3_uri,
        org_bucket = org_bucket, 
        org_key = org_key,
        org_prefix = org_prefix,
        filename = org_filename,
    )


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
    if s3_uri or (bucket_name and prefix):
        if s3_uri:
            bucket_name = s3_uri.split('/')[2]
            prefix = '/'.join(s3_uri.split('/')[3:])
    else:
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
        
        response_list.extend(resp['Contents'])
        if not resp['IsTruncated']:
            break        
        ContinuationToken = resp['NextContinuationToken']
    return response_list
