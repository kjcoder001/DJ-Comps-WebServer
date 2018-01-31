'''from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, sap_id, password, **kwargs):
        sap_id = self.normalize_sap_id(sap_id)
        is_superuser = kwargs.pop('is_superuser', False)
        user = self.model(
            sap_id=sap_id,
            is_active=True,
            is_superuser=is_superuser,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, sap_id, password=None, **extra_fields):
        return self._create_user(sap_id, password, **extra_fields)

    def create_superuser(self, sap_id, password, **extra_fields):
        return self._create_user(sap_id, password, is_superuser=True, **extra_fields)
'''
