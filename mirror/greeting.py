import logging
import uuid

def insert_item(mirror_service):
    '''Insert a greeting into the timeline.'''
    body = {
        'notification': {'level': 'DEFAULT'},
        'creator': {
            'displayName': 'Glass Eats',
            'id':'Glass Eats'
        },

        'html':'<article class=\"photo\">\n<img src=\"https://glasseats.appspot.com/static/images/GlassHomeScreen.png?r='+str(uuid.uuid1()).replace('-','')+'\" width=\"100%\" height=\"100%\">\n  <div class=\"photo-overlay\"/>\n  <section>\n</section>\n</article>\n',
        'menuItems': [
            {'action':'TOGGLE_PINNED'},
            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Nearby', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Nearby.png'}], 'id':'nearby'},
            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Burgers', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Burger.png'}], 'id':'burgers'},
            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Mexican', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Mexican.png'}], 'id':'mexican'},

            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Italian', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Italian.png'}], 'id':'italian'},
            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Greek', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Greek.png'}], 'id':'greek'},
            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Chinese', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Chinese.png'}], 'id':'chinese'},
            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Japanese', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Japanese.png'}], 'id':'japanese'},
            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Korean', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Korean.png'}], 'id':'korean'},
            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Thai', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Thai.png'}], 'id':'thai'},
            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Vegetarian', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Vegetarian.png'}], 'id':'vegetarian'},
            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Brunch', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Breakfast_Brunch.png'}], 'id':'breakfast & brunch'},
            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Cafes', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Cafe.png'}], 'id':'cafes'},
            {'action':'CUSTOM', 'values':[{'state':'DEFAULT', 'displayName':'Pizza', 'iconUrl':'https://glasseats.appspot.com/static/images/menu_icons/Pizza.png'}], 'id':'pizza'},
            {'action':'DELETE'}
        ]

    }

    logging.info('body : %s' % body)
    mirror_service.timeline().insert(body=body).execute()
    return 'A greeting has been sent'
