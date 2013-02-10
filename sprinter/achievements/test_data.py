from datetime import datetime

RECENT_CHANGES = [1,2]

RECENT_TICKETS = {
    1: {
        'change': [
            [datetime(2010, 2, 3, 10, 0, 0, 0), 'testuser', 'comment', '', '', 1], 
            [datetime(2013, 2, 3, 11, 0, 0, 0), 'testuser', 'attachment', '', '', 1], 
            [datetime(2013, 2, 3, 12, 0, 0, 0), 'testuser2', 'comment', '', '', 1], 
            [datetime(2013, 2, 3, 13, 0, 0, 0), 'testuser2', 'comment', '', '', 1], 
            [datetime(2013, 2, 3, 14, 0, 0, 0), 'testuser', 'comment', '', '', 1], 
            [datetime(2013, 2, 3, 15, 0, 0, 0), 'testuser', 'attachment', '', '', 1], 
            [datetime(2013, 2, 3, 16, 0, 0, 0), 'testuser', 'comment', '', '', 1], 
            [datetime(2013, 2, 3, 17, 0, 0, 0), 'testuser', 'resolution', '', '', 1], 
        ],
        'ticket': [1, '', '', {'has_patch': 1, 'type': 'Bug', 'component': 'Core (URLs)',\
                'resolution': 'worksforme', 'severity': 'Normal'}],
    },
    2: {
        'change': [
            [datetime(2010, 2, 2, 10, 0, 0, 0), 'testuser', 'comment', '', '', 1], 
            [datetime(2011, 2, 2, 10, 0, 0, 0), 'testuser', 'comment', '', '', 1], 
            [datetime(2013, 2, 2, 10, 0, 0, 0), 'testuser', 'comment', '', '', 1], 
        ],
        'ticket': [2, '', '', {'has_patch': 0, 'type': 'New feature', 'component': 'GIS',\
                'resolution': 'wontfix', 'severity': 'Release blocker'}],
    }        
}
