#import simplejson as json
import ujson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    suggestions = [
    	{
    	"id" : result.object.pk, 
    	"title" : result.object.__str__(), 
    	"link" : result.object.get_absolute_url()
    	} for result in sqs
    ]

    return HttpResponse(json.dumps(suggestions), content_type='application/json')