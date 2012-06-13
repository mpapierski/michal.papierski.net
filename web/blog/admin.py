from django.contrib import admin

from blog.models import Post, Category

class PostAdmin(admin.ModelAdmin):
	'''
	Post model admin class
	'''
	prepopulated_fields = {
		'slug': ('title', )
	}
	
admin.site.register(Post, PostAdmin)
admin.site.register(Category)