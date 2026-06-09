from django.contrib.auth.models import User
from django.test import TestCase

from profiles.models import UserProfile, Follow


class UserProfileModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="paul",
            email="paul@paul.es",
            password="paul123",
        )
        self.user2 = User.objects.create_user(
            username="jony",
            email="jony@jony.es",
            password="jony123",
        )
        # UserProfile no tiene create_user; se crea ligado a un User existente.
        self.profile1 = UserProfile.objects.create(user=self.user1)
        self.profile2 = UserProfile.objects.create(user=self.user2)

    def test_user_profile_creation(self):
        self.assertEqual(self.user1.username, "paul")
        self.assertEqual(self.profile1.user, self.user1)
        self.assertEqual(self.profile2.user.username, "jony")

    def test_follow_and_unfollow(self):
        self.profile1.follow(self.profile2)
        self.assertTrue(
            Follow.objects.filter(
                follower=self.profile1,
                following=self.profile2,
            ).exists()
        )
        self.profile1.unfollow(self.profile2)
        self.assertFalse(
            Follow.objects.filter(
                follower=self.profile1,
                following=self.profile2,
            ).exists()
        )

    def test_str_userProfile(self):
        self.assertEqual(str(self.profile1),self.profile1.user.username)

class FollowModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="paul",
            email="paul@paul.es",
            password="paul123",
        )
        self.user2 = User.objects.create_user(
            username="jony",
            email="jony@jony.es",
            password="jony123",
        )
        # UserProfile no tiene create_user; se crea ligado a un User existente.
        self.profile1 = UserProfile.objects.create(user=self.user1)
        self.profile2 = UserProfile.objects.create(user=self.user2)

    def test_unique_follow_once_time(self):
        Follow.objects.get_or_create(follower=self.profile1, following=self.profile2)
        self.assertEqual(Follow.objects.filter(follower=self.profile1, following=self.profile2).count(), 1)
        Follow.objects.get_or_create(follower=self.profile1, following=self.profile2)
        self.assertEqual(Follow.objects.filter(follower=self.profile1, following=self.profile2).count(), 1)

