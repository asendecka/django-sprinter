from django.conf.urls import patterns

urlpatterns = patterns('',
	(r'^$', 'sprinter.achievements.views.board'),
	(r'^(?P<pk>[0-9]+)/$', 'sprinter.achievements.views.sprinter_detail'),
    # TODO: remove
    (r'^test/$', 'sprinter.achievements.views.test_trac'),
)
