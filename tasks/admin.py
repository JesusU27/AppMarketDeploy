from django.contrib import admin
from .models import Sale
from .models import User
from .models import Receipt

# Register your models here.
admin.site.register(Sale);
admin.site.register(User);
admin.site.register(Receipt);