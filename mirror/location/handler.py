import webapp2
import util

class LocationHandler(webapp2.RequestHandler):
    '''Request Handler to retrieve user\'s location'''

    @util.auth_required
    def get(self):
        location = self.mirror_service.locations().get(id='latest').execute()
        self.response.out.write('location %s' % location)


LOCATION_ROUTES = [
    ('/location', LocationHandler)
]
