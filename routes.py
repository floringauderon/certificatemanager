# routes.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import app, db, forms, models
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import sendgrid
from sendgrid.helpers.mail import Mail

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    certificates = models.Certificate.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', certificates=certificates, username=current_user.email)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        try:
            user = models.User(email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash('I am so sorry, Registration failed. Please try again.', 'danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/add_certificate', methods=['GET', 'POST'])
@login_required
def add_certificate():
    form = forms.CertificateForm()
    if form.validate_on_submit():

        cert = models.Certificate(
            common_name=form.common_name.data,
            creation_date=form.creation_date.data,
            valid_to_date=form.valid_to_date.data,
            comments=form.comments.data,
            user_id=current_user.id,
            zip_password=form.zip_password.data,
            pfx_password=form.pfx_password.data,
        )
        db.session.add(cert)
        db.session.commit()
        flash('Damn, Certificate added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_certificate.html', form=form)

@app.route('/certificate/<int:id>', methods=['GET', 'POST'])
@login_required
def certificate(id):
    cert = models.Certificate.query.get_or_404(id)

    if cert.user_id != current_user.id:
        flash("You do not have permission to view this certificate.", "danger")
        return redirect(url_for('index'))

    form = forms.CertificateForm(obj=cert)

    if form.validate_on_submit():
        cert.common_name = form.common_name.data
        cert.creation_date = form.creation_date.data
        cert.valid_to_date = form.valid_to_date.data
        cert.comments = form.comments.data
        cert.zip_password = form.zip_password.data,
        cert.pfx_password = form.pfx_password.data,

        db.session.commit()
        flash('Damn, Certificate updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('certificate.html', form=form, certificate=cert)

@app.route('/delete_certificate/<int:id>')
@login_required
def delete_certificate(id):
    cert = models.Certificate.query.get_or_404(id)

    if cert.user_id != current_user.id:
        flash("No no my man! You do not have permission to delete this certificate.", "danger")
        return redirect(url_for('index'))

    db.session.delete(cert)
    db.session.commit()
    flash('Aaaand he gone - Certificate deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
