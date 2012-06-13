from django.conf.urls import patterns, url

from blog.views import PostListView

urlpatterns = patterns('',
	#url('^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[_-\w\d]+)/$',
	url(r'^$', PostListView.as_view()),
)
