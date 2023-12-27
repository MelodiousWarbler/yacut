from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


ID_NOT_FOUND = 'Указанный id не найден'
NO_DATA = 'Отсутствует тело запроса'
NO_URL = '"url" является обязательным полем!'
NO_LINK = 'Ссылка не создана'


@app.route('/api/id/<short>/', methods=['GET'])
def get_url(short):
    url_map_obj = URLMap.get(short)
    if url_map_obj is None:
        raise InvalidAPIUsage(ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map_obj.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json()
    if not isinstance(data, dict):
        raise InvalidAPIUsage(NO_DATA)
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL)
    try:
        return jsonify(
            URLMap.create(
                data['url'],
                data.get('custom_id'),
                True
            ).to_dict()
        ), HTTPStatus.CREATED
    except (RuntimeError) as error:
        raise InvalidAPIUsage(str(error))
