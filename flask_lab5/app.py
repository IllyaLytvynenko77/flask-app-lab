import logging
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf.csrf import CSRFProtect
from config import Config
from forms import ContactForm
from products.routes import products_bp

app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)

# Налаштування логування контактної форми у файл contact.log
contact_logger = logging.getLogger('contact_logger')
contact_logger.setLevel(logging.INFO)
if not contact_logger.handlers:
    file_handler = logging.FileHandler('contact.log', encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    contact_logger.addHandler(file_handler)

# Реєстрація блюпринта products
app.register_blueprint(products_bp)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            log_entry = (
                f"Name: {form.name.data} | Email: {form.email.data} | "
                f"Phone: {form.phone.data} | Subject: {form.subject.data} | "
                f"Message: {form.message.data}"
            )
            contact_logger.info(log_entry)
            flash('Дані успішно відправлено та записано у лог-файл!', 'success')
            # Патерн Post/Redirect/Get (PRG)
            return redirect(url_for('contact'))
        except Exception as exc:
            contact_logger.error(f"Помилка при збереженні даних форми: {exc}")
            flash('Сталася помилка під час запису даних користувача.', 'danger')
    elif request.method == 'POST':
        flash('Не вдалося відправити форму. Перевірте правильність введених даних.', 'danger')

    return render_template('contact.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
