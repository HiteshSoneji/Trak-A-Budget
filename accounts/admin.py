from django.contrib import admin

from .models import Ind_User, Org_User

# Register your models here.

admin.site.register(Ind_User)

admin.site.register(Org_User)