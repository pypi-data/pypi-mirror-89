"""target(靶)相关操作
by tacey@XARC on 20-10-30
"""


def simple(session, target_id):
    """靶摘要信息

    :param session: app/user session
    :param target_id: 靶ID
    :return: 靶摘要信息
    """
    url_path = "target/{}".format(target_id)
    flag, result = session.do_request(url_path)
    return (flag, result["data"]) if flag else (flag, result)


def detail(session, target_id, section: str):
    """靶详情

    :param session: app/user session
    :param target_id: 靶ID
    :param section: ("summary","function","names","bioassay","activity","sequence",
                    "structure","similar_seq","domain","interaction","reference")其中之一
    :return: 靶某section详情信息
    """
    url_path = "target/{}/detail/{}".format(target_id,section)
    sections = ("summary", "function", "names", "bioassay", "activity", "sequence",
                "structure", "similar_seq", "domain", "interaction", "reference")
    assert section in sections, "section 必须是 {} 其中之一".format(str(sections))
    flag, result = session.do_request(url_path)
    return (flag, result["data"]) if flag else (flag, result)


def query(session, query_type, query_value, page=0, limit=20):
    """通过靶类型查询靶

    :param session: app/user session
    :param query_type:查询字段 ("uniprot", "tname", "sequence")其中之一
    :param query_value:查询值
    :param page: 第几页（以0为基，缺省为0）
    :param limit:单页数据量(缺省为20)
    :return: 靶列表
    """
    url_path = "target/{}/{}".format(query_type,query_value)
    query_types = ("uniprot", "tname", "sequence")
    assert query_type in query_types, "query_type必须是 {}其中之一".format(str(query_types))
    json_data = {"page": page, "limit": limit}
    flag, result = session.do_request(url_path, json_data=json_data, method="GET")
    return (flag, result["data"]) if flag else (flag, result)
