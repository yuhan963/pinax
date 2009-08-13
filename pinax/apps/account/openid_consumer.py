
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

from django_openid.registration import RegistrationConsumer

from account.forms import OpenIDSignupForm
from account.utils import get_default_redirect
from account.views import login as account_login

class PinaxConsumer(RegistrationConsumer):
    
    # Pinax does its own e-mail confirmation handling, but django-openid
    # wants to do its own handling of this so we turn it off in all cases
    confirm_email_addresses = False
    
    def on_registration_complete(self, request):
        return HttpResponseRedirect(get_default_redirect(request))
    
    def show_i_have_logged_you_in(self, request):
        return HttpResponseRedirect(get_default_redirect(request))
    
    def get_registration_form_class(self, request):
        return OpenIDSignupForm
    
    def do_register(self, request, *args, **kwargs):
        """
        A small wrapper around django_openid's implementation of registration
        that redirects back to a certain URL if there's no openid_url in the
        POST body.
        """
        openid_url = request.POST.get('openid_url')
        openids = request.session.get('openids')
        if not openid_url and not openids:
            return account_login(request, url_required=True)
        return super(PinaxConsumer, self).do_register(request, *args, **kwargs)