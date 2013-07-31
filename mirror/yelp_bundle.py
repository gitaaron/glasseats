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
            resto = response.values()[2][i]
            try:
                image_url = resto['image_url'].replace('ms.jpg', 'l.jpg')
            except KeyError:
                image_url = None
            address = resto['location']['display_address'][0] +','+resto['location']['city']
            category = resto['categories'][0][0]
            phone_number = resto['phone']
            rating_url = resto['rating_img_url']
            if image_url:
                if food_type:
                    body['html'] = '<article class=\"photo\">\n<img src=\"' + image_url + '\" width=\"100%\" height=\"100%\">\n  <div class=\"photo-overlay\"/>\n  <section>\n    <p class=\"align-center text-auto-size\">' + resto['name'] + '<br />Category: '+category+'<br />'+address+'<br/>'+phone_number+'<br/><img src=\"'+rating_url+'\" /></p>\n  </section>\n</article>\n'

                else: 
                    body['html'] = '<article class=\"photo\">\n<img src=\"' + image_url + '\" width=\"100%\" height=\"100%\">\n  <div class=\"photo-overlay\"/>\n  <section>\n    <p class=\"align-center text-auto-size\">' + resto['name'] + '<br />'+address+'<br/>'+phone_number+'<br/><img src=\"'+rating_url+'\" /></p>\n  </section>\n</article>\n'
            else:
                if food_type:
                    body['html'] = '<article class=\"photo\">\n <div class=\"photo-overlay\"/>\n  <section>\n    <p class=\"align-center text-auto-size\">' + resto['name'] + '<br />Category: '+category+'<br />'+address+'<br/>'+phone_number+'<br/><img src=\"'+rating_url+'\" /></p>\n  </section>\n</article>\n'

                else: 
                    body['html'] = '<article class=\"photo\">\n <div class=\"photo-overlay\"/>\n  <section>\n    <p class=\"align-center text-auto-size\">' + resto['name'] + '<br />'+address+'<br/>'+phone_number+'<br/><img src=\"'+rating_url+'\" /></p>\n  </section>\n</article>\n'



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
