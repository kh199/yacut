import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import LINK_SYMBOLS, get_unique_short_id


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    short_link = data.get('custom_id')
    if short_link:
        if URLMap.query.filter_by(short=short_link).first():
            raise InvalidAPIUsage(f'Имя "{short_link}" уже занято.')
        if len(short_link) > 16 or not re.match(LINK_SYMBOLS, short_link):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    else:
        short_link = get_unique_short_id()
    cut_link = URLMap(
        original=data['url'],
        short=short_link
    )
    db.session.add(cut_link)
    db.session.commit()

    return jsonify(cut_link.to_dict()), 201
