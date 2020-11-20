# Код ответа (состояния) HTTP
import os
from pathlib import Path

OK = '200 ok'
NOT_FOUND = '404 Not Found'
REDIRECT = '302 Moved Temporarily'

# Кодировка проекта
ENCODING = 'utf-8'

# Название базы данных
base_name = 'database.db'


# путь к базе данных
def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent/base_name


# Создание базы в корне проекта
BASE = get_project_root()
