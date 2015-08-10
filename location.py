import webapp2
from google.appengine.ext import ndb
import models
import json
from utils import authenticate


class LocationListHandler(webapp2.RequestHandler):
    @authenticate
    def get(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = 'Only accepts application/json.'
            return

        query = models.Location.query()
        entities = query.fetch()
        results = {'locations': [{'address': loc.address, 'key': loc.key.id()} for loc in entities] }
        self.response.write(json.dumps(results))


class LocationHandler(webapp2.RequestHandler):
    @authenticate
    def post(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = 'Only accepts application/json.'
            return

        address = self.request.get('address', default_value=None)
        number_of_units = self.request.get('number_of_units', default_value=None)
        new_location = models.Location()
        if address:
            new_location.address = address
        else:
            self.response.status = 400
            self.response.status_message = 'Location requires an address'
            return
        if number_of_units:
            new_location.number_of_units = int(number_of_units)
        else:
            self.response.status = 400
            self.response.status_message = 'Location requires a number_of_units'
            return
        key = new_location.put()
        out = new_location.to_dict()
        self.response.write(json.dumps(out))

    @authenticate
    def get(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = 'Only accepts application/json.'
            return

        if 'lid' in kwargs:
            out = ndb.Key(models.Location, int(kwargs['lid'])).get().to_dict()
            self.response.write(json.dumps(out))
        else:
            query = models.Location.query()
            entities = query.fetch()
            results = {'locations': [loc.to_dict() for loc in entities] }
            self.response.write(json.dumps(results))

    @authenticate
    def put(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = 'Only accepts application/json.'
            return

        address = self.request.get('address', default_value=None)
        number_of_units = self.request.get('number_of_units', default_value=None)
        if 'lid' not in kwargs:
            self.response.status = 400
            self.response.status_message = 'A location must be specified.'
            return
        out = ndb.Key(models.Location, int(kwargs['lid'])).get()
        if address:
            out.address = address
        if number_of_units:
            out.number_of_units = number_of_units
        out.put()
        self.response.write(json.dumps(out.to_dict()))

    @authenticate
    def delete(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = 'Only accepts application/json.'
            return

        if 'lid' not in kwargs:
            self.response.status = 400
            self.response.status_message = 'A location must be specified.'
            return
        key = ndb.Key(models.Location, int(kwargs['lid']))
        ndb.delete_multi(ndb.Query(ancestor=key).iter(keys_only = True))
        key.delete()

