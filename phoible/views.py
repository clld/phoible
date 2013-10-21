from pyramid.view import view_config


@view_config(route_name='history', renderer='history.mako')
def history(req):
    return {}
