import pytest

pytest_plugins = ['clld']


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get', '/void.md.txt'),
        ('get_html', '/contributors/GM'),
        ('get_dt', '/parameters'),
        ('get_dt', '/parameters?sSearch_1=>100&iSortingCols=1&iSortCol_0=1'),
        ('get_html', '/parameters'),
        ('get_html', '/parameters/5AE9663626770D1D4B97AAE5769AB83C'),
        ('get_xml', '/parameters/5AE9663626770D1D4B97AAE5769AB83C.rdf'),
        ('get_json', '/parameters/5AE9663626770D1D4B97AAE5769AB83C.geojson'),
        ('get_dt', '/inventories'),
        ('get_dt', '/inventories?sSearch_1=>20&iSortingCols=1&iSortCol_0=1'),
        ('get_dt', '/inventories?sSearch_5=a&iSortingCols=1&iSortCol_0=5'),
        ('get_dt', '/inventories?sSearch_6=a&iSortingCols=1&iSortCol_0=6'),
        ('get_html', '/inventories'),
        ('get_html', '/inventories/view/432'),
        ('get_xml', '/inventories/view/432.rdf'),
        ('get', '/inventories/view/432.md.ris'),
        ('get', '/inventories/view/432.md.bib'),
        ('get', '/inventories/view/432.md.html'),
        ('get_dt', '/languages'),
        ('get_dt', '/languages?sSearch_2=a&iSortingCols=1&iSortCol_0=2'),
        ('get_dt', '/languages?sSearch_3=a&iSortingCols=1&iSortCol_0=3'),
        ('get_html', '/languages'),
        ('get_json', '/languages.geojson'),
        ('get', '/languages/cogu1240'),
        ('get_xml', '/languages/cogu1240.rdf'),
        ('get_dt', '/values'),
        ('get_dt', '/values?parameter=5AE9663626770D1D4B97AAE5769AB83C'),
        ('get_dt', '/values?parameter=5AE9663626770D1D4B97AAE5769AB83C&sSearch_0=a&iSortingCols=1&iSortCol_0=0'),
        ('get_dt', '/values?contribution=1003&sSearch_0=a&iSortingCols=1&iSortCol_0=0'),
        ('get_html', '/sources/saphon'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)


def test_redirect(app):
    app.get('/parameters/1', status=301)
    app.get('/parameters/0', status=404)
    app.get('/languages/mij', status=301)
