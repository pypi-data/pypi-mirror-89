"""DataCenter: DataCenter-Service#XARC的API封装SDK"""

from .biology import query_molecule, molecule_detail, molecule_simple_detail, \
    query_target, target_detail, target_simple_detail
from .tools import smiles2sdf, smiles2svg

from .dataset import versions as dataset_versions
from .dataset import download as download_dataset
from .dataset import upload as upload_dataset
from .dataset import freeze as freeze_dataset
from .dataset import unfreeze as unfreeze_dataset
from .dataset import keys as dataset_keys
from .dataset import tree as dataset_tree
from .dataset import query_list as query_dataset
from .dataset import types as dataset_types
from .datacenter import DataCenterSession as Session
from .datacenter import get_user_token
from .datacenter import get_app_token

__author__ = """Tacey Wong"""
__email__ = 'xinyong.wang@xtalpi.com'
__version__ = '0.0.2'

__all__ = ["query_molecule", "molecule_detail", "molecule_simple_detail",
           "query_target", "target_detail", "target_simple_detail",
           "smiles2sdf", "smiles2svg",
           "download_dataset", "upload_dataset", "freeze_dataset", "unfreeze_dataset",
           "dataset_keys", "dataset_tree", "dataset_versions", "dataset_types",
           "query_dataset",
           "Session", "get_app_token", "get_user_token"]
