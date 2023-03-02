from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True 

    def create_user(self, pis, password = None, **extra_fields):
        user = self.model(pis = pis,**extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user


    def create_superuser(self, pis, password= None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(pis,password,  **extra_fields)
        

