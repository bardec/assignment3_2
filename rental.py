import webapp2
from google.appengine.api import oauth

app = webapp2.WSGIApplication([
    ], debug=True)
app.router.add(webapp2.Route(r'/location/<username>&<password>', 'location.LocationHandler'))
app.router.add(webapp2.Route(r'/location/<lid:[0-9]+>/<username>&<password>', 'location.LocationHandler'))
app.router.add(webapp2.Route(r'/location/<lid:[0-9]+>/unit/<uid:[0-9]+>/<username>&<password>', 'unit.UnitHandler'))
app.router.add(webapp2.Route(r'/location/<lid:[0-9]+>/unit/<username>&<password>', 'unit.UnitHandler'))
app.router.add(webapp2.Route(r'/location/<lid:[0-9]+>/unit/<uid:[0-9]+>/tenant/<tid:[0-9]+>/<username>&<password>', 'tenant.TenantHandler'))
app.router.add(webapp2.Route(r'/location/<lid:[0-9]+>/unit/<uid:[0-9]+>/tenant/<username>&<password>', 'tenant.TenantHandler'))
app.router.add(webapp2.Route(r'/user/', 'user.UserHandler'))
