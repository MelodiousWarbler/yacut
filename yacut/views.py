from flask import flash, redirect, render_template

from . import app
from .const import INDEX, UNIQUE_SHORT_MSG
from .error_handlers import InvalidAPIUsage
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template(INDEX, form=form)
    custom_id = form.custom_id.data
    url_map = URLMap(
        original=form.original_link.data,
        short=custom_id
    )
    try:
        url_map.save()
    except InvalidAPIUsage:
        flash(UNIQUE_SHORT_MSG)
    return render_template(INDEX, url=url_map, form=form)


@app.route('/<string:short_id>')
def redirect_view(short_id):
    object_in_db = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(object_in_db.original)
