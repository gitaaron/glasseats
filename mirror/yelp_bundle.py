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
    for i in xrange(1):
        #body['bundleId'] = str(uuid.uuid1())
        #body['bundleId'] = 'bundleId1'
        #body['isBundleCover'] = is_first
        is_first = False
        if food_type:
            body['text']='%s : %s' % (food_type, response.values()[2][i]['name'])
        else: 
            body['text']=response.values()[2][i]['name']


        mirror_service.timeline().insert(body=body).execute()


    logging.info('zip3')



def insert_handler(mirror_service, food_type=None):
    '''Inserting the yelp bundle into the timeline'''
    logging.info('insert_handler')
    taskqueue.add(url='/', params={'operation':'insertYelpBundleWithFoodType'})

    return 'The bundle item has been inserted'
