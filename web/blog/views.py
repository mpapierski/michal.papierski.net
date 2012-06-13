from django.views.generic import ListView

from blog.models import Post

class PostListView(ListView):
	'''
	Posts list
	'''
	model = Post
	