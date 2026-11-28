from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db

# Асоціативна таблиця для зв'язку Many-to-Many між постами та тегами
post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    category: Mapped[str] = mapped_column(
        Enum("news", "publication", "tech", "other", name="post_category"),
        default="other",
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Зовнішній ключ та зв'язок One-to-Many з моделлю User
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="posts")  # noqa: F821

    # Зв'язок Many-to-Many з моделлю Tag
    tags: Mapped[list["Tag"]] = relationship(
        secondary=post_tags,
        back_populates="posts",
    )

    def __repr__(self) -> str:
        return f"<Post(title={self.title!r})>"


class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    # Зворотний зв'язок Many-to-Many з постами
    posts: Mapped[list["Post"]] = relationship(
        secondary=post_tags,
        back_populates="tags",
    )

    def __repr__(self) -> str:
        return f"<Tag({self.name!r})>"
