"""
by tacey@XARC on 2020/12/25
"""
from datacenter.internals.downloader import simple_download
from datacenter.internals.uploader import simple_upload


def app_space_upload(session, local_path: str, object_name: str, object_desc: str = ""):
    """向APP-SPACE上传数据 （APP-TOKEN only）

    :param session: app session
    :param local_path: 文件本地地址
    :param object_name: 目的存储对象名
    :param object_desc： 对此对象的描述
    """
    # 申请签名
    url_path = "app_space/signature"
    json_data = {"object_name": object_name, "object_desc": object_desc}
    flag, result = session.do_request(path=url_path, json_data=json_data, method="POST")
    if not flag:
        return flag, result
    url = result["data"]["url"]
    fields = result["data"]["fields"]
    object_name = result["data"]["object_name"]
    # 上传
    simple_upload(url=url, file_path=local_path, fields=fields, file_name=object_name)
    # 汇报上传完成
    url_path = "app_space/confirm"
    json_data = {"object_name": object_name}
    flag, result = session.do_request(path=url_path, json_data=json_data, method="POST")
    return (flag, None) if flag else (flag, result)


def app_space_download_url(session, app_name, object_name):
    """ 获取预签名下载URL

    :param session: app/user session
    :param app_name:
    :param object_name:
    :return: url
    """
    url_path = "app_space/signature"
    json_data = {"object_name": object_name, "app_name": app_name}
    flag, result = session.do_request(path=url_path, json_data=json_data, method="GET")
    return result["url"] if flag else None


def app_space_download(session, app_name, object_name, file_name=None):
    """ 获取预签名下载URL

    :param session: app/user session
    :param app_name:
    :param object_name:
    :param file_name: 本地保存名称
    :return:
    """
    url = app_space_download_url(session, app_name, object_name)
    simple_download(url, file_name=file_name)


def app_space_list(session, page=0, limit=20):
    """ 应用空间数据列表 (APP-TOKEN only)

    :param session: app session
    :param page: 第几页，缺省为0
    :param limit: 单页个数，缺省为20
    :return:
    """
    url_path = "app_space/data"
    json_data = {"page": page, "limit": limit}
    flag, result = session.do_request(path=url_path, json_data=json_data, method="GET")
    return (flag, result["data"]["data_list"]) if flag else (flag, result)
