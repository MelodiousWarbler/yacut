import re
from http import HTTPStatus

from flask import flash, jsonify, request, url_for

from . import app
from .const import PATTERN, SHORT_LENGTH
from .error_handlers import InvalidAPIUsage
from .models import URLMap


ID_NOT_FOUND = 'Указанный id не найден'
NO_DATA = 'Отсутствует тело запроса'
NO_URL = '"url" является обязательным полем!'
WRONG_SHORT = 'Указано недопустимое имя для короткой ссылки'
SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
NO_LINK = 'Ссылка не создана'


@app.route('/api/id/<short>/', methods=['GET'])
def get_url(short):
    url_map_obj = URLMap.get_object(short)
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
    short = data.get('custom_id')
    if short:
        if not re.search(
            PATTERN,
            short
        ) or len(short) > SHORT_LENGTH:
            raise InvalidAPIUsage(WRONG_SHORT)
        if URLMap.query.filter_by(short=short).first():
            raise InvalidAPIUsage(SHORT_EXISTS)
    try:
        url = URLMap.save(
            data.get('url'), data.get('custom_id')
        )
        return jsonify(url.to_dict()), HTTPStatus.CREATED
    except InvalidAPIUsage:
        flash(NO_LINK)