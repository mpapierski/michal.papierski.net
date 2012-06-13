from django.db import models
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
	'''
	Post category

	>>> cat = Category.objects.create(name = 'Category')
	>>> cat.name
	'Category'
	'''
	name = models.CharField(max_length = 20,
		db_index = True, verbose_name = _('Name'))

	class Meta:
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')

	def __unicode__(self):
		return self.name

class Post(models.Model):
	'''
	Blog post
	
	>>> post = Post.objects.create(title = 'Title', message = 'Test')
	>>> post.added is not None
	True
	>>> post.modified is not None
	True
	'''
	added = models.DateTimeField(auto_now_add = True,
		verbose_name = _('Added'))
	modified = models.DateTimeField(auto_now = True,
		verbose_name = _('Modified'))
	title = models.CharField(max_length = 150, verbose_name = _('Title'))
	slug = models.SlugField(db_index = True, verbose_name = _('Slug'))
	message = models.TextField(verbose_name = _('Message'))
	categories = models.ManyToManyField(Category)
	
	def __unicode__(self):
		return self.title
