from django.template import Context, loader, RequestContext
from contest.apps.contests.models import Contest, Entry, Score
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect

def index(request):
    contest_list = Contest.objects.all().order_by('-start_date')
    return render_to_response('contests/contests.html', {'contest_list': contest_list}, context_instance=RequestContext(request))

def detail(request, contest_id):
    p = get_object_or_404(Contest, pk=contest_id)
    r = Entry.objects.filter(contest=p)
    from datetime import date
    if date.today() > p.judge_date:
        showWinner = True
    else:
        showWinner = False
    
    return render_to_response('contests/contest_detail.html', {'contest': p, 'entries': r}, context_instance=RequestContext(request))

def entry(request, entry_id):
    from image_thumb import thumbnail
    p = get_object_or_404(Entry, pk=entry_id)
    scores = Score.objects.filter(entry=p)
    try:
        thumb = thumbnail(p.screenshot)
    except:
        thumb = p.screenshot

    return render_to_response('contests/entry_detail.html', {'entry': p, 'scores': scores, 'thumb': thumb}, context_instance=RequestContext(request))

def rules(request):
    return render_to_response('contests/contest_rules.html', {}, context_instance=RequestContext(request))

def judge(request):
    return render_to_response('contests/judge_entry.html', {}, context_instance=RequestContext(request))

def submit(request):
    from forms import MapUploadForm
    if request.POST and request.user.is_authenticated():
        request.POST['user'] = request.user.id
        data = request.POST.copy()
        data.update(request.FILES)
        form = MapUploadForm(data)
        if form.is_valid():
            p = form.save()
            return HttpResponseRedirect('/contests/entry/%s/' % p)
        else:
            from datetime import date
            d=date.today()
            contest = Contest.objects.filter(start_date__lte=d).filter(end_date__gte=d)
            return render_to_response('contests/submit_entry.html', {'form_as_table': form, 'form': form, 'contests': contest}, context_instance=RequestContext(request))
        
    else:
        from datetime import date
        d=date.today()
        contest = Contest.objects.filter(start_date__lte=d).filter(end_date__gte=d)
        form = MapUploadForm()
        return render_to_response('contests/submit_entry.html', {'form_as_table': form.as_p(), 'form': form, 'contests': contest}, context_instance=RequestContext(request))
