from google.appengine.api import taskqueue
import webapp2
import logging

class QueueHandler(webapp2.RequestHandler):
    def get(self):
        taskqueue.add(url='/queue_worker', params={})
        self.response.out.write('ok')

class QueueWorker(webapp2.RequestHandler):
    def post(self): 
        logging.info('worker called')
        self.response.out.write('ok')



QUEUE_ROUTES = [
    ('/queue_worker', QueueWorker),
    ('/queue_handler', QueueHandler)
]
