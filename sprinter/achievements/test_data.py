from datetime import datetime

RECENT_CHANGES = [1,2]

RECENT_TICKETS = {
    1: {
        'change': [
            [datetime(2010, 02, 02, 10, 0, 0, 0), 'testuser', 'comment', '', '', 1], 
            [datetime(2013, 02, 02, 11, 0, 0, 0), 'testuser', 'attachment', '', '', 1], 
            [datetime(2013, 02, 02, 12, 0, 0, 0), 'testuser2', 'comment', '', '', 1], 
            [datetime(2013, 02, 02, 13, 0, 0, 0), 'testuser2', 'comment', '', '', 1], 
            [datetime(2013, 02, 02, 14, 0, 0, 0), 'testuser', 'comment', '', '', 1], 
            [datetime(2013, 02, 02, 15, 0, 0, 0), 'testuser', 'comment', '', '', 1], 
            [datetime(2013, 02, 02, 16, 0, 0, 0), 'testuser', 'comment', '', '', 1], 
        ],
        'ticket': [1, '', '', {'has_patch': 1, 'type': 'Bug', 'component': '',\
                'resolution': '', 'severity': ''}],
    },
    2: {
        'change': [
            [datetime(2010, 02, 02, 10, 0, 0, 0), 'testuser', 'comment', '', '', 1], 
            [datetime(2011, 02, 02, 10, 0, 0, 0), 'testuser', 'comment', '', '', 1], 
        ],
        'ticket': [2, '', '', {'has_patch': 0, 'type': 'Bug', 'component': '',\
                'resolution': '', 'severity': ''}],
    }        
}
