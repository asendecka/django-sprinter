from django.conf.urls import patterns

urlpatterns = patterns('',
	(r'^$', 'sprinter.achievements.views.board'),
)
