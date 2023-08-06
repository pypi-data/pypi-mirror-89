"""数据工具
by tacey@XARC on 20-10-30
"""


def smiles2svg(session, smiles: str):
    """SMILES转SVG

    :param session: user/app session
    :param smiles: SMILES字符串
    :return:

    使用样例::

        from datacenter.datacenter import DataCenterSession
        from datacenter.tools import smiles2svg
        session = DataCenterSession()
        print(smiles2svg(session=session,smiles="SMILES-STR"))
    """
    url_path = "data_tools/smiles_to_svg/{}".format(smiles)
    flag, result = session.do_request(path=url_path, json_data=None, method="GET")
    return (flag, result["data"]["svg"]) if flag else (flag, result)


def smiles2sdf(session, smiles):
    """SMILES转SDF

    :param session: user/app session
    :param smiles: SMILES字符串
    :return:

    使用样例::

        from datacenter.datacenter import DataCenterSession
        from datacenter.tools import smiles2sdf
        session = DataCenterSession()
        print(smiles2sdf(session=session,smiles="SMILES-STR"))
    """
    url_path = "data_tools/smiles_to_sdf/{}".format(smiles)
    flag, result = session.do_request(path=url_path, json_data=None, method="GET")
    return (flag, result["data"]["sdf"]) if flag else (flag, result)
