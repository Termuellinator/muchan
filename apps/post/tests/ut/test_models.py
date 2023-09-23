from django.test import TestCase
from django.db.utils import DataError, IntegrityError

from apps.post import models
from apps.user.models import User


class TestCategoryModel(TestCase):
    def setUp(self) -> None:
        self.category_name = "Memes"
        self.category = models.Category(cat=self.category_name)

    def test_create_category_object_successful(self):
        self.assertIsInstance(self.category, models.Category)

    def test_dunder_str(self):
        self.assertEqual(str(self.category), self.category_name)

    def test_verbose_name_plural(self):
        self.assertEqual(self.category._meta.verbose_name_plural, "Categories")

    def test_max_length(self):
        too_long_category = "0123456789_" * 10
        with self.assertRaises(DataError):
            models.Category.objects.create(cat=too_long_category)


class TestTagModel(TestCase):
    def setUp(self) -> None:
        self.tag_name = "Funny"
        self.tag = models.Tag(name=self.tag_name)

    def test_create_tag_object_successful(self):
        self.assertIsInstance(self.tag, models.Tag)

    def test_dunder_str(self):
        self.assertEqual(str(self.tag), self.tag_name)


class TestPostModel(TestCase):
    def setUp(self) -> None:
        self.post_title = "Testpost"
        self.username = "test"
        self.category = "testcat"
        self.user = User.objects.create_user(
            username=self.username,
            password="test",
            )
        self.cat = models.Category.objects.create(cat=self.category)
        self.post = models.Post(
            user_id=self.user,
            cat_id=self.cat,
            title=self.post_title,
            image="uploads/image.jpg"
        )
    
    def test_create_post_object_successful(self):
        self.assertIsInstance(self.post, models.Post)
        
    def test_dunder_str(self):
        self.assertEqual(str(self.post), self.post_title)
        
    def test_username_property(self):
        self.assertEqual(self.post.username, self.username)
        
    def test_category_property(self):
        self.assertEqual(self.post.category, self.category)


class TestPostTagModel(TestCase):
    def setUp(self) -> None:
        self.post_title = "Testpost"
        self.username = "test"
        self.category = "testcat"
        self.user = User.objects.create_user(
            username=self.username,
            password="test",
            )
        self.cat = models.Category.objects.create(cat=self.category)
        self.post = models.Post.objects.create(
            user_id=self.user,
            cat_id=self.cat,
            title=self.post_title,
            image="uploads/image.jpg"
        )
        self.tag_name = "Funny"
        self.tag = models.Tag.objects.create(name=self.tag_name)
        self.post.tags.add(self.tag)
        self.posttag = models.PostTag.objects.all()[0]
        
    def test_create_posttag_object_successful(self):
        self.assertIsInstance(self.posttag, models.PostTag)
        
    def test_create_duplicate_posttag_raises_error(self):
        with self.assertRaises(IntegrityError):
            models.PostTag.objects.create(post_id=self.post, tag_id=self.tag)

    def test_dunder_str(self):
        self.assertEqual(str(self.posttag), 
                         f"{self.post_title} - {self.tag_name}")

    def test_title_property(self):
        self.assertEqual(self.posttag.title, self.post_title)
        
    def test_tag_property(self):
        self.assertEqual(self.posttag.tag, self.tag_name)


class TestCommentModel(TestCase):
    def setUp(self) -> None:
        self.post_title = "Testpost"
        self.username = "test"
        self.category = "testcat"
        self.body = "This is a test comment" * 10
        self.user = User.objects.create_user(
            username=self.username,
            password="test",
            )
        self.cat = models.Category.objects.create(cat=self.category)
        self.post = models.Post.objects.create(
            user_id=self.user,
            cat_id=self.cat,
            title=self.post_title,
            image="uploads/image.jpg"
        )
        self.comment = models.Comment(
            post_id=self.post,
            user_id=self.user,
            body=self.body
        )

    def test_create_comment_object_successful(self):
        self.assertIsInstance(self.comment, models.Comment)

    def test_dunder_str(self):
        self.assertEqual(str(self.comment), 
                         f"By {self.username} on {self.post_title}")

    def test_short_body_propert(self):
        self.assertEqual(self.comment.short_body, self.body[:99] + "…")

    def test_username_property(self):
        self.assertEqual(self.comment.username, self.username)

    def test_post_title_property(self):
        self.assertEqual(self.comment.post_title, self.post_title)