import webapp2
from google.appengine.ext import ndb
import models
import json
from utils import authenticate

class UnitHandler(webapp2.RequestHandler):
    @authenticate
    def post(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = 'Only accepts application/json.'
            return

        if 'lid' not in kwargs:
            self.response.status = 400
            self.response.status_message = 'lid must be specified'

        try:
            int(kwargs['lid'])
        except:
            self.response.status = 406
            self.response.status_message = 'the location URI must be a integer'

        unit_number = self.request.get('unit_number', default_value=None)
        cost_per_month = self.request.get('cost_per_month', default_value=None)
        avg_climate_control_per_month = self.request.get('avg_climate_control_per_month', default_value=None)
        features = self.request.get('features', default_value=None)
        new_unit = models.Unit(parent=ndb.Key(models.Location, int(kwargs['lid'])))
        if unit_number:
            try:
                new_unit.unit_number = int(unit_number)
            except Exception:
                self.response.status = 406
                self.response.status_message = 'unit_number must be an integer'
        else:
            self.response.status = 400
            self.response.status_message = 'Unit requires a unit_number'
        if cost_per_month:
            try:
                new_unit.cost_per_month = float(cost_per_month)
            except Exception:
                self.response.status = 406
                self.response.status_message = 'cost_per_month must be a float'
                return
        if avg_climate_control_per_month:
            try:
                new_unit.avg_climate_control_per_month = float(avg_climate_control_per_month)
            except Exception:
                self.response.status = 406
                self.response.status_message = 'avg_climate_control_per_month must be a float'
        if features:
            new_unit.features = features

        key = new_unit.put()
        out = new_unit.to_dict()
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

        if 'uid' in kwargs:
            try:
                int(kwargs['uid'])
            except:
                self.response.status = 406
                self.response.status_message = 'the location URI must be a integer'
                return
            out = ndb.Key(models.Location, int(kwargs['lid']), models.Unit, int(kwargs['uid'])).get().to_dict()
            self.response.write(json.dumps(out))
        else:
            query = models.Unit.query(ancestor=ndb.Key(models.Location, int(kwargs['lid'])))
            entities = query.fetch()
            results = {'units': [unit.to_dict() for unit in entities] }
            self.response.write(json.dumps(results))

    @authenticate
    def put(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = 'Only accepts application/json.'
            return

        unit_number = self.request.get('unit_number', default_value=None)
        cost_per_month = self.request.get('cost_per_month', default_value=None)
        avg_climate_control_per_month = self.request.get('avg_climate_control_per_month', default_value=None)
        features = self.request.get('features', default_value=None)
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
            self.response.status_message = 'A user must be specified.'
            return
        try:
            int(kwargs['uid'])
        except:
            self.response.status = 406
            self.response.status_message = 'the location URI must be a integer'
            return

        out = ndb.Key(models.Location, int(kwargs['lid']), models.Unit, int(kwargs['uid'])).get()
        if unit_number:
            try:
                out.unit_number = int(unit_number)
            except:
                self.response.status = 406
                self.response.status_message = 'unit_number must be an int'
        if cost_per_month:
            try:
                out.cost_per_month = float(cost_per_month)
            except:
                self.response.status = 406
                self.response.status_message = 'cost_per_month must be an int'
        if avg_climate_control_per_month:
            try:
                out.avg_climate_control_per_month = float(avg_climate_control_per_month)
            except:
                self.response.status = 406
                self.response.status_message = 'avg_climate_control_per_month must be an int'
        if features:
            out.features = features
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
        try:
            int(kwargs['lid'])
        except:
            self.response.status = 406
            self.response.status_message = 'the location URI must be a integer'
            return

        if 'uid' not in kwargs:
            self.response.status = 400
            self.response.status_message = 'A user must be specified.'
            return
        try:
            int(kwargs['lid'])
        except:
            self.response.status = 406
            self.response.status_message = 'the unit URI must be a integer'
            return

        key = ndb.Key(models.Location, int(kwargs['lid']), models.Unit, int(kwargs['uid']))
        ndb.delete_multi(ndb.Query(ancestor=key).iter(keys_only = True))
        key.delete()
