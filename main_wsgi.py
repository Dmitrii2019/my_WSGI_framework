from my_wsgl.urls import urls
from my_wsgl.controller import view_404, Request, secret_middleware


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
        if url[-1] != '/' and len(url) > 1:
            url += '/'

        for item in self.middlewares:
            item(request)

        if url in self.urls:
            view = self.urls[url]
            response = view(request)
        else:
            response = view_404(request)
        start_response(response.code, [('Content-Type', 'text/html')])
        # возвращаем тело ответа в виде списка из bite
        return response.body


middlewares = [
    secret_middleware,
]
application = Application(urls, middlewares)
