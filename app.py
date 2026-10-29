from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'dev-secret-key'


@app.route('/')
def resume():
    return render_template('resume.html', title='Резюме')


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form.get('name', '')
        flash(f'Дякуємо, {name}! Повідомлення отримано (це форма-заглушка, реальної відправки немає).', 'success')
        return redirect(url_for('contacts'))
    return render_template('contacts.html', title='Контакти')


if __name__ == '__main__':
    app.run(debug=True)
