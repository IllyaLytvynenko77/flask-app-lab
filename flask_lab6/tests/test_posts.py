import unittest
from app import create_app, db
from app.posts.models import Post


class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        # US01: Створення нового поста (POST /post/create)
        with self.app.app_context():
            response = self.client.post(
                "/post/create",
                data={
                    "title": "My first post",
                    "content": "This is TDD with SQLAlchemy!",
                    "is_active": "y",
                    "category": "tech",
                },
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"has been added successfully.", response.data)

            post = db.session.scalar(db.select(Post).where(Post.title == "My first post"))
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "This is TDD with SQLAlchemy!")
            self.assertEqual(post.category, "tech")
            self.assertEqual(post.author, "Anonymous")

    def test_list_posts(self):
        # US02: Перегляд усіх активних постів (GET /post)
        with self.app.app_context():
            p1 = Post(title="Visible Post", content="Active content", is_active=True)
            p2 = Post(title="Hidden Post", content="Inactive content", is_active=False)
            db.session.add_all([p1, p2])
            db.session.commit()

            response = self.client.get("/post")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Visible Post", response.data)
            self.assertNotIn(b"Hidden Post", response.data)

    def test_view_post_detail(self):
        # US03: Перегляд деталей конкретного поста (GET /post/<id>)
        with self.app.app_context():
            post = Post(title="Detail Title", content="Detailed text content", category="news")
            db.session.add(post)
            db.session.commit()
            post_id = post.id

            response = self.client.get(f"/post/{post_id}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Detail Title", response.data)
            self.assertIn(b"Detailed text content", response.data)

    def test_update_post(self):
        # US04: Редагування поста (POST /post/<id>/update)
        with self.app.app_context():
            post = Post(title="Old Title", content="Old Content", is_active=True, category="other")
            db.session.add(post)
            db.session.commit()
            post_id = post.id

            response = self.client.post(
                f"/post/{post_id}/update",
                data={
                    "title": "Updated Title",
                    "content": "Updated Content",
                    "is_active": "y",
                    "category": "publication",
                },
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Updated Title", response.data)

            updated = db.session.get(Post, post_id)
            self.assertEqual(updated.title, "Updated Title")
            self.assertEqual(updated.content, "Updated Content")
            self.assertEqual(updated.category, "publication")

    def test_delete_post(self):
        # US05: Видалення поста (GET підтвердження + POST /post/<id>/delete)
        with self.app.app_context():
            post = Post(title="Post To Delete", content="Temporary content")
            db.session.add(post)
            db.session.commit()
            post_id = post.id

            get_resp = self.client.get(f"/post/{post_id}/delete")
            self.assertEqual(get_resp.status_code, 200)
            self.assertIn(b"Post To Delete", get_resp.data)

            post_resp = self.client.post(f"/post/{post_id}/delete", follow_redirects=True)
            self.assertEqual(post_resp.status_code, 200)
            self.assertIsNone(db.session.get(Post, post_id))

    def test_404_not_found(self):
        # US06: Помилка 404 при відсутньому пості (GET /post/999)
        response = self.client.get("/post/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"404", response.data)


if __name__ == "__main__":
    unittest.main()
