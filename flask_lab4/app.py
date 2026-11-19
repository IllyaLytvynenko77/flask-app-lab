from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response

app = Flask(__name__)
app.secret_key = "change-this-secret-key-for-your-project"

# Тестові дані для входу (без бази даних)
VALID_USERNAME = "admin"
VALID_PASSWORD = "12345"


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["username"] = username
            flash("Ви успішно увійшли в систему!", "success")
            return redirect(url_for("profile"))

        flash("Неправильний логін або пароль. Спробуйте ще раз.", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile")
def profile():
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("login"))

    # Беремо cookie з поточного запиту, службові cookie Flask не приховуємо.
    cookies = request.cookies.to_dict()
    theme = request.cookies.get("theme", "light")
    return render_template("profile.html", username=session["username"],
                           cookies=cookies, theme=theme)


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("login"))


@app.route("/cookie/add", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Для керування cookie потрібно увійти.", "warning")
        return redirect(url_for("login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "").strip()
    days_text = request.form.get("days", "1").strip()

    if not key or not value:
        flash("Вкажіть ключ і значення cookie.", "danger")
        return redirect(url_for("profile"))

    if key.lower() == "session":
        flash("Назва 'session' зарезервована для Flask. Виберіть інший ключ.", "danger")
        return redirect(url_for("profile"))

    try:
        days = int(days_text)
        if days < 1:
            raise ValueError
    except ValueError:
        flash("Термін дії має бути цілим числом від 1 дня.", "danger")
        return redirect(url_for("profile"))

    response = make_response(redirect(url_for("profile")))
    response.set_cookie(key, value, max_age=days * 24 * 60 * 60,
                        httponly=True, samesite="Lax")
    flash(f"Cookie '{key}' успішно додано на {days} дн.", "success")
    return response


@app.route("/cookie/delete", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        flash("Для керування cookie потрібно увійти.", "warning")
        return redirect(url_for("login"))

    key = request.form.get("key", "").strip()
    if not key:
        flash("Вкажіть ключ cookie для видалення.", "danger")
        return redirect(url_for("profile"))

    response = make_response(redirect(url_for("profile")))
    response.delete_cookie(key)
    flash(f"Запит на видалення cookie '{key}' виконано.", "success")
    return response


@app.route("/cookie/delete-all", methods=["POST"])
def delete_all_cookies():
    if "username" not in session:
        flash("Для керування cookie потрібно увійти.", "warning")
        return redirect(url_for("login"))

    response = make_response(redirect(url_for("profile")))
    for key in request.cookies.keys():
        response.delete_cookie(key)
    flash("Усі cookie поточного сайту видалено.", "success")
    return response


@app.route("/theme/<theme>", methods=["POST"])
def set_theme(theme):
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("login"))

    if theme not in ("light", "dark"):
        flash("Невідома кольорова схема.", "danger")
        return redirect(url_for("profile"))

    response = make_response(redirect(url_for("profile")))
    response.set_cookie("theme", theme, max_age=365 * 24 * 60 * 60,
                        httponly=True, samesite="Lax")
    flash("Кольорову схему змінено.", "success")
    return response


if __name__ == "__main__":
    app.run(debug=True)
