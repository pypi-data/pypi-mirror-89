from pkgutil import iter_modules
from importlib import import_module

def load_configuration(name):
    '''
    加载配置。
    '''

    result = {}
    module = import_module(name)
    for _, child, _ in iter_modules(module.__path__):
        cn = f'{name}.{child}'
        cm = import_module(cn)
        vs = {}
        for k in dir(cm):
            if k[0] != '_':
                vs[k] = getattr(cm, k)
        result[child] = vs
    return result