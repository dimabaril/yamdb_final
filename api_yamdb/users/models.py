from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from api_yamdb.settings import (MESSAGE_FOR_RESERVED_NAME,
                                RESERVED_NAME)


class MyUserManager(UserManager):
    """Сохраняет пользователя только с email.
    Зарезервированное имя использовать нельзя."""

    def create_user(self, username, email, password, **extra_fields):

        if not email:

            raise ValueError('Поле email обязательное')

        if username == RESERVED_NAME:

            raise ValueError(MESSAGE_FOR_RESERVED_NAME)

        return super().create_user(
            username, email, password, **extra_fields)

    def create_superuser(
            self, username, email, password, role='admin', **extra_fields):

        return super().create_superuser(
            username, email, password, role='admin', **extra_fields)


class User(AbstractUser):
    """Our custom user model."""

    USER = 'user'
    MODER = 'moderator'
    ADMIN = 'admin'
    ROLES_CHOICES = (
        (USER, USER),
        (MODER, MODER),
        (ADMIN, ADMIN),
    )
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=50, choices=ROLES_CHOICES, default='user')
    username = models.CharField(max_length=50, unique=True)
    objects = MyUserManager()
    REQUIRED_FIELDS = ('email', 'password')

    class Meta:

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODER

    @property
    def is_user(self):
        return self.role == self.USER
