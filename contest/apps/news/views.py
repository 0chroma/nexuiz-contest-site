from django.template import Context, loader, RequestContext
from contest.apps.news.models import Item
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404

def index(request):
    news_list = Item.objects.all().order_by('-pub_date')[:5]
    return render_to_response('news/news_index.html', {'news_list': news_list}, context_instance=RequestContext(request))

def item(request, id):
    item = get_object_or_404(Item, pk=id)
    return render_to_response('news/news_item.html', {'entry': item}, context_instance=RequestContext(request))