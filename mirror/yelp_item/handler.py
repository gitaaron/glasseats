import webapp2
import yelp_bundle
import logging
import util
from oauth2client.appengine import StorageByKeyName
from model import Credentials


class YelpItem(webapp2.RequestHandler):

    def post(self):
        userid = self.request.get('user_id')
        food_type = self.request.get('food_type')
        logging.info('YelpItemWorker userid : %s fooditem : %s' % (userid, food_type))
        logging.info('YelpItemWorker boyd : %s' % self.request.body)
        self.response.write('ok : %s' % userid)

        mirror_service = util.create_service(
            'mirror', 'v1',
            StorageByKeyName(Credentials, userid, 'credentials').get())
        yelp_bundle.insert_worker(mirror_service, food_type)


YELP_ITEM_ROUTES = [
    ('/yelp_item', YelpItem)
]
