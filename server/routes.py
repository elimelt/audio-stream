from server.handlers import index, consume, produce, get_metrics

def setup_routes(app):
    app.router.add_get('/channel/{channel_id}/index.html', index)
    app.router.add_get('/channel/{channel_id}/consume', consume)
    app.router.add_get('/channel/{channel_id}/produce', produce)
    app.router.add_get('/metrics', get_metrics)
    app.router.add_static('/static/', path=str(app['config'].STATIC_ROOT), name='static')
