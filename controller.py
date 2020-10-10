from setting import OK, NOT_FOUND
from templates.template import render
from utilities import Response


def main_view(request, method, request_params):
    data = request.datas.get('data', None)
    title = 'Главна'
    content = 'Текс'
    renders = render('index.html', object_list=[{'title': title}, {'content': content}, {'data': data}])
    return Response(OK, [renders])


def about_view(request, method, request_params):
    data = request.datas.get('data', None)
    title = 'О нас'
    content = 'Текс'
    renders = render('authors.html', object_list=[{'title': title}, {'content': content}, {'data': data}])
    return Response(OK, [renders], )


def contact_view(request, method, request_params):
    if method == 'POST':
        print(request_params) # работаем с введенными параметрами
    data = request.datas.get('data', None)
    title = 'Контакты'
    content = f'это {method} запрос c параметрами = {request_params}'
    renders = render('contact.html', object_list=[{'title': title}, {'content': content}, {'data': data}])
    return Response(OK, [renders])


def view_404(request):
    title = 'Not_Found'
    content = 'Не найдено'
    renders = render('authors.html', object_list=[{'title': title}, {'content': content}])
    return Response(NOT_FOUND, [renders])
