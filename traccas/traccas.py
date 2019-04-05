# CASified login module for Trac

from trac.core import *
from trac.config import Option
from trac.web.api import IAuthenticator, IRequestHandler
from trac.web.chrome import INavigationContributor
from trac.util import escape, hex_entropy, Markup
from trac.web.auth import LoginModule
from genshi.builder import tag

from pycas import PyCAS

class CasLoginModule(LoginModule):
    """A CAS-based login module."""
    
    server = Option('cas', 'server', doc='Base URL for the CAS server')
    login_path = Option('cas', 'login_path', default='/login', 
                        doc='Path component for the login system')
    logout_path = Option('cas', 'logout_path', default='/logout', 
                        doc='Path component for the logout system')
    validate_path = Option('cas', 'validate_path', default='/validate', 
                        doc='Path component for the validation system')
        
    # IAuthenticatorMethods
    def authenticate(self, req):
        ticket = req.args.get('ticket')
        if ticket:
            valid, user = self.cas.validate_ticket(req.abs_href.login(), ticket)
            if valid:
                req.environ['REMOTE_USER'] = user
                
        return super(CasLoginModule, self).authenticate(req)
        
    # INavigationContributor methods
    def get_navigation_items(self, req):        
        if req.authname and req.authname != 'anonymous':
            yield 'metanav', 'login', 'logged in as %s' % req.authname
            yield 'metanav', 'logout', tag.a('Logout', href=req.href.logout())
        else:
            yield 'metanav', 'login', tag.a('Login', href=self.cas.login_url(req.abs_href.login()))

    # Internal methods
    def _do_login(self, req):
        if not req.remote_user:
            req.redirect(self.cas.login_url(req.abs_href.login()))
        super(CasLoginModule, self)._do_login(req)

    def _do_logout(self, req):
        if req.authname:
            super(CasLoginModule, self)._do_logout(req)
            req.redirect(self.cas.logout_url(req.abs_href()))
        else:
            req.redirect(req.abs_href())
    
    def cas(self):
        paths = {
            'login_path': self.login_path,
            'logout_path': self.logout_path,
            'validate_path': self.validate_path,
        }
        return PyCAS(self.server, **paths)
    cas = property(cas)
