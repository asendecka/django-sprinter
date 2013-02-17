from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'sprinter.achievements.views.board', name='board'),
	url(r'^home/$', 'sprinter.achievements.views.home', name='home'),
	url(r'^(?P<pk>[0-9]+)/$', 'sprinter.achievements.views.sprinter_detail', name='sprinter_detail'),
	url(r'^achievement/(?P<pk>[0-9]+)/$', 'sprinter.achievements.views.achievement_detail', name='achievement_detail'),
    # TODO: remove
    (r'^test/$', 'sprinter.achievements.views.test_trac'),
    (r'^test_git/$', 'sprinter.achievements.views.test_github'),
)
