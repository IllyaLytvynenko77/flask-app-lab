from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, abort
from sqlalchemy.orm import joinedload, selectinload
from app import db
from app.models import User
from app.posts import post_bp
from app.posts.models import Post, Tag
from app.posts.forms import PostForm


def _populate_form_choices(form: PostForm) -> None:
    authors = db.session.scalars(db.select(User).order_by(User.id)).all()
    form.author_id.choices = [(author.id, author.username) for author in authors]

    all_tags = db.session.scalars(db.select(Tag).order_by(Tag.id)).all()
    form.tags.choices = [(tag.id, tag.name) for tag in all_tags]


@post_bp.route("", methods=["GET"])
@post_bp.route("/", methods=["GET"])
def all_posts():
    stmt = (
        db.select(Post)
        .options(joinedload(Post.user), selectinload(Post.tags))
        .where(Post.is_active.is_(True))
        .order_by(Post.posted.desc())
    )
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)


@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    _populate_form_choices(form)

    if form.validate_on_submit():
        selected_tags = []
        if form.tags.data:
            selected_tags = list(
                db.session.scalars(db.select(Tag).where(Tag.id.in_(form.tags.data))).all()
            )

        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data or datetime.utcnow(),
            category=form.category.data or "other",
            user_id=form.author_id.data,
            tags=selected_tags,
        )
        db.session.add(new_post)
        db.session.commit()
        flash(f"Post '{new_post.title}' has been added successfully.", "success")
        return redirect(url_for("posts.all_posts"))
    elif request.method == "POST":
        flash("Enter the correct data in the form!", "danger")

    return render_template("add_post.html", form=form, title="Create a New Post")


@post_bp.route("/<int:id>", methods=["GET"])
def detail_post(id):
    stmt = (
        db.select(Post)
        .options(joinedload(Post.user), selectinload(Post.tags))
        .where(Post.id == id)
    )
    post = db.session.scalar(stmt)
    if not post:
        abort(404)
    return render_template("detail_post.html", post=post)


@post_bp.route("/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    _populate_form_choices(form)
    form.submit.label.text = "Update Post"

    if request.method == "GET":
        form.publish_date.data = post.posted
        form.author_id.data = post.user_id
        form.tags.data = [tag.id for tag in post.tags]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.user_id = form.author_id.data
        if form.publish_date.data:
            post.posted = form.publish_date.data
        if form.category.data:
            post.category = form.category.data

        if form.tags.data:
            post.tags = list(
                db.session.scalars(db.select(Tag).where(Tag.id.in_(form.tags.data))).all()
            )
        else:
            post.tags = []

        db.session.commit()
        flash("Пост успішно оновлено!", "success")
        return redirect(url_for("posts.detail_post", id=post.id))
    elif request.method == "POST":
        flash("Помилка при оновленні поста. Перевірте поля форми.", "danger")

    return render_template("add_post.html", form=form, title="Edit Post", post=post)


@post_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Пост успішно видалено.", "danger")
        return redirect(url_for("posts.all_posts"))

    return render_template("delete_confirm.html", post=post)
