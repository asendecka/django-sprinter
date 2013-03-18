import hurl


urlpatterns = hurl.patterns('sprinter.achievements.views', [
    ('', 'board'),
    ('home', 'home'),
    ('<pk:int>', 'sprinter_detail'),
    ('achievements', [
        ('', 'achievements'),
        ('<pk:int>', 'achievement_detail')
    ])
])
