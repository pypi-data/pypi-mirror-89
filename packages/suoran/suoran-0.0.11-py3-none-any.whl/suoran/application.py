from pkgutil import iter_modules
from importlib import import_module
from sanic import Sanic
from .common import *


class Application(Sanic):
    '''
    应用类
    '''

    def __init__(self, **kws):
        '''
        初始化。
        '''

        super().__init__(
            name=kws.get('name', None),
            router=kws.get('router', None),
            error_handler=kws.get('error_handler', None),
            load_env=kws.get('load_env', False),
            request_class=kws.get('request_class', None),
            strict_slashes=kws.get('strict_slashes', True),
            log_config=kws.get('log_config', None),
            configure_logging=kws.get('configure_logging', True)
        )

    def apply(self, **kws):
        '''
        应用启动。
        '''

        self.run(
            host=kws.get('host', '0.0.0.0'),
            port=kws.get('port', 8000),
        )

    def control(self, module, deep=True):
        '''
        加载控制器。
        '''

        # 如果传模块名则加载。
        if isinstance(module, str):
            module = import_module(module)

        # 加载路由。
        if hasattr(module, '___router___'):
            router = getattr(module, '___router___')
            router.route(self)

        # 是否深入解析。
        name = module.__name__
        if deep and module.__loader__.is_package(name):
            for _, child, _ in iter_modules(module.__path__):
                mn = f'{name}.{child}'
                m = import_module(mn)
                self.control(m, deep)
