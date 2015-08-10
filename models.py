from google.appengine.ext import ndb

class Model(ndb.Model):
    def to_dict(self):
        d = super(Model, self).to_dict()
        d['key'] = self.key.id()
        return d

class Location(Model):
    address = ndb.StringProperty(required=True)
    number_of_units = ndb.IntegerProperty(required=True)

class Unit(Model):
    unit_number = ndb.IntegerProperty(required=True)
    cost_per_month = ndb.FloatProperty(required=False)
    avg_climate_control_per_month = ndb.FloatProperty(required=False)
    features = ndb.StringProperty()

class Tenant(Model):
    occupants = ndb.StringProperty(required=True)
    notes = ndb.StringProperty()
    payment_history = ndb.StringProperty()

class User(Model):
    role = ndb.StringProperty(required=True, choices=['manager','tenant'])
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    related_key = ndb.KeyProperty()

    def to_dict(self):
        d = super(Model, self).to_dict()
        d['related_key'] = self.related_key.id()
        return d
