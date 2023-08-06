from tortoise import Tortoise


async def init(app, **kws):
    '''
    初始化。
    '''

    await Tortoise.init(
        config=app.config.SUORAN['database']
    )
    if kws.get('initial', False):
        await Tortoise.generate_schemas()


async def exit(app):
    '''
    回收。
    '''

    await Tortoise.close_connections()
