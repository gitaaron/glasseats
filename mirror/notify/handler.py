# Copyright (C) 2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Request Handler for /notify endpoint."""

__author__ = 'alainv@google.com (Alain Vongsouvanh)'


import io
import json
import logging
import webapp2

from apiclient.http import MediaIoBaseUpload
from oauth2client.appengine import StorageByKeyName

from model import Credentials
import util

import yelp_bundle


class NotifyHandler(webapp2.RequestHandler):
  """Request Handler for notification pings."""

  def post(self):
    """Handles notification pings."""
    logging.info('Got a notification with payload %s', self.request.body)
    data = json.loads(self.request.body)
    userid = data['userToken']
    self.userid = userid
    # TODO: Check that the userToken is a valid userToken.
    self.mirror_service = util.create_service(
        'mirror', 'v1',
        StorageByKeyName(Credentials, userid, 'credentials').get())
    if data.get('collection') == 'locations':
      self._handle_locations_notification(data)
    elif data.get('collection') == 'timeline':
      self._handle_timeline_notification(data)

  def _handle_locations_notification(self, data):
    """Handle locations notification."""
    location = self.mirror_service.locations().get(id=data['itemId']).execute()
    text = 'New location is %s, %s' % (location.get('latitude'),
                                       location.get('longitude'))
    body = {
        'text': text,
        'location': location,
        'menuItems': [{'action': 'NAVIGATE'}],
        'notification': {'level': 'DEFAULT'}
    }
    self.mirror_service.timeline().insert(body=body).execute()

  def _handle_timeline_notification(self, data):
    """Handle timeline notification."""
    for user_action in data.get('userActions', []):
      if user_action.get('type') == 'SHARE':
        # Fetch the timeline item.
        item = self.mirror_service.timeline().get(id=data['itemId']).execute()
        attachments = item.get('attachments', [])
        media = None
        if attachments:
          # Get the first attachment on that timeline item and do stuff with it.
          attachment = self.mirror_service.timeline().attachments().get(
              itemId=data['itemId'],
              attachmentId=attachments[0]['id']).execute()
          resp, content = self.mirror_service._http.request(
              attachment['contentUrl'])
          if resp.status == 200:
            media = MediaIoBaseUpload(
                io.BytesIO(content), attachment['contentType'],
                resumable=True)
          else:
            logging.info('Unable to retrieve attachment: %s', resp.status)
        body = {
            'text': 'Echoing your shared item: %s' % item.get('text', ''),
            'notification': {'level': 'DEFAULT'}
        }
        self.mirror_service.timeline().insert(
            body=body, media_body=media).execute()
        # Only handle the first successful action.
        break

      if user_action.get('type') == 'REPLY':
        reply_id = data['itemId']
        result = self.mirror_service.timeline().get(id=reply_id).execute()
        origional_txt = result.get('text')
        logging.info('REPLY : %s' % origional_txt)

      elif user_action.get('type') == 'CUSTOM' and user_action.get('payload') == 'nearby':
        logging.info('CUSTOM nearby user_id : %s' % self.userid)
        yelp_bundle.insert_handler('food', self.userid)
      
      else:
        logging.info(
            "CUSTOM it must have a food type: %s", user_action)
        logging.info('CUSTOM user_id : %s' % self.userid)

        yelp_bundle.insert_handler(user_action.get('payload'), self.userid)




  def _insert_item(self):
    """Insert a timeline item."""
    logging.info('Inserting timeline item')
    body = {
        'notification': {'level': 'DEFAULT'}
    }

    response = search_yelp.make_request()

    body['text'] = response.values()[2][0]['name']

    media = None

    # self.mirror_service is initialized in util.auth_required.
    self.mirror_service.timeline().insert(body=body, media_body=media).execute()
    return  'A timeline item has been inserted.'


NOTIFY_ROUTES = [
    ('/notify', NotifyHandler)
]
