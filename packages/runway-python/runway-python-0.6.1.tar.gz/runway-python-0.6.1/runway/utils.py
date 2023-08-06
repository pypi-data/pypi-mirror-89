import tempfile
import tarfile
import inspect
import re
import os
import functools
import sys
import gzip
import datetime
import colorcet
import uuid
import urllib3
import multiprocessing
import certifi
import json
import imageio
from unidecode import unidecode
from io import BytesIO as IO
from urllib.parse import urlparse
import numpy as np
from flask import after_this_request, request, jsonify


URL_REGEX = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def validate_post_request_body_is_json(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        json = get_json_or_none_if_invalid(request)
        if json is not None:
            return f(*args, **kwargs)
        else:
            err_msg = 'The body of all POST requests must contain JSON'
            return jsonify(dict(error=err_msg)), 400
    return wrapped

def get_json_or_none_if_invalid(request):
    if request.headers.get('content-encoding') == 'gzip' and request.headers.get('content-type') == 'application/json':
        data = request.get_data()
        decompressed = gzip_decompress(data)
        return json.loads(decompressed)
    else:
        return request.get_json(force=True, silent=True)

def serialize_command(cmd):
    ret = {}
    ret['name'] = cmd['name']
    ret['description'] = cmd['description']
    ret['inputs'] = [inp.to_dict() for inp in cmd['inputs']]
    ret['outputs'] = [inp.to_dict() for inp in cmd['outputs']]
    return ret


def is_url(path):
    return re.match(URL_REGEX, path)


def get_file_suffix_from_url(url):
    suffix_parts = os.path.basename(urlparse(url).path).split('.')[1:]
    if len(suffix_parts) == 0:
        return ''
    else:
        return '.%s' % '.'.join(suffix_parts)


def get_download_chunks(total_size, chunk_size=1e7):
    n_chunks = max(1, int(total_size // chunk_size))
    for i in range(n_chunks):
        start = (total_size // n_chunks) * i
        end = (total_size // n_chunks) * (i + 1) - 1
        if i == n_chunks - 1: end = max(end, total_size)
        yield [start, end]


def download_worker(url, queue, filename):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    while True:
        try:
            rng = queue.get_nowait()
        except:
            break
        [start, end] = rng
        resp = http.request('GET', url, headers={'Range': 'bytes=' + str(start) + '-' + str(end)})
        f = open(filename, 'r+b')
        f.seek(start)
        f.write(resp.data)
        f.close()


def download_file(url, n_processes=16):
    tmp = tempfile.NamedTemporaryFile(suffix=get_file_suffix_from_url(url), delete=False)
    filename = tmp.name
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    initial_response = http.request('HEAD', url)
    enable_segmented_download = 'accept-ranges' in initial_response.headers and \
        'content-length' in initial_response.headers and \
        initial_response.headers['accept-ranges'] == 'bytes' and \
        initial_response.headers['content-length'] is not None
    if enable_segmented_download:
        content_length = int(initial_response.headers['content-length'])
        manager = multiprocessing.Manager()
        queue = manager.Queue()
        [queue.put(chunk) for chunk in get_download_chunks(content_length)]
        processes = [multiprocessing.Process(target=download_worker, args=(url, queue, filename)) for _ in range(n_processes)]
        [process.start() for process in processes]
        [process.join() for process in processes]
    else:
        resp = http.request('GET', url)
        f = open(filename, 'wb')
        f.write(resp.data)
        f.close()
    return filename


def extract_tarball(path):
    extracted_dir = tempfile.mkdtemp()
    with tarfile.open(path, 'r:*', errors='ignore') as tar:
        def encode_ascii(member):
            member.name = unidecode(member.name)
        [encode_ascii(member) for member in tar.getmembers()]
        tar.extractall(path=extracted_dir)
    return extracted_dir


def gzip_compress(data):
    compressed_data = IO()
    g = gzip.GzipFile(fileobj=compressed_data, mode='w')
    g.write(data)
    g.close()
    return compressed_data.getvalue()


def gzip_decompress(data):
    compressed_data = IO(data)
    return gzip.GzipFile(fileobj=compressed_data, mode='r').read()


def gzipped(f):
    @functools.wraps(f)
    def view_func(*args, **kwargs):
        @after_this_request
        def zipper(response):
            accept_encoding = request.headers.get('Accept-Encoding', '')

            if 'gzip' not in accept_encoding.lower():
                return response

            response.direct_passthrough = False

            if (response.status_code < 200 or
                response.status_code >= 300 or
                'Content-Encoding' in response.headers):
                return response

            gzip_buffer = IO()
            gzip_file = gzip.GzipFile(mode='wb', fileobj=gzip_buffer)
            gzip_file.write(response.data)
            gzip_file.close()

            response.data = gzip_buffer.getvalue()
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Vary'] = 'Accept-Encoding'
            response.headers['Content-Length'] = len(response.data)

            return response

        return f(*args, **kwargs)

    return view_func


def try_cast_np_scalar(value):
    if type(value).__module__ == 'numpy' and np.isscalar(value):
        return value.item()
    return value


def cast_to_obj(cls_or_obj):
    if inspect.isclass(cls_or_obj):
        return cls_or_obj()
    return cls_or_obj


def timestamp_millis():
    offset = datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)
    return int(offset.total_seconds() * 1000)


def get_color_palette(name):
    palette = getattr(colorcet, name)
    return [[int(c[0]*255), int(c[1]*255), int(c[2]*255)] for c in palette]

  
def argspec(fn):
    return inspect.getfullargspec(fn)


def deserialize_data(data, fields):
    ret = {}
    for field in fields:
        name = field.name
        if name in data:
            ret[name] = field.deserialize(data[name])
        elif hasattr(field, 'default'):
            ret[name] = field.default
        else:
            raise Exception('Missing field:', field.name)
    return ret


def serialize_data(data, fields, output_formats=None):
    if output_formats is None:
        output_formats = {}
    if type(data) != dict and len(fields) == 1:
        name = fields[0].name
        data = {name: data}
    ret = {}
    for field in fields:
        name = field.name
        output_format = output_formats.get(field.name)
        ret[name] = field.serialize(data[name], output_format=output_format)
    return ret
    

def generate_uuid():
    return uuid.uuid4().hex


def adjust_dynamic_range(data, drange_in, drange_out):
    if drange_in != drange_out:
        scale = (np.float32(drange_out[1]) - np.float32(drange_out[0])) / (
            np.float32(drange_in[1]) - np.float32(drange_in[0])
        )
        bias = np.float32(drange_out[0]) - np.float32(drange_in[0]) * scale
        data = data * scale + bias
        return data


def encode_image(image, image_format):
    buffer = IO()
    if image_format.upper() in ['PNG', 'JPEG']:
        image.save(buffer, format=image_format)
    else:
        data = np.array(image)
        adjusted = adjust_dynamic_range(data, [0, 255], [0, 1])
        imageio.plugins.freeimage.download()
        imageio.imwrite(buffer, adjusted.astype(np.float32), format='exr')
    return buffer.getvalue()


def parse_output_formats_from_header(value):
    result = {}
    for item in map(str.strip, value.split(';')):
        if not item:
            continue
        name, value = item.split('=', 1)
        result[name] = value
    return result
