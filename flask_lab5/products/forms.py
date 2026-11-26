from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

CATEGORY_CHOICES = [
    ('electronics', 'Електроніка'),
    ('clothing', 'Одяг'),
    ('books', 'Книги'),
    ('home', 'Дім та сад'),
    ('other', 'Інше')
]


class ProductForm(FlaskForm):
    name = StringField('Назва товару', validators=[
        DataRequired(message="Введіть назву товару"),
        Length(min=3, message="Назва товару повинна містити мінімум 3 символи")
    ])
    content = TextAreaField('Опис товару', validators=[
        DataRequired(message="Введіть опис товару")
    ])
    price = DecimalField('Ціна (грн)', places=2, validators=[
        DataRequired(message="Введіть ціну товару"),
        NumberRange(min=0.01, message="Ціна має бути додатною (мінімум 0.01)")
    ])
    category = SelectField('Категорія', choices=CATEGORY_CHOICES, validators=[
        DataRequired(message="Оберіть категорію")
    ])
    quantity = IntegerField('Кількість одиниць', validators=[
        DataRequired(message="Введіть кількість одиниць"),
        NumberRange(min=0, message="Кількість не може бути від'ємною")
    ])
    image = FileField('Зображення товару (PNG, JPG, JPEG)', validators=[
        FileAllowed(['png', 'jpg', 'jpeg'], 'Дозволені лише зображення форматів PNG, JPG або JPEG!')
    ])
    submit = SubmitField('Зберегти товар')
