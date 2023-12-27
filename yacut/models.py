import random
import re
from datetime import datetime

from flask import url_for

from yacut import db
from .const import (
    ORIGINAL_LENGTH, LEN_OF_SHORT,
    SHORT_LENGTH, REGEX_FOR_SHORT,
    PATTERN_FOR_SHORT, REDIRECT_VIEW
)


ID_ERROR_MESSAGE = 'Указанный id не найден'
ITERATIONS = 10
WRONG_SHORT = 'Указано недопустимое имя для короткой ссылки'
SHORT_EXISTS = 'Предложенный вариант короткой ссылки уже существует.'
TOO_LONG_ORIGINAL = 'Слишком длинная ссылка'


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
    def create(original, short, validate=False):
        if short:
            if validate:
                if len(short) > SHORT_LENGTH or not re.search(
                    REGEX_FOR_SHORT,
                    short
                ):
                    raise RuntimeError(WRONG_SHORT)
            if URLMap.get(short):
                raise RuntimeError(SHORT_EXISTS)
        else:
            short = URLMap.get_unique_short()
        if len(original) > ORIGINAL_LENGTH:
            raise RuntimeError(TOO_LONG_ORIGINAL)
        url = URLMap(
            original=original,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        return url

    @staticmethod
    def get_unique_short():
        for _ in range(ITERATIONS):
            short = ''.join(random.choices(PATTERN_FOR_SHORT, k=LEN_OF_SHORT))
            if URLMap.get(short) is None:
                return short
        raise RuntimeError(ID_ERROR_MESSAGE)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404()
