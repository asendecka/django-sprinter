# ticket fields
FD_STATUS = 'status'
FD_COMMENT = 'comment'
FD_RESOLUTION = 'resolution'
FD_ATTACHMENT = 'attachment'

FIELDS = (
    (FD_STATUS, 'Status'),
    (FD_COMMENT, 'Comment'),
    (FD_RESOLUTION, 'Resolution'),
    (FD_ATTACHMENT, 'Attachement'),
)

# ticket statuses
ST_ASSIGN = 0
ST_CLOSED = 1
ST_NEW = 2

STATUSES = (
    (ST_ASSIGN, 'assign'),
    (ST_CLOSED, 'closed'),
    (ST_NEW, 'new'),
)

# ticket types
TP_UNCAT = 0 
TP_BUG = 1
TP_FEATURE = 2
TP_CLEANUP = 3

TYPES = (
    (TP_UNCAT, 'Uncategorized'), 
    (TP_BUG, 'Bug'), 
    (TP_FEATURE, 'New feature'), 
    (TP_CLEANUP, 'Cleanup/optimization'),
)

# ticket severity
SV_NORMAL = 0 
SV_BLOCKER = 1

SEVERITIES = (
    (SV_NORMAL,'Normal'), 
    (SV_BLOCKER, 'Release blocker'),
)

# ticket resolution
RS_FIXED = 0 
RS_INVALID = 1
RS_WONTFIX = 2
RS_DUPLICATE = 3
RS_WORKS = 4
RS_NEEDSINFO = 5

RESOLUTIONS = (
    (RS_FIXED, 'fixed'), 
    (RS_INVALID, 'invalid'), 
    (RS_WONTFIX, 'wontfix'),
    (RS_DUPLICATE, 'duplicate'), 
    (RS_WORKS, 'worksforme'), 
    (RS_NEEDSINFO, 'needsinfo'),
)

# ticket components
CM_ADMIN = 0
CM_ADMINDOCS = 1
CM_AUTH = 2
CM_COMMENTS = 3
CM_CONTENTTYPES = 4 
CM_CSRF = 5
CM_FLATPAGES = 6
CM_FORMTOOLS = 7
CM_HUMANIZE = 8
CM_MESSAGES = 9
CM_REDIRECTS = 10
CM_SESSIONS = 11
CM_SITEMAPS = 12
CM_SITES = 13
CM_STATICFILES = 14
CM_SYNDICATION = 15
CM_WEBDESIGN = 16
CM_CACHE = 17
CM_MAIL = 18
CM_COMMANDS = 19
CM_OTHER = 20
CM_SERIALIZATION = 21 
CM_URLS = 22
CM_MODELS = 23
CM_WEBSITE = 24
CM_DOCS = 25
CM_FILES = 26
CM_FORMS = 27
CM_GENERIC_VIEWS = 28
CM_GIS = 29
CM_HTTP = 30
CM_INTERNATIONALIZATION = 31
CM_ORM_AGGREGATION = 32
CM_PYTHON_2 = 33
CM_PYTHON_3 = 34
CM_TEMPLATE = 35
CM_TESTING = 36
CM_TRANSLATIONS = 37
CM_UNCAT = 38

COMPONENTS = (
    (CM_ADMIN, 'contrib.admin'), 
    (CM_ADMINDOCS, 'contrib.admindocs'), 
    (CM_AUTH, 'contrib.auth'), 
    (CM_COMMENTS, 'contrib.comments'), 
    (CM_CONTENTTYPES, 'contrib.contenttypes'), 
    (CM_CSRF, 'contrib.csrf'), 
    (CM_FLATPAGES, 'contrib.flatpages'), 
    (CM_FORMTOOLS, 'contrib.formtools'), 
    (CM_HUMANIZE, 'contrib.humanize'), 
    (CM_MESSAGES, 'contrib.messages'), 
    (CM_REDIRECTS, 'contrib.redirects'), 
    (CM_SESSIONS, 'contrib.sessions'), 
    (CM_SITEMAPS, 'contrib.sitemaps'), 
    (CM_SITES, 'contrib.sites'), 
    (CM_STATICFILES, 'contrib.staticfiles'), 
    (CM_SYNDICATION, 'contrib.syndication'), 
    (CM_WEBDESIGN, 'contrib.webdesign'), 
    (CM_CACHE, 'Core (Cache system)'), 
    (CM_MAIL, 'Core (Mail)'), 
    (CM_COMMANDS, 'Core (Management commands)'), 
    (CM_OTHER, 'Core (Other)'), 
    (CM_SERIALIZATION, 'Core (Serialization)'), 
    (CM_URLS, 'Core (URLs)'), 
    (CM_MODELS, 'Database layer (models, ORM)'), 
    (CM_WEBSITE, 'Djangoproject.com Web site'), 
    (CM_DOCS, 'Documentation'), 
    (CM_FILES, 'File uploads/storage'), 
    (CM_FORMS, 'Forms'), 
    (CM_GENERIC_VIEWS, 'Generic views'), 
    (CM_GIS, 'GIS'), 
    (CM_HTTP, 'HTTP handling'), 
    (CM_INTERNATIONALIZATION, 'Internationalization'), 
    (CM_ORM_AGGREGATION, 'ORM aggregation'), 
    (CM_PYTHON_2, 'Python 2'), 
    (CM_PYTHON_3, 'Python 3'), 
    (CM_TEMPLATE, 'Template system'), 
    (CM_TESTING, 'Testing framework'), 
    (CM_TRANSLATIONS, 'Translations'), 
    (CM_UNCAT, 'Uncategorized'),
)
