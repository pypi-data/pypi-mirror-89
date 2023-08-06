"""dataset相关操作
by tacey@XARC on 20-10-30
"""

import concurrent.futures
from datacenter.internals.downloader import SimpleDownloader, Downloader


def detail(session, dataset_id, dataset_version: int = 0):
    """ 获取某个dataset的详情

    :param session: app/user session
    :param dataset_id: 数据集ID
    :param dataset_version: 数据集版本
    :return:
    """
    url_path = "dataset/{}".format(dataset_id)
    json_data = {"version": dataset_version}
    flag, result = session.do_request(path=url_path, json_data=json_data, method="GET")
    return (flag, result["data"]) if flag else (flag, result)


def tree(session, dataset_id, prefix, dataset_version=0):
    """ tree-level-items of one dataset

    :param session: user/app session
    :param dataset_id: 数据集ID
    :param prefix: 层级前缀
    :param dataset_version: 数据集版本号（缺省为0）
    :return:
    """
    url_path = "datasets/{}/tree".format(dataset_id)
    json_data = {"version": dataset_version}
    flag, result = session.do_request(path=url_path, json_data=json_data)
    return (flag, result["data"]["items"]) if flag else (flag, result)


def keys(session, dataset_id, dataset_version=0):
    """数据集的对象key列表

    :param session: app/user session
    :param dataset_id: 数据集ID
    :param dataset_version: 该数据集的版本号
    :return: 数据集的对象key列表
    """
    url_path = "datasets/{}/keys".format(dataset_id)
    json_data = {"version": dataset_version}
    flag, result = session.do_request(url_path, json_data=json_data)
    return (flag, result["data"]["keys"]) if flag else (flag, result)


def versions(session, dataset_id):
    """查询某个数据集的版本数据

    :param session: app/user session
    :param dataset_id: 数据集ID
    :return: 版本数据列表
    """
    url_path = "dataset/{}/versions".format(dataset_id)
    flag, result = session.do_request(url_path)
    return (flag, result["data"]["versions"]) if flag else (flag, result)


def query_list(session, query_by="name", query_content="", page=0, limit=20):
    """ 查询数据集

    :param session: app/user session
    :param query_by: 查询字段， 目前支持（"name","desc"）
    :param query_content: 查询值
    :param page: 第几页（以0为基，缺省为0）
    :param limit: 单页数据量（缺省20）
    :return: 数据集列表
    """
    url_path = "datasets"
    json_data = {"limit": limit, "page": page,
                 "query_by": query_by, "query_content": query_content}
    query_bys = ("name", "desc")
    assert query_by in query_bys, "query_by必须是 {}其中之一".format(str(query_bys))
    flag, result = session.do_request(url_path, json_data=json_data)
    return (flag, result["data"]["dataset_list"]) if flag else (flag, result)


def freeze(session, dataset_id, dataset_version=0):
    """冷冻数据集（S3->Glacier）

    s3(Simple-Object-Storage) to glacier storage

    :param session: app/user session
    :param dataset_id: 数据集ID
    :param dataset_version: 数据集版本
    :return:
    """
    # raise NotImplemented("目前暂不可使用")
    url_path = "datasets/{}/freezen".format(dataset_id)
    json_data = {"version": dataset_version}
    flag, result = session.do_request(path=url_path, json_data=json_data, method="POST")
    return (flag, result["data"]["freezen_id"]) if flag else (flag, result)


def unfreeze(session, dataset_id, dataset_version=0):
    """解冻数据集 (Glacier->S3->Glacier)

     glacier storage to s3(Simple-Object-Storage)

    :param session: app/user session
    :param dataset_id: 数据集ID
    :param dataset_version: 数据集版本
    :return: freezen_id
    """
    # raise NotImplemented("目前暂不可使用")
    url_path = "datasets/{}/unfreezen".format(dataset_id)
    json_data = {"version": dataset_version}
    flag, result = session.do_request(path=url_path, json_data=json_data, method="POST")
    return (flag, result["data"]["freezen_id"]) if flag else (flag, result)


def types(session):
    """ 数据集类型列表

    :param session: app/user session
    :return: 数据集类型列表
    """
    url_path = "dataset/types"
    flag, result = session.do_request(url_path)
    return (flag, result["data"]["data_types"]) if flag else (flag, result)


def signatures(session, dataset_id, dataset_version=0):
    """获取数据集文件的预先签名列表

    :param session:
    :param dataset_id:
    :param dataset_version:
    :return:
    """
    url_path = "dataset/{}/signatures".format(dataset_id)
    json_data = {"version": dataset_version}
    flag, result = session.do_request(path=url_path, json_data=json_data)
    return (flag, result["data"]) if flag else (flag, result)


def download(session, dataset_id: int, target_path: str, dataset_version=0, **kwargs):
    """ 下载一个数据集到本地的某处

    :param session: user/app session
    :param dataset_id: 数据集ID（in DataCenter）
    :param target_path: 用于保存数据集的本地目录
    :param dataset_version: 数据集版本
    :param kwargs: extra special info
    :return: result
    """

    def download_small(url, local_path):
        """ 下载小文件

        :param url: 文件URL
        :param local_path: 下载文件的本地保存地址
        :return:
        """
        pass

    # 获取数据集keys
    flag, f_keys = keys(session=session, dataset_id=dataset_id, dataset_version=dataset_version)
    if not flag:
        return flag, f_keys

    # 获取URL签名
    flag, signs = signatures(session=session, dataset_id=dataset_id,
                             dataset_version=dataset_version)
    if not flag:
        return flag, signs
    # 通过size信息划分为小文件和大文件
    small = []
    big = []

    # 小文件使用简单Downloader多线程下载 （worker=os.cpu_count() * 5）
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url_file in small:
            futures.append(executor.submit(download_small, url="", local_path=""))
        for future in concurrent.futures.as_completed(futures):
            print(future.result())
    # 小文件通过特殊的Downloader串行下载（Downloader内部是多线/多chunk下载）
    for url_file in big:
        Downloader(url="").run()


def upload(session, local_path, **kwargs):
    """ 从本地上传一个数据集

    :param session: user/app session
    :param local_path: 数据集的本地地址（单文件为文件路径，多文件为文件夹路径）
    :param kwargs: extra info
    :return:
    """
    # 创建数据集记录
