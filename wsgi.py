from controller import urls
from controller import view_404
from setting import OK
from wavy.utilities import middlewares, get_data_method, Request


class Application:

    def __init__(self, urls, middlewares):
        self.urls = urls
        self.middlewares = middlewares

    def __call__(self, environ, start_response):
        """
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        """
        # сначала в функцию start_response передаем код ответа и заголовки
        # pprint(environ)
        url = environ['PATH_INFO']
        request = Request()

        # Проверка на / в конце урла, если нет добовляем
        if not url.endswith('/') and url != '/':
            url += '/'

        for item in self.middlewares:
            item(request)

        # получаем метод и распарсеные даные параметра запроса
        method, request_params = get_data_method(environ)

        if url in self.urls:
            view = self.urls[url]
            response = view(request, method, request_params)
        else:
            response = view_404(request)
        start_response(response.code, [('Content-Type', 'text/html')])
        # возвращаем тело ответа в виде списка из bite
        return response.body


class LoggingApplication(Application):

    def __init__(self, urls, middlewares):
        super().__init__(urls, middlewares)
        self.application = Application(urls, middlewares)

    def __call__(self, environ, start_response):
        print(f'тип запроса {environ["REQUEST_METHOD"]} параметры {environ["QUERY_STRING"]}')
        return self.application(environ, start_response)


class FakeApplication:

    def __call__(self, environ, start_response):
        start_response = (OK, [('Content-Type', 'text/html')])
        return [b'Hello from Fake']


application = Application(urls, middlewares)
logging_application = LoggingApplication(urls, middlewares)
fake_application = FakeApplication()
