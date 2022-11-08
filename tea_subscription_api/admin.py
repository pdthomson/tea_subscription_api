from django.contrib import admin

from .models import Tea
from .models import Customer 
from .models import Subscription 

admin.site.register(Tea)
admin.site.register(Customer)
admin.site.register(Subscription)
# Register your models here.
