import hurl


urlpatterns = hurl.patterns('sprinter.userprofile.views', {
    'signin': 'signin',
    'edit': 'edit_profile',
    'signout': 'signout',
})
