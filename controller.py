from my_wsgl.setting import OK, NOT_FOUND
from my_wsgl.template_engine import render


class Response:
    def __init__(self, code, body):
        self.code = code
        self.body = body


class Request:
    def __init__(self, datas=None):
        self.datas = datas or {}


def main_view(request):
    data = request.datas.get('data', None)
    title = 'Главна'
    content = 'Наполнение страницы текстом Главна'
    renders = render('authors.html', object_list=[{'title': title}, {'content': content}, {'data': data}])
    return Response(OK, [renders.encode(encoding='utf-8')])


def about_view(request):
    data = request.datas.get('data', None)
    title = 'О нас'
    content = 'Наполнение страницы текстом О Нас'
    renders = render('authors.html', object_list=[{'title': title}, {'content': content}, {'data': data}])
    return Response(OK, [renders.encode(encoding='utf-8')])


def view_404(request):
    title = 'Not_Found'
    content = 'Не найдено'
    renders = render('authors.html', object_list=[{'title': title}, {'content': content}])
    return Response(NOT_FOUND, [renders.encode(encoding='utf-8')])


def secret_middleware(request):
    request.datas['data'] = 'Этот front controller'
