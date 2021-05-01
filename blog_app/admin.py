from django.contrib import admin
from blog_app.models import PostModel, CommentModel


# Register your models here.
admin.site.register(PostModel)
admin.site.register(CommentModel)