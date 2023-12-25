from flask import flash, redirect, render_template, url_for

from . import app
from .const import REDIRECT_VIEW
from .error_handlers import ValidationError
from .forms import URLMapForm
from .models import URLMap


UNIQUE_SHORT_MASSAGE = 'Предложенный вариант короткой ссылки уже существует.'
INDEX = 'index.html'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template(INDEX, form=form)
    try:
        return render_template(
            INDEX,
            url=url_for(
                REDIRECT_VIEW,
                short=URLMap.create(
                    original=form.original_link.data,
                    short=form.custom_id.data
                ).short,
                _external=True
            ),
            form=form
        )
    except ValidationError as error:
        flash(error.message)
        return render_template(INDEX, form=form)


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(URLMap.get_or_404(short).original)
