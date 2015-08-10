import webapp2
from google.appengine.ext import ndb
import models
import json
from utils import authenticate

class TenantHandler(webapp2.RequestHandler):
    @authenticate
    def post(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = 'Only accepts application/json.'
            return

        if 'lid' not in kwargs:
            self.response.status = 400
            self.response.status_message = 'A location must be specified.'
            return
        try:
            int(kwargs['lid'])
        except:
            self.response.status = 406
            self.response.status_message = 'the location URI must be a integer'
            return

        if 'uid' not in kwargs:
            self.response.status = 400
            self.response.status_message = 'A unit must be specified.'
            return
        try:
            int(kwargs['uid'])
        except:
            self.response.status = 406
            self.response.status_message = 'the unit URI must be a integer'
            return

        occupants = self.request.get('occupants', default_value=None)
        notes = self.request.get('notes', default_value=None)
        payment_history = self.request.get('payment_history', default_value=None)
        new_tenant = models.Tenant(parent=ndb.Key(models.Location, int(kwargs['lid']), models.Unit, int(kwargs['uid'])))
        if occupants:
            new_tenant.occupants = occupants
        else:
            self.response.status = 400
            self.response.status_message = 'Tenant requires a occupants'
            self.response.write('tenant requires a occupants')
            return
        if notes:
            new_tenant.notes = notes
        if payment_history:
            new_tenant.payment_history = payment_history

        key = new_tenant.put()
        out = new_tenant.to_dict()
        self.response.write(json.dumps(out))

    @authenticate
    def get(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = 'Only accepts application/json.'
            return

        if 'lid' not in kwargs:
            self.response.status = 400
            self.response.status_message = 'A location must be specified.'
            return
        try:
            int(kwargs['lid'])
        except:
            self.response.status = 406
            self.response.status_message = 'the location URI must be a integer'
            return
        if 'uid' not in kwargs:
            self.response.status = 400
            self.response.status_message = 'A unit must be specified.'
            return
        try:
            int(kwargs['uid'])
        except:
            self.response.status = 406
            self.response.status_message = 'the unit URI must be a integer'
            return
        if 'tid' in kwargs:
            try:
                int(kwargs['tid'])
            except:
                self.response.status = 406
                self.response.status_message = 'the tenant URI must be a integer'
                return
            out = ndb.Key(models.Location, int(kwargs['lid']), models.Unit, int(kwargs['uid']), models.Tenant, int(kwargs['tid'])).get().to_dict()
            self.response.write(json.dumps(out))
        else:
            query = models.Tenant.query(ancestor=ndb.Key(models.Location, int(kwargs['lid']), models.Unit, int(kwargs['uid'])))
            entities = query.fetch()
            results = {'tenants': [tenant.to_dict() for tenant in entities ]}
            self.response.write(json.dumps(results))

    @authenticate
    def put(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = 'Only accepts application/json.'
            return

        occupants = self.request.get('occupants', default_value=None)
        notes = self.request.get('notes', default_value=None)
        payment_history = self.request.get('payment_history', default_value=None)
        if 'lid' not in kwargs:
            self.response.status = 400
            self.response.status_message = 'A location must be specified.'
            return
        if 'uid' not in kwargs:
            self.response.status = 400
            self.response.status_message = 'A unit must be specified.'
            return
        if 'tid' not in kwargs:
            self.response.status = 400
            self.response.status_message = 'A tenant must be specified.'
            return
        out = ndb.Key(models.Location, int(kwargs['lid']), models.Unit, int(kwargs['uid']), models.Tenant, int(kwargs['tid'])).get()
        if occupants:
            out.occupants = occupants
        if notes:
            out.notes = notes
        if payment_history:
            out.payment_history = payment_history
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
        if 'uid' not in kwargs:
            self.response.status = 400
            self.response.status_message = 'A unit must be specified.'
            return
        if 'tid' not in kwargs:
            self.response.status = 400
            self.response.status_message = 'A tenant must be specified.'
            return
        key = ndb.Key(models.Location, int(kwargs['lid']), models.Unit, int(kwargs['uid']), models.Tenant, int(kwargs['tid']))
        ndb.delete_multi(ndb.Query(ancestor=key).iter(keys_only = True))
        key.delete()

