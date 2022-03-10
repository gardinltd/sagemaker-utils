import io
import tempfile
import numpy as np
import time

def protobuf_to_numpy_mask(bytes_obj: bytes):
    """Converts record io protobuf response from Segmentation model
    to a numpy segment mask array"""
    from sagemaker.amazon.record_pb2 import Record
    import mxnet as mx

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

