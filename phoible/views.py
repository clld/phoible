from pyramid.view import view_config
import os


@view_config(route_name='faq', renderer='faq.mako')
def faq_view(request):
    dir_path = os.path.dirname(__file__)
    faq_file = os.path.join(dir_path, 'static/faq_with_indexes.html')
    with open(faq_file, 'r') as f:
        faq_page = f.read()
    return {'content': faq_page}


@view_config(route_name='conventions', renderer='conventions.mako')
def conventions_view(request):
    dir_path = os.path.dirname(__file__)
    conventions_file = os.path.join(dir_path, 'static/conventions.html')
    with open(conventions_file, 'r') as file:
        conventions_page = file.read().replace('\n', '')
    return {'content': conventions_page}
