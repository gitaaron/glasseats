import logging

def insert_item(mirror_service):
    '''Insert a greeting into the timeline.'''
    body = {
        'notification': {'level': 'DEFAULT'},
        'creator': {
            'displayName': 'Glass Eats',
            'id':'Glass Eats'
        },
        'html': '<div style="color"white">Welcome to Glass Eats. Pin this card to your timeline. Tap to search restaurants nearby or by restaurant type.,/div>',


        'html':'<article class=\"photo\">\n<img src=\"https://glasseats.appspot.com/static/images/GlassHomeScreen.png\" width=\"100%\" height=\"100%\">\n  <div class=\"photo-overlay\"/>\n  <section>\n    <p class=\"text-auto-size\">Welcome to Glass Eats. Pin this card to your timeline. Tap to search restaurants nearby or by restaurant type.</p>\n  </section>\n</article>\n',
        'menuItems': [
            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Nearby', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Nearby.png'}], 'id':'nearby'},
            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Burgers', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Burger.png'}], 'id':'burgers'},
            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Mexican', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Mexican.png'}], 'id':'mexican'},

            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Pizza', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Pizza.png'}], 'id':'pizza'},
            {'action':'DELETE'}
        ]

    }

    logging.info('body : %s' % body)
    mirror_service.timeline().insert(body=body).execute()
    return 'A greeting has been sent'
