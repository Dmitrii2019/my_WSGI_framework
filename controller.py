from decorators.debug import debug
from wavy.setting import OK, NOT_FOUND, REDIRECT
from wavy.template import render
from wavy.utilities import Response
from models import TrainingSite

site = TrainingSite()


@debug
def main_view(request, method, request_params):
    title = 'Главна'
    return Response(OK, [render('index.html', objects_list=[{'title': title}])])


def registration_view(request, method, request_params):
    title = 'Регистрации'
    if method == 'POST':
        type_ = request_params["type_"]
        user = request_params["usrnm"]
        email = request_params["email"]
        psw = request_params["psw"]
        data = site.create_user(type_, user, email, psw)
        site.user.append(data)
    return Response(OK, [render('registration.html', objects_list=[{'title': title}])])


def users_list(request, method, request_params):
    return Response(OK, [render('users-list.html', objects_list=site.user)])


def students_list(request, method, request_params):
    return Response(OK, [render('students-list.html', objects_list=site.user)])


def teachers_list(request, method, request_params):
    return Response(OK, [render('teachers-list.html', objects_list=site.user)])


@debug
def create_category_view(request, method, request_params):
    if method == 'POST':
        # метод пост
        data = request_params
        name = data['name']
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)
        site.categories.append(new_category)
        return Response(OK, [render('create-category.html')])
    else:
        categories = site.categories
        return Response(OK, [render('create-category.html', categories=categories)])


@debug
def create_course_view(request, method, request_params):
    if method == 'POST':
        # метод пост
        data = request_params
        name = data['name']
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
            course = site.create_course('record', name, category)
            site.courses.append(course)
        else:
            # редирект
            return Response(REDIRECT, [render('create-category.html')])

        return Response(OK, [render('create-course.html')])
    else:
        categories = site.categories
        return Response(OK, [render('create-course.html', categories=categories)])


@debug
def contact_view(request, method, request_params):
    if method == 'POST':
        print(request_params)  # работаем с введенными параметрами
    data = request.datas.get('data', None)
    title = 'Контакты'
    return Response(OK, [render('contact.html', object_list=[{'title': title}, {'data': data}])])


@debug
def course_list(request, method, request_params):
    return Response(OK, [render('course-list.html', objects_list=site.courses)])


@debug
def copy_course(request, method, request_params):
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return Response(OK, [render('course-list.html', objects_list=site.courses)])


@debug
def category_list(request, method, request_params):
    return Response(OK, [render('category-list.html', objects_list=site.categories)])


@debug
def view_404(request):
    title = 'Not_Found'
    return Response(NOT_FOUND, [render('index.html', objects_list=[{'title': title}])])


urls = {
    '/': main_view,
    '/create-category/': create_category_view,
    '/create-course/': create_course_view,
    '/contact/': contact_view,
    '/category-list/': category_list,
    '/course-list/': course_list,
    '/copy-course/': copy_course,
    '/registration-form/': registration_view,
    '/students-list/': students_list,
    '/teachers-list/': teachers_list,
    '/users-list/': users_list,
}
