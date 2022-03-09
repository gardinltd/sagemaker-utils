import io
import tempfile
import numpy as np


def protobuf_to_numpy_mask(bytes_obj):
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