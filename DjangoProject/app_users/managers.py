from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError


class MyUserManager(BaseUserManager):
    def create_user(self, email: str, first_name: str = "", last_name: str = "", username: str = None, password: str = None):
        """
        Oddiy foydalanuvchini yaratish.
        """
        if not email:
            raise ValidationError('Users must have email')

        email = self.normalize_email(email=email)

        if not username:
            username = email[:email.index('@')]

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, first_name: str = "", last_name: str = "", password: str = None):
        """
        Superfoydalanuvchini yaratish.
        """
        superuser = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save(using=self._db)
        return superuser
