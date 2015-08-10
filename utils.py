import webapp2
from google.appengine.ext import ndb
from models import User, Location, Tenant, Unit

def authenticate(f):
    def wrapper(self, *args, **kwargs):
        if ('username' or 'password') not in kwargs:
            self.abort(401)

        results = User.query(User.username == kwargs['username'],
                    User.password == kwargs['password']).fetch(1)
        if len(results) == 0:
            self.abort(401)
        user = results[0]
        key = None

        #check to make sure that the resource is something thye can check
        if user.role == 'manager':
            #can access all units and tenants related to lid
            key = ndb.Key(Location, int(kwargs['lid']))
        elif user.role == 'tenant':
            #can access all tenants related to lid, uid, tid
            try:
                key = ndb.Key(Location, int(kwargs['lid']),
                        Unit, int(kwargs['uid']),
                        Tenant, int(kwargs['tid']))
            except Exception:
                return self.abort(401)
        if user.related_key != key:
            return self.abort(402)
        return f(self, **kwargs)
    return wrapper
