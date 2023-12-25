from flask import flash, redirect, render_template, url_for

from . import app
from .error_handlers import InvalidAPIUsage
from .forms import URLMapForm
from .models import URLMap


UNIQUE_SHORT_MASSAGE = 'Предложенный вариант короткой ссылки уже существует.'
INDEX = 'index.html'
REDIRECT_VIEW = 'redirect_view'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template(INDEX, form=form)
    try:
        url = URLMap.save(original=form.original_link.data, short=form.custom_id.data)
        render=url_for(REDIRECT_VIEW, short=url.short, _external=True)
        return render_template(
            INDEX,
            url=render,
            form=form
        )
    except InvalidAPIUsage:
        flash(UNIQUE_SHORT_MASSAGE)
        return render_template(INDEX, form=form)


@app.route('/<string:short>')
def redirect_view(short):
    return redirect(URLMap.get_or_404(short).original)
