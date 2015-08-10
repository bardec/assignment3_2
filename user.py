from models import Unit, Location, Tenant, User
import webapp2
from google.appengine.ext import ndb
import json

class UserHandler(webapp2.RequestHandler):
    def post(self, **kwargs):
        role = self.request.get('role', default_value=None)
        tenantKey = self.request.get('tenant_key', default_value=None)
        unitKey = self.request.get('unit_key', default_value=None)
        locationKey = self.request.get('location_key', default_value = None)
        username = self.request.get('username', default_value=None)
        password = self.request.get('password', default_value=None)
        if not all([role,locationKey,username,password]):
            self.abort(400)
        if role == 'tenant' and not tenantKey:
            self.abort(400)
        key = None
        if role == 'tenant':
            key = ndb.Key(Location, int(locationKey),
                    Unit, int(unitKey),
                    Tenant, int(tenantKey))
        elif role == 'manager':
            key = ndb.Key(Location, int(locationKey))
        else:
            self.response.status = 400
            self.response.status_message = 'Role must be either tenant or manager.'

        user = User()
        try:
            user.role = role
            user.related_key = key
            user.username = username
            user.password = password
            user.put()
        except Exception as msg:
            self.abort(500, details=msg)
            return
        self.response.write(json.dumps(user.to_dict()))


