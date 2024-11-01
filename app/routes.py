from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import Contacts
from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from sqlalchemy.exc import DataError
from flask_paginate import Pagination, get_page_parameter

bp = Blueprint('main', __name__)

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    phone = StringField('Telefon', validators=[DataRequired(), Length(max=20)])
    email = StringField('E-Mail', validators=[DataRequired(), Email(), Length(max=255)])
    address = TextAreaField('Adresse', validators=[DataRequired()])
    submit = SubmitField('Absenden')

@bp.route('/')
def index():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    search = request.args.get('search', '', type=str)
    sort = request.args.get('sort', 'date', type=str)
    direction = request.args.get('direction', 'desc', type=str)
    
    query = Contacts.query
    if search:
        query = query.filter(Contacts.name.contains(search) | Contacts.phone.contains(search) | Contacts.email.contains(search) | Contacts.address.contains(search))
    
    if direction == 'asc':
        query = query.order_by(getattr(Contacts, sort).asc())
    else:
        query = query.order_by(getattr(Contacts, sort).desc())
    
    per_page = 10
    total = query.count()
    contacts_pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    contacts = contacts_pagination.items
    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap4')
    
    return render_template('index.html', contacts=contacts, pagination=pagination, search=search, sort=sort, direction=direction, page=page, total=total)

@bp.route('/add', methods=['GET', 'POST'])
def add_contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contacts(name=form.name.data, phone=form.phone.data, email=form.email.data, address=form.address.data)
        try:
            db.session.add(contact)
            db.session.commit()
            flash('Kontakt erfolgreich hinzugefügt!', 'success')
            return redirect(url_for('main.index'))
        except DataError:
            db.session.rollback()
            flash('Fehler: Daten zu lang für eines der Felder.', 'danger')
    return render_template('add_contact.html', form=form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    contact = Contacts.query.get_or_404(id)
    form = ContactForm(obj=contact)
    if form.validate_on_submit():
        contact.name = form.name.data
        contact.phone = form.phone.data
        contact.email = form.email.data
        contact.address = form.address.data
        try:
            db.session.commit()
            flash('Kontakt erfolgreich aktualisiert!', 'success')
            return redirect(url_for('main.index', sort=request.args.get('sort'), direction=request.args.get('direction'), search=request.args.get('search'), page=request.args.get('page')))
        except DataError:
            db.session.rollback()
            flash('Fehler: Daten zu lang für eines der Felder.', 'danger')
    return render_template('edit_contact.html', form=form, contact=contact)

@bp.route('/delete/<int:id>', methods=['POST'])
def delete_contact(id):
    contact = Contacts.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Kontakt erfolgreich gelöscht!', 'success')
    return redirect(url_for('main.index', sort=request.args.get('sort'), direction=request.args.get('direction'), search=request.args.get('search'), page=request.args.get('page')))