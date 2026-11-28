import unittest
from app import create_app, db
from app.models import User
from app.posts.models import Post, Tag


class PostRelationshipsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            u1 = User(username="user1", email="user1@ex.com", password="secret1")
            u2 = User(username="user2", email="user2@ex.com", password="secret2")
            t1 = Tag(name="Tech")
            t2 = Tag(name="Art")
            t3 = Tag(name="Science")
            db.session.add_all([u1, u2, t1, t2, t3])
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_one_to_many_user_posts(self):
        with self.app.app_context():
            u1 = db.session.scalar(db.select(User).where(User.username == "user1"))
            u2 = db.session.scalar(db.select(User).where(User.username == "user2"))

            p1 = Post(title="Post by user1", content="Content 1", user=u1)
            p2 = Post(title="Post by user2", content="Content 2", user=u2)
            db.session.add_all([p1, p2])
            db.session.commit()

            self.assertEqual(len(u1.posts), 1)
            self.assertEqual(u1.posts[0].title, "Post by user1")
            self.assertEqual(p2.user.username, "user2")

    def test_many_to_many_post_tags(self):
        with self.app.app_context():
            u1 = db.session.scalar(db.select(User).where(User.username == "user1"))
            t_tech = db.session.scalar(db.select(Tag).where(Tag.name == "Tech"))
            t_art = db.session.scalar(db.select(Tag).where(Tag.name == "Art"))

            post = Post(title="Tagged Post", content="Tagged Content", user=u1)
            post.tags.append(t_tech)
            post.tags.append(t_art)
            db.session.add(post)
            db.session.commit()

            self.assertEqual({t.name for t in post.tags}, {"Tech", "Art"})
            self.assertEqual(t_tech.posts[0].title, "Tagged Post")

    def test_create_post_with_author_and_tags(self):
        with self.app.app_context():
            u2 = db.session.scalar(db.select(User).where(User.username == "user2"))
            tags = db.session.scalars(db.select(Tag)).all()

            response = self.client.post(
                "/post/create",
                data={
                    "title": "Art of pop culture",
                    "content": "Full content for pop culture article",
                    "category": "tech",
                    "author_id": str(u2.id),
                    "tags": [str(t.id) for t in tags],
                    "is_active": "y",
                },
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Art Of Pop Culture", response.data)
            self.assertIn(b"Tech", response.data)
            self.assertIn(b"Art", response.data)
            self.assertIn(b"Science", response.data)

            created = db.session.scalar(db.select(Post).where(Post.title == "Art of pop culture"))
            self.assertIsNotNone(created)
            self.assertEqual(created.user_id, u2.id)
            self.assertEqual(len(created.tags), 3)

    def test_update_and_delete_post(self):
        with self.app.app_context():
            u1 = db.session.scalar(db.select(User).where(User.username == "user1"))
            u2 = db.session.scalar(db.select(User).where(User.username == "user2"))
            t_art = db.session.scalar(db.select(Tag).where(Tag.name == "Art"))

            post = Post(title="Initial", content="Body", user=u1)
            db.session.add(post)
            db.session.commit()
            post_id = post.id

            resp = self.client.post(
                f"/post/{post_id}/update",
                data={
                    "title": "Updated Post",
                    "content": "Updated Body",
                    "category": "news",
                    "author_id": str(u2.id),
                    "tags": [str(t_art.id)],
                    "is_active": "y",
                },
                follow_redirects=True,
            )
            self.assertEqual(resp.status_code, 200)
            updated = db.session.get(Post, post_id)
            self.assertEqual(updated.user_id, u2.id)
            self.assertEqual([t.name for t in updated.tags], ["Art"])

            del_resp = self.client.post(f"/post/{post_id}/delete", follow_redirects=True)
            self.assertEqual(del_resp.status_code, 200)
            self.assertIsNone(db.session.get(Post, post_id))


if __name__ == "__main__":
    unittest.main()
