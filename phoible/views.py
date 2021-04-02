from pyramid.view import view_config


@view_config(route_name='faq', renderer='templates/faq.mako')
def faq_view(request):
    request.faq = True
    return {}


@view_config(route_name='conventions', renderer='templates/conventions.mako')
def conventions_view(request):
    request.conventions = True
    return {}
