from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^signin/$', 'sprinter.userprofile.views.signin', name='signin'),
	url(r'^edit/$', 'sprinter.userprofile.views.edit_profile', name='edit_profile'),
	url(r'^signout/$', 'sprinter.userprofile.views.signout', name='signout'),
)
