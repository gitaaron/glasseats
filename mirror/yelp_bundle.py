import logging
import search_yelp
import uuid
from apiclient import errors
from google.appengine.api import taskqueue



def insert_worker(mirror_service, food_type=None):

    try:
        location = mirror_service.locations().get(id='latest').execute()
        latlong = '%s,%s' % (location.get('latitude'), location.get('longitude'))
    except errors.HttpError, e:
        latlong = None

    logging.info('location %s' % latlong)

    response = search_yelp.make_request(latlong, term=food_type)

    body = { 
        'menuItems': [
            {'action':'DELETE'}
        ]
    }

    is_first = True



    for i in xrange(10):
        body['bundleId'] = str(uuid.uuid1()).replace('-','')
        #body['bundleId'] = 'bundleId3'
        body['isBundleCover'] = is_first


        if is_first:
            body['html'] = '<article class=\"photo\">\n<img src=\"https://glasseats.appspot.com/static/images/GlassHomeRestaurantResults.png\" width=\"100%\" height=\"100%\">\n  <div class=\"photo-overlay\"/>\n  <section>\n</section>\n</article>\n'

        else:
            if food_type:
                body['text']='%s : %s' % (food_type, response.values()[2][i]['name'])
            else: 
                body['text']=response.values()[2][i]['name']

        is_first = False

        mirror_service.timeline().insert(body=body).execute()

        try:
            del body['html']
        except KeyError:
            pass
        try:
            del body['text']
        except KeyError:
            pass


    logging.info('zip3')



def insert_handler(food_type, user_id):
    '''Inserting the yelp bundle into the timeline'''
    taskqueue.add(url='/yelp_item', params={'user_id':user_id, 'food_type':food_type})

    return 'The bundle item has been inserted'
