from django.test import TestCase
from .models import *
# Create your tests here.

# test image class


class ImageTestCase(TestCase):
    def setUp(self):
        # create a user
        user = User.objects.create(
            username='test_user',
            first_name='mzee',
            last_name='mzima'
        )
        Image.objects.create(
            image_name='test_image',
            image='https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
            image_caption='test image',
            profile_id=user.id,
            user_id=user.id
        )

    def test_image_name(self):
        image = Image.objects.get(image_name='test_image')
        self.assertEqual(image.image_name, 'test_image')


# test profile class
class ProfileTestCase(TestCase):
    def setUp(self):
        # create a user
        user = User.objects.create(
            username='test_user',
            first_name='mzee',
            last_name='mzima'
        )
        Profile.objects.create(
            bio='test bio',
            profile_photo='static/img/homepage.jpg',
            user_id=user.id
        )

    def test_bio(self):
        profile = Profile.objects.get(bio='test bio')
        self.assertEqual(profile.bio, 'test bio')


# test likes class
class LikesTestCase(TestCase):
    def setUp(self):
        # create a user
        user = User.objects.create(
            username='test_user',
            first_name='mzee',
            last_name='mzima'
        )
        # create a profile
        Profile.objects.create(
            bio='test bio',
            profile_photo='static/img/homepage.jpg',
            user_id=user.id
        )
        # create a image
        image = Image.objects.create(
            image_caption='test post',
            image='https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
            profile_id=user.id,
            user_id=user.id
        )
        # create a likes
        Likes.objects.create(
            image_id=image.id,
            user_id=user.id
        )

    def test_image_id(self):
        # create a user
        user = User.objects.create(
            username='newuser',
            first_name='mzees',
            last_name='mzimas'
        )
        # create a image
        image = Image.objects.create(
            image_caption='test post',
            image='https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
            profile_id=user.id,
            user_id=user.id
        )
        # likes = Likes.objects.get(image_id=image.id)
        # self.assertEqual(likes.image_id, 1)
