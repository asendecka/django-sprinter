FIELDS = (
    'Status',
    'Comment',
    'Resolution',
    'Attachement',
)

TYPES = (
    'Uncategorized',
    'Bug',
    'New feature',
    'Cleanup/optimization',
)

SEVERITIES = (
    'Normal',
    'Release blocker',
)

RESOLUTIONS = (
    'fixed',
    'invalid',
    'wontfix',
    'duplicate',
    'worksforme',
    'needsinfo',
)

COMPONENTS = (
    'contrib.admin',
    'contrib.admindocs',
    'contrib.auth',
    'contrib.comments',
    'contrib.contenttypes',
    'contrib.csrf',
    'contrib.flatpages',
    'contrib.formtools',
    'contrib.humanize',
    'contrib.messages',
    'contrib.redirects',
    'contrib.sessions',
    'contrib.sitemaps',
    'contrib.sites',
    'contrib.staticfiles',
    'contrib.syndication',
    'contrib.webdesign',
    'Core (Cache system)',
    'Core (Mail)',
    'Core (Management commands)',
    'Core (Other)',
    'Core (Serialization)',
    'Core (URLs)',
    'Database layer (models, ORM)',
    'Djangoproject.com Web site',
    'Documentation',
    'File uploads/storage',
    'Forms',
    'Generic views',
    'GIS',
    'HTTP handling',
    'Internationalization',
    'ORM aggregation',
    'Python 2',
    'Python 3',
    'Template system',
    'Testing framework',
    'Translations',
    'Uncategorized',
)

FIELDS_CHOICES = zip(FIELDS, FIELDS)
TYPES_CHOICES = zip(TYPES, TYPES)
SEVERITIES_CHOICES = zip(SEVERITIES, SEVERITIES)
RESOLUTIONS_CHOICES = zip(RESOLUTIONS, RESOLUTIONS)
COMPONENTS_CHOICES = zip(COMPONENTS, COMPONENTS)
