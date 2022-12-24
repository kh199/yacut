from flask import flash, redirect, render_template

from . import app, db
from .forms import CutForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = CutForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if short:
            if URLMap.query.filter_by(short=short).first():
                flash(f'Имя {short} уже занято!')
                return render_template('yacut.html', form=form)
            cut_link = URLMap(
                original=form.original_link.data,
                short=form.custom_id.data
            )
            db.session.add(cut_link)
            db.session.commit()
            return render_template('link.html', form=form, short=short)
        else:
            generated = get_unique_short_id()
            cut_link = URLMap(
                original=form.original_link.data,
                short=generated
            )
            db.session.add(cut_link)
            db.session.commit()
            return render_template('link.html', form=form, short=generated)

    return render_template('yacut.html', form=form)


@app.route('/<short>')
def redirect_view(short):
    link = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(link.original)
