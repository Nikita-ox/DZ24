import os

from flask import Flask, request, Response
import re
from typing import Iterator, List, Any, Optional

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


# http://127.0.0.1:25000/perform_query?cmd1=1&value1=1&cmd2=2&value2=2&file_name=apache_logs.txt
@app.route("/perform_query", methods=['GET', 'POST'])
def perform_query() -> Response:
    cmd1 = request.args.get('cmd1')
    value1 = request.args.get('value1')
    cmd2 = request.args.get('cmd2')
    value2 = request.args.get('value2')
    file_name = request.args.get('file_name')

    if None in [cmd1, value1]:
        # return "Введите значения параметров cmd1, value1, cmd2, value2", 400
        return app.response_class("Введите значения параметров cmd1, value1, cmd2, value2", content_type="text/plain")
    try:
        # print(DATA_DIR + '/' + file_name)
        with open(DATA_DIR + '/' + str(file_name), 'r') as file:
            data = file.readlines()
    except Exception:
        # return f'Файл {file_name} не был найден', 400
        return app.response_class(f'Файл {file_name} не был найден', content_type="text/plain")

    with open(DATA_DIR + '/' + str(file_name), 'r') as file:
        data = [x for x in file.readlines()]
        # print(data[:2])
        res = func_response(str(cmd1), str(value1), list(data))
        # print(list(res))
        if cmd2 and value2:
            res = func_response(str(cmd2), str(value2), list(res))
            # print(type(res))
        # res = "\n".join(res)
        # print(res)
    return app.response_class("\n".join(res), content_type="text/plain")


def func_response(cmd: str, value: str, data: list) -> List[Any]:
    if cmd == 'filter':  # выбираем те строки, где встречается value
        res = filter(lambda x: value in x, data)
        return list(res)

    elif cmd == 'map':  # делим строку в список по пробелам. Выводим нужный индекс каждой строки - как бы колонку
        # value = int(value)
        # res = [x.split()[int(value)] for x in data]
        return list(x.split()[int(value)] for x in data)

    elif cmd == 'unique':  # множество исключает одинаковые строки
        return list(set(data))

    elif cmd == 'sort':  # сортируем список строк.
        if value == "desc":
            return sorted(data, reverse=True)
        elif value == "asc":
            return sorted(data, reverse=False)

    elif cmd == 'limit':  # ограничиваем показ списка строк срезом от 0 и "до"
        # value = int(value)
        return list(data)[:int(value)]

    elif cmd == 'regex':  # выводим строки с регулярным выражением
        regex = re.compile(value)
        # res = list(filter(lambda x: regex.search(x), data))
        # print(type(res))
        # if len(res) == 0:
        #     return [f"Регулярное выражение {value} не нашлось"]
        return list(filter(lambda x: regex.search(x), data))

    return ["Нет такой команды"]


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=25000, debug=True)
