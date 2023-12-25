from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp
from .const import (
    PATTERN,
    SHORT_LENGTH,
    ORIGINAL_LENGTH
)

LONG_LINK = 'Длинная ссылка'
OBLIGATORY_FIELD = 'Обязательное поле'
LINK_IS_NOT_VALID = 'Ссылка не валидна'
YOUR_SHORT_LINK = 'Ваш вариант короткой ссылки'
CREATE = 'Создать'
REGEX_MSG = 'Используйте буквы латинского алфавита и цифры'


class URLMapForm(FlaskForm):
    original_link = URLField(
        LONG_LINK,
        validators=[
            DataRequired(message=OBLIGATORY_FIELD),
            URL(message=LINK_IS_NOT_VALID),
            Length(max=ORIGINAL_LENGTH)
        ]
    )
    custom_id = StringField(
        YOUR_SHORT_LINK,
        validators=[
            Length(max=SHORT_LENGTH),
            Optional(),
            Regexp(
                PATTERN,
                message=REGEX_MSG
            )
        ]
    )
    submit = SubmitField(CREATE)
