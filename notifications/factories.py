import factory
import factory.fuzzy
from django.contrib.auth import get_user_model
from notifications.models import Category, Notification
User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', )
    username = "Jack"

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

class NotificationFactory(factory.django.DjangoModelFactory):
    sender = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    class Meta:
        model = Notification
        django_get_or_create = ('title', )
    title = "Hello World"