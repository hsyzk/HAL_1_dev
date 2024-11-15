from django.contrib import admin
from .models import Account
from .models import Post
from .models import Post_Mu

admin.site.register(Post)
admin.site.register(Account)
admin.site.register(Post_Mu)

# admin.site.register(NoteTable)

# Register your models here.
