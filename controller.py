from setting import OK, NOT_FOUND
from template_engine import render
from utilities import Request, Response


def main_view(request, method, request_params):
    data = request.datas.get('data', None)
    title = 'Главна'
    content = f'это {method} запрос c параметрами = {request_params}'
    renders = render('templates/authors.html', object_list=[{'title': title}, {'content': content}, {'data': data}])
    return Response(OK, [renders])


def about_view(request, method, request_params):
    data = request.datas.get('data', None)
    title = 'О нас'
    content = f'это {method} запрос c параметрами = {request_params}'
    renders = render('templates/authors.html', object_list=[{'title': title}, {'content': content}, {'data': data}])
    return Response(OK, [renders])


def contact_view(request, method, request_params):
    data = request.datas.get('data', None)
    title = 'Контакты'
    content = f'это {method} запрос c параметрами = {request_params}'
    renders = render('templates/contact.html', object_list=[{'title': title}, {'content': content}, {'data': data}])
    return Response(OK, [renders])


def view_404(request):
    title = 'Not_Found'
    content = 'Не найдено'
    renders = render('templates/authors.html', object_list=[{'title': title}, {'content': content}])
    return Response(NOT_FOUND, [renders])
