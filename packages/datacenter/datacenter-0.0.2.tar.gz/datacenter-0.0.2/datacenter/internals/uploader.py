"""数据上传，DataCenter 内部代码，非外部调用者使用
by tacey@XARC on 2020/11/3
"""
"""数据上传
by tacey@XARC on 2020/12/22
"""

import os
import shutil
import logging
import subprocess
import concurrent.futures
from requests import Session


class UploaderBase:
    def __init__(self, url, file_path, file_name, fields=None, headers=None, **kwargs):
        self.url = url
        self.file_path = file_path
        self.fields = fields
        self.headers = headers
        self.file_name = file_name

    def run(self):
        raise NotImplemented


class SimpleUploader(UploaderBase):

    def run(self):
        with Session() as session:
            with open(self.file_path, "rb") as f:
                file_field = {'file': (self.file_name, f)}
                resp = session.post(self.url, data=self.fields, files=file_field, stream=True)
                code = resp.status_code
        return code


def simple_upload(url, file_path, file_name, fields=None, headers=None):
    return SimpleUploader(url, file_path, file_name, fields, headers).run()


def simple_plus_upload(url, file_path, file_name, fields=None, headers=None):
    return SimplePlusUploader(url, file_path, file_name, fields, headers).run()


def upload():
    raise NotImplemented


class SimplePlusUploader(UploaderBase):

    def read_in_chunk(self, file_object, chunk_size=65536):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def run(self):
        content_path = os.path.abspath(self.file_path)
        content_size = os.stat(content_path).st_size
        index = 0
        offset = 0
        # 'application/octet-stream'
        headers = {'Content-length': str(content_size)}
        with Session() as session:
            with open(self.file_path, "rb") as f:
                for chunk in self.read_in_chunk(f):
                    offset = index + len(chunk)
                    file_field = {'file': (self.file_name, chunk)}
                    headers['Content-Range'] = 'bytes %s-%s/%s' % (index, offset, content_size)
                    headers['X-Content-Range'] = headers['Content-Range']
                    index = offset
                    session.post(self.url, data=self.fields, headers=headers, files=file_field)


class CURLUploader:  # TODO: file_name不生效

    def __init__(self, url, file_path, file_name, fields=None, **kwargs):
        self.url = url
        self.file_path = file_path
        self.file_name = file_name
        self.fields = ""
        if fields is not None:
            self.fields = " ".join([f'-F "{k}={v}"' for k, v in fields.items()])

    def run(self):
        curl = os.getenv("CURL_PATH")
        curl = curl if curl else shutil.which("curl")
        if not curl:
            logging.warning("使用本地Python-Uploader")
            return SimpleUploader(url=self.url, file_=self.file_path).run()
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        # 注意：-F file字段必须放在最后，S3会忽略file字段之后的所有字段
        result = subprocess.run(
            [shutil.which("sh"), "-c",
             f'{curl} -k {self.fields} -F "file=@{self.file_path}"  "{self.url}" -i'],
            stderr=subprocess.PIPE)
        if result.returncode != 0:
            logging.exception(result.stderr)
        return not (bool(result.returncode))


def curl_upload(url, file_path, file_name, fields=None):
    return CURLUploader(url, file_path, file_name, fields).run()


class S3Uploader(UploaderBase):
    MAX_PART_NUM = 1000
    CHUNK_SIZE = 1024 * 8 * 60
    MAX_PART_WORKERS = (os.cpu_count() or 1) * 5
    BIG_LIMIT = CHUNK_SIZE

    def __init__(self, file_path, file_name, single_url=None, start_url=None, part_url=None,
                 complete_url=None, abort_url=None, **kwargs):
        super().__init__(None, file_path, file_name, **kwargs)
        self.single_url = os.getenv("DC_DU_SINGLE_URL") if single_url is None else single_url
        self.start_url = os.getenv("DC_DU_START_URL") if start_url is None else start_url
        self.part_url = os.getenv("DC_DU_PART_URL") if part_url is None else part_url
        self.complete_url = os.getenv(
            "DC_DU_COMPLETE_URL") if complete_url is None else complete_url
        self.abort_url = os.getenv("DC_DU_ABORT_URL") if abort_url is None else abort_url
        self.content_size = 0
        self.upload_id = -1
        self.uploaded_parts = set()
        self.remain_parts = set()

    def __start(self):
        """开始上传"""
        with Session() as session:
            resp = session.post(self.start_url, data={"object_name": self.file_name})
            self.upload_id = resp.json()["data"]["upload_id"]
        return self.upload_id

    def __parting(self):
        data = {
            "upload_id": self.upload_id,
            "number": self.MAX_PART_NUM,
            "length": self.content_size
        }
        with Session() as session:
            resp = session.post(self.part_url, data=data)
            self.remain_parts = set(resp.json()["data"]["urls"])

    def __upload(self):
        """上传各个分块"""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for url in self.remain_parts:
                futures.append(executor.submit(simple_upload, url=url))
            for future in concurrent.futures.as_completed(futures):
                self.uploaded_parts.add(future.result())

    def __complete(self):
        """通知完成上传（文件上传完毕）"""
        with Session() as session:
            resp = session.post(url=self.complete_url, data={"upload_id": self.upload_id})
        return resp.status_code

    def abort(self):
        """通知终断上传（放弃所有）"""
        with Session() as session:
            resp = session.post(url=self.abort_url, data={"upload_id": self.upload_id})
        return resp.status_code

    def __sigle(self):
        # 根据single-url获取生成的预签名
        with Session() as session:
            resp = session.post(self.single_url, data={"object_name": self.file_name})
            resp_json = resp.json()
        url = resp_json.get("url")
        fields = resp_json.get("fields")
        return simple_upload(url=url, file_path=self.file_path,
                             file_name=self.file_path, fields=fields)

    def __pre(self):
        content_path = os.path.abspath(self.file_path)
        self.content_size = os.stat(content_path).st_size
        return self.content_size

    def run(self):
        """运行"""
        self.__pre()
        if self.content_size <= self.BIG_LIMIT:
            return self.__sigle()
        self.__start()
        self.__parting()
        self.__complete()


def s3_upload(**kwargs):
    return S3Uploader(**kwargs).run()
