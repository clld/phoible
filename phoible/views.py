from pyramid.view import view_config

faq_page = None
conventions_page = None
with open('phoible/static/faq_with_indexes.html', 'r') as file:
    faq_page = file.read()
with open('phoible/static/conventions.html', 'r') as file:
    conventions_page = file.read().replace('\n', '')


@view_config(route_name='faq', renderer='faq.mako')
def faq_view(request):
    request.faq = True
    return {'content': faq_page}


@view_config(route_name='conventions', renderer='conventions.mako')
def conventions_view(request):
    request.conventions = True
    return {'content': conventions_page}
