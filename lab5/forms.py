from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message="Поле Name є обов'язковим"),
        Length(min=4, max=10, message="Довжина імені має бути від 4 до 10 символів")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Поле Email є обов'язковим"),
        Email(message="Введіть коректну email-адресу")
    ])
    phone = StringField('Phone', validators=[
        DataRequired(message="Поле Phone є обов'язковим"),
        Regexp(r'^\+380\d{9}$', message="Формат телефону має бути +380XXXXXXXXX (9 цифр після +380)")
    ])
    subject = SelectField('Subject', choices=[
        ('general', 'Загальне питання'),
        ('support', 'Технічна підтримка'),
        ('order', 'Питання щодо замовлення'),
        ('cooperation', 'Співпраця')
    ], validators=[DataRequired(message="Оберіть тему звернення")])
    message = TextAreaField('Message', validators=[
        DataRequired(message="Поле Message є обов'язковим"),
        Length(max=500, message="Повідомлення не може перевищувати 500 символів")
    ])
    submit = SubmitField('Send Message')
