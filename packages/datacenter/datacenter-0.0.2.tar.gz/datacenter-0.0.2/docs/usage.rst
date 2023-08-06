=========
使用说明
=========

To use DataCenter in a project::

    import datacenter

datacenter-sdk的使用一般遵循如下一种模式::

    from datacenter.datacenter import DataCenterSession
    from datacenter import X-DATACENTER-ACTION
    session = DataCenterSession()
    X-DATACENTER-ACTION(session=session,**kwargs)

下面以【获取某个数据集详情】为例子介绍此SDK的使用

Step1:首先是必要的import::

    from datacenter import get_user_token
    from datacenter import Session
    from datacenter import dataset_detail

Step2:然后获取User-Token::

    user_token = get_user_token(user_name="xinyong.wang@xtalpi.com",
                                user_password="123456",
                                auth_by="auth0")

Step3:接着创建datacenter-session::

    session = Session(user_token=user_token)

Step4:最后获取dataset详情::

    flag,dataset_detail = dataset_detail(session=session,
                                         dataset_id=dataset_id)


注意：
    + Step1的get_user_token以来xacs-sdk，而且很多时候这个不是必须要使用的（整个服务流程中可能传递着这个user-token）
    + Step4的flag为执行结果的布尔标识，当flag为False的时候，dataset_detail为出错信息


更多使用详情请参考 `代码注释文档`_ 。

.. _代码注释文档: ./modules.html
