from django.conf.urls import patterns

urlpatterns = patterns('',
	(r'^$', 'sprinter.achievements.views.board'),
	(r'^home/$', 'sprinter.achievements.views.home'),
	(r'^(?P<pk>[0-9]+)/$', 'sprinter.achievements.views.sprinter_detail'),
	(r'^achievement/(?P<pk>[0-9]+)/$', 'sprinter.achievements.views.achievement_detail'),
    # TODO: remove
    (r'^test/$', 'sprinter.achievements.views.test_trac'),
    (r'^test_git/$', 'sprinter.achievements.views.test_github'),
)
