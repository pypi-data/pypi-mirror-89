"""分子数据相关操作
by tacey@XARC on 20-10-30
"""


def simple_detail(session, molecule_id):
    """分子摘要

    :param session: app/user session
    :param molecule_id: 分子ID
    :return: 分子摘要信息
    """
    url_path = "molecule/{}".format(molecule_id)
    flag, result = session.do_request(url_path)
    return (flag, result["data"]) if flag else (flag, result)


def detail(session, molecule_id, section):
    """fully detail info of one molecule

    :param session: app/user session
    :param molecule_id: 分子ID
    :param section: ("summary", "identifiers", "properties", "activity", "link", "vendor")其中之一
    :return: 分子某个section的详情
    """
    url_path = "molecule/{}/detail/{}".format(molecule_id, section)
    sections = ("summary", "identifiers", "properties", "activity", "link", "vendor")
    assert section in sections, "section必须为 {} 其中之一".format(str(sections))
    flag, result = session.do_request(url_path)
    return (flag, result["data"]) if flag else (flag, result)


def query(session, query_type, query_value, page=0, limit=20):
    """通过分子类型查询分子

    :param session: app/user session
    :param query_type: 查询字段，("sub", "sim", "exact", "synonym", "cas")其中之一
    :param query_value: 查询值
    :param page: 第几页(以0为基，缺省为0)
    :param limit: 单页数据量 （缺省为20）
    :return: 分子列表
    """
    url_path = "molecule/{}/{}".format(query_type, query_value)
    query_types = ("sub", "sim", "exact", "synonym", "cas")
    assert query_type in query_types
    json_data = {"limit": limit, "page": page}
    flag, result = session.do_request(url_path, json_data=json_data, method="GET")
    return (flag, result["data"]) if flag else (flag, result)
