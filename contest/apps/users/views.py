from django.template import Context, loader, RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from contest.apps.contests.models import Entry

def user(request, user_id):
    p = User.objects.filter(id=user_id)
    e = Entry.objects.filter(user=p[0])
    return render_to_response('users/user.html', {'theuser': p[0], 'entries': e}, context_instance=RequestContext(request))

def loginformContextProcessor(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
    request.session.set_test_cookie()
    return {'path': request.path}