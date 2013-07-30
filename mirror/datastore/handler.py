import webapp2
import util

from model import UserActions

class DataStoreHandler(webapp2.RequestHandler):
    def get(self):
        s = UserActions(user_action_id='asdf')
        k = s.put()

        new_entry = UserActions.get_by_id('ag1kZXZ-Z2xhc3NlYXRzchgLEgtVc2VyQWN0aW9ucxiAgICAgICACww')

        self.response.out.write('datastore len : %s'%len(new_entry))



DATASTORE_ROUTES = [
    ('/datastore', DataStoreHandler)
]
