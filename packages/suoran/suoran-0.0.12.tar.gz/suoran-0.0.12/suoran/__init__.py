from dotenv import load_dotenv
from .application import *
from .config import load_configuration


def new_application(**kws):
    '''
    新建应用。
    '''

    load_dotenv(verbose=False, override=True)
    cmn = kws.get('config_module', 'config')
    config = load_configuration(cmn)
    appcnf = config['app']
    appcnf['log_config'] = config['log']
    app = Application(**{**appcnf, **kws})
    app.config.SUORAN = config
    return app
