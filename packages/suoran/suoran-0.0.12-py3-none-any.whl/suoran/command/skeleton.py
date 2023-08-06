import os
import io
import base64
from os.path import basename
import zipfile
from ran import pkg
from ..common import list_files


def zip(folder):
    '''
    压缩。
    '''

    d = os.path.dirname(os.path.dirname(__file__))
    t = os.path.join(d, 'asset', 'skeleton.py')

    def filter(name, path):
        if path.find('__pycache__') >= 0:
            return False
        suffix = os.path.splitext(path)[1]
        if suffix in ['.db', '.db-shm', '.db-wal', '.log']:
            return False
        basename = os.path.basename(path)
        if basename in ['.env']:
            return False
        return True
    pkg.save(t, filter=filter, zip=folder)


def unzip(folder):
    '''
    解压框架。
    '''

    pkg.cast('suoran.asset.skeleton', 'zip', folder)
