import pytest
import os
from zipfile import ZipFile


@pytest.fixture(scope="session", autouse=True)
def make_zip():
    # Создаём папку 'resources', если её нет
    if not os.path.exists("resources"):
        os.mkdir("resources")

    # Получаем пути к директориям
    current_directory_path = os.path.dirname(__file__)
    resources_directory_path = os.path.join(current_directory_path, "resources")
    tmp_directory_path = os.path.join(current_directory_path, "tmp")
    archive_file = os.path.join(resources_directory_path, "archive.zip")

    # Создаём ZIP-архив
    with ZipFile(archive_file, 'w') as zfile:
        # Рекурсивно обходим все файлы в папке 'tmp'
        for root, dirs, files in os.walk(tmp_directory_path):
            # os.walk функция которая обходит папку tmp root : текущую папку.
            # dirs: Список подпапок в текущей папке.
            # files: Список файлов в текущей папке
            for file in files:
                file_path = os.path.join(root, file)
                # Добавляем файл в архив с именем файла (без пути)
                zfile.write(file_path, os.path.basename(file_path))

    yield  # Фикстура предоставляет значение (в данном случае ничего)

    # Очистка: удаляем созданный ZIP-архив
    if os.path.exists(archive_file):
        os.remove(archive_file)