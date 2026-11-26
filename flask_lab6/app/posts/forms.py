from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, DateTimeLocalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

CATEGORIES = [
    ("news", "News"),
    ("publication", "Publication"),
    ("tech", "Tech"),
    ("other", "Other"),
]


class PostForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[
            DataRequired(message="Заголовок є обов'язковим"),
            Length(min=2, max=150, message="Довжина заголовку має бути від 2 до 150 символів"),
        ],
    )
    content = TextAreaField(
        "Content",
        render_kw={"rows": 5, "cols": 40},
        validators=[DataRequired(message="Текст поста є обов'язковим")],
    )
    is_active = BooleanField("Active Post", default=True)
    publish_date = DateTimeLocalField(
        "Publish Date",
        format="%Y-%m-%dT%H:%M",
        default=datetime.now,
        validators=[Optional()],
    )
    category = SelectField(
        "Category",
        choices=CATEGORIES,
        default="other",
        validators=[Optional()],
    )
    submit = SubmitField("Submit")
