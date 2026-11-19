from flask import (
    current_app,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from app.users import users_bp


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        valid_user = current_app.config["VALID_USERNAME"]
        valid_pass = current_app.config["VALID_PASSWORD"]

        if username == valid_user and password == valid_pass:
            session["username"] = username
            flash("Ви успішно увійшли в систему!", "success")
            return redirect(url_for("users.profile"))

        flash("Неправильний логін або пароль. Спробуйте ще раз.", "danger")
        return redirect(url_for("users.login"))

    return render_template("users/login.html")


@users_bp.route("/profile")
def profile():
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    cookies = request.cookies.to_dict()
    theme = request.cookies.get("theme", "light")
    return render_template(
        "users/profile.html",
        username=session["username"],
        cookies=cookies,
        theme=theme,
    )


@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("users.login"))


@users_bp.route("/cookie/add", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Для керування cookie потрібно увійти.", "warning")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "").strip()
    days_text = request.form.get("days", "1").strip()

    if not key or not value:
        flash("Вкажіть ключ і значення cookie.", "danger")
        return redirect(url_for("users.profile"))

    if key.lower() == "session":
        flash("Назва 'session' зарезервована для Flask. Виберіть інший ключ.", "danger")
        return redirect(url_for("users.profile"))

    try:
        days = int(days_text)
        if days < 1:
            raise ValueError
    except ValueError:
        flash("Термін дії має бути цілим числом від 1 дня.", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(
        key,
        value,
        max_age=days * 24 * 60 * 60,
        httponly=True,
        samesite="Lax",
    )
    flash(f"Cookie '{key}' успішно додано на {days} дн.", "success")
    return response


@users_bp.route("/cookie/delete", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        flash("Для керування cookie потрібно увійти.", "warning")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    if not key:
        flash("Вкажіть ключ cookie для видалення.", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.delete_cookie(key)
    flash(f"Запит на видалення cookie '{key}' виконано.", "success")
    return response


@users_bp.route("/cookie/delete-all", methods=["POST"])
def delete_all_cookies():
    if "username" not in session:
        flash("Для керування cookie потрібно увійти.", "warning")
        return redirect(url_for("users.login"))

    response = make_response(redirect(url_for("users.profile")))
    for key in request.cookies.keys():
        response.delete_cookie(key)
    flash("Усі cookie поточного сайту видалено.", "success")
    return response


@users_bp.route("/theme/<theme>", methods=["POST"])
def set_theme(theme):
    if "username" not in session:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    if theme not in ("light", "dark"):
        flash("Невідома кольорова схема.", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie(
        "theme",
        theme,
        max_age=365 * 24 * 60 * 60,
        httponly=True,
        samesite="Lax",
    )
    flash("Кольорову схему змінено.", "success")
    return response
