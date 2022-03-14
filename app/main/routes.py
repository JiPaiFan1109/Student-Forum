from flask import render_template, flash, redirect, url_for, session

from . import main
from .forms import NameForm
from .. import db
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form = form, name = session.get('name'),
                           known = session.get('known', False))