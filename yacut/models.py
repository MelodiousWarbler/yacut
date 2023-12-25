import random
from datetime import datetime

from flask import url_for

from yacut import db
from .const import (
    ORIGINAL_LENGTH, LEN_OF_SHORT,
    SHORT_LENGTH,
    PATTERN_FOR_SHORT
)
from .error_handlers import InvalidAPIUsage


REDIRECT_VIEW = 'redirect_view'
UNIQUE_SHORT_MESSAGE = 'Предложенный вариант короткой ссылки уже существует.'
ID_ERROR_MESSAGE = 'Указанный id не найден'
PATTERN_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
ITERATIONS = 10


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_VIEW,
                short=self.short,
                _external=True
            )
        )

    @staticmethod
    def save(original, short):
        if short:
            if len(short) > SHORT_LENGTH:
                raise InvalidAPIUsage(PATTERN_MESSAGE)
            if not URLMap.check_unique_short(short):
                raise InvalidAPIUsage(UNIQUE_SHORT_MESSAGE)
        else:
            short = URLMap.get_unique_short()
        url = URLMap(
            original=original,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        return url

    @staticmethod
    def check_unique_short(short_link):
        return not URLMap.query.filter_by(short=short_link).first()

    @staticmethod
    def get_unique_short():
        for _ in range(ITERATIONS):
            short_link = ''.join(random.choices(PATTERN_FOR_SHORT, k=LEN_OF_SHORT))
            if not URLMap.check_unique_short(short_link):
                raise InvalidAPIUsage(ID_ERROR_MESSAGE)
        return short_link

    @staticmethod
    def get_object(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404()
