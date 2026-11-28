import os
from sqlalchemy import select, event
from sqlalchemy.orm import Session, joinedload, selectinload

os.environ["SQLALCHEMY_ECHO"] = "True"

from app import create_app, db
from app.posts.models import Post

app = create_app("development")

select_queries = []


with app.app_context():
    @event.listens_for(db.engine, "before_cursor_execute")
    def count_selects(conn, cursor, statement, parameters, context, executemany):
        if statement.strip().upper().startswith("SELECT"):
            select_queries.append(statement)

    print("=" * 70)
    print("ВАРІАНТ 1: БЕЗ .options() (Lazy Loading / N+1)")
    print("=" * 70)
    select_queries.clear()
    with Session(db.engine) as session1:
        stmt1 = select(Post).order_by(Post.id.desc())
        posts1 = session1.scalars(stmt1).all()
        for post in posts1:
            print(
                post.title,
                "|",
                post.user.username,
                "|",
                [tag.name for tag in post.tags],
            )
    count_without_options = len(select_queries)
    posts_count_1 = len(posts1)

    print("\n" + "=" * 70)
    print("ВАРІАНТ 2: ІЗ joinedload(Post.user) ТА selectinload(Post.tags)")
    print("=" * 70)
    select_queries.clear()
    with Session(db.engine) as session2:
        stmt2 = (
            select(Post)
            .options(
                joinedload(Post.user),
                selectinload(Post.tags),
            )
            .order_by(Post.id.desc())
        )
        posts2 = session2.scalars(stmt2).all()
        for post in posts2:
            print(
                post.title,
                "|",
                post.user.username,
                "|",
                [tag.name for tag in post.tags],
            )
    count_with_options = len(select_queries)
    posts_count_2 = len(posts2)

    print("\n" + "=" * 70)
    print("ПОРІВНЯЛЬНА ТАБЛИЦЯ РЕЗУЛЬТАТІВ (Пункт 13)")
    print("=" * 70)
    print(f"{'Варіант запиту':<36} | {'Кількість дописів':<18} | {'Кількість SELECT':<16}")
    print("-" * 76)
    print(f"{'Без .options()':<36} | {posts_count_1:<18} | {count_without_options:<16}")
    print(f"{'Із joinedload() та selectinload()':<36} | {posts_count_2:<18} | {count_with_options:<16}")
