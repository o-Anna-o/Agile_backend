from django.contrib import admin
from .models import Task
from .models import Sprint

admin.site.register(Task)

admin.site.register(Sprint)


from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(CustomUser, UserAdmin)



