from flask import flash, redirect, render_template

from . import app, db
from .forms import CutForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = CutForm()
    if form.validate_on_submit():
        short_link = form.custom_id.data
        if URLMap.query.filter_by(short=short_link).first():
            flash(f'Имя {short_link} уже занято!')
            return render_template('yacut.html', form=form)
        if not short_link:
            short_link = get_unique_short_id()
        cut_link = URLMap(
            original=form.original_link.data,
            short=short_link
        )
        db.session.add(cut_link)
        db.session.commit()
        return render_template('link.html', form=form, short=short_link)
    return render_template('yacut.html', form=form)


@app.route('/<short>')
def redirect_view(short):
    link = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(link.original)
