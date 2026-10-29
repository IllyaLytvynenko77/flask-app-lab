from flask import request, redirect, url_for, render_template, flash
from . import app


@app.route('/')
def resume():
    return render_template('resume.html', title='Резюме')


@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template('homepage.html', title='Головна', agent=agent)


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form.get('name', '')
        flash(f'Дякуємо, {name}! Повідомлення отримано (це форма-заглушка, реальної відправки немає).', 'success')
        return redirect(url_for('contacts'))
    return render_template('contacts.html', title='Контакти')
