import random
import re

from datetime import datetime

from flask import url_for

from yacut import db

from .const import (
    LABELS, ORIGINAL_LENGTH,
    SHORT_LENGTH, PATTERN,
    PATTERN_FOR_GEN_URL,
    REDIRECT_VIEW, UNIQUE_SHORT_MSG
)
from .error_handlers import InvalidAPIUsage


ID_ERR_MSG = 'Указанный id не найден'
PATTERN_MSG = 'Указано недопустимое имя для короткой ссылки'


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
                short_id=self.short,
                _external=True
            )
        )

    @staticmethod
    def from_dict(data):
        instance = URLMap()
        for field_key, field_item in LABELS.items():
            if field_item in data:
                setattr(instance, field_key, data[field_item])
        return instance

    def save(self):
        if self.short:
            if not check_unique_short_id(self.short):
                raise InvalidAPIUsage(UNIQUE_SHORT_MSG)
            elif not re.match(PATTERN, self.short):
                raise InvalidAPIUsage(PATTERN_MSG)
        else:
            self.short = get_unique_short_id()
        db.session.add(self)
        db.session.commit()


def check_unique_short_id(short_link):
    return not URLMap.query.filter_by(short=short_link).first()


def get_unique_short_id():
    short_link = ''.join(random.choices(PATTERN_FOR_GEN_URL, k=6))
    if not check_unique_short_id(short_link):
        raise InvalidAPIUsage(ID_ERR_MSG)
    return short_link
