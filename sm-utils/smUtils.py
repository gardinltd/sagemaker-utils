import io
import json
import tempfile
import time
from typing import Sequence

from .s3Utils import read_file_from_s3, upload_file_to_s3


def protobuf_to_numpy_mask(bytes_obj: bytes):
    """Converts record io protobuf response from Segmentation model
    to a numpy segment mask array"""
    from sagemaker.amazon.record_pb2 import Record
    import mxnet as mx
    import numpy as np

    rec = Record()
    imageStream = io.BytesIO(bytes_obj)

    with tempfile.NamedTemporaryFile(mode="w+b") as ftemp:
        ftemp.write(imageStream.read())
        ftemp.seek(0)
        recordio = mx.recordio.MXRecordIO(ftemp.name, "r")
        protobuf = rec.ParseFromString(recordio.read())
    values = list(rec.features["target"].float32_tensor.values)
    shape = list(rec.features["shape"].int32_tensor.values)

    shape = np.squeeze(shape)
    values = np.reshape(np.array(values), shape)
    return np.squeeze(values, axis=0)


def deploy_endpoint(sm_client, endpoint_config_name: str = None, endpoint_name: str = None):
    """Deploys endpoint and waits till its created"""

    start_time = time.perf_counter()

    ep_res = sm_client.create_endpoint(
        EndpointName=endpoint_name, EndpointConfigName=endpoint_config_name
    )
    print(ep_res, '\n\n')

    print('Creating Endpoint', end=' ')
    creating = True
    while creating:
        ep_des_res = sm_client.describe_endpoint(EndpointName=endpoint_name)
        print('.', end='')
        time.sleep(30)
        if ep_des_res["EndpointStatus"] != "Creating":
            print('!\n')
            print(f'Endpoint Name: {endpoint_name}')
            print(f'Endpoint Status: {ep_des_res["EndpointStatus"]}, Time taken: {int(time.perf_counter() - start_time)} sec')
            creating = False


def get_manifest_lines(
    s3_client,
    s3_uri: str = None,
    bucket_name: str = None, 
    key: str = None,
    prefix: str = None,
    filename: str = None
) -> Sequence:
    manifest_bytes = read_file_from_s3(
        s3_client, 
        s3_uri = s3_uri, 
        bucket_name = bucket_name, 
        key = key, 
        prefix = prefix, 
        filename = filename
    )

    lines = []
    with io.BytesIO(manifest_bytes) as f:
        for line in f.readlines():
            lines.append(json.loads(line))
    return lines


def write_lines_to_manifest(
    s3_client,
    lines,
    s3_uri: str = None,
    bucket_name: str = None, 
    key: str = None,
    prefix: str = None,
    filename: str = None
) -> None:
    with tempfile.TemporaryFile(mode="w+b") as ftemp:
        for l in lines:
            ftemp.write(bytes(json.dumps(l), 'utf-8'))
            ftemp.write(b'\n')
        ftemp.seek(0)
        line_bytes = ftemp.read()
    
    upload_file_to_s3(
        s3_client,
        line_bytes,
        s3_uri = s3_uri, 
        bucket_name = bucket_name, 
        key = key, 
        prefix = prefix, 
        filename = filename
    )