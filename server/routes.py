from server.handlers import index, consume, produce, list_channels, metrics

def setup_routes(app):
    app.router.add_get('/channel/{channel_id}/index.html', index)
    app.router.add_get('/channel/{channel_id}/consume', consume)
    app.router.add_get('/channel/{channel_id}/produce', produce)
    app.router.add_get('/channels', list_channels)  # New endpoint for channel discovery
    app.router.add_get('/metrics', metrics)  # New endpoint for metrics
    app.router.add_static('/static/', path=str(app['config'].STATIC_ROOT), name='static')
