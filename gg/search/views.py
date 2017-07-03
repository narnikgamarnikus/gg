import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    suggestions = {
    	str(result.object) : result.object.get_absolute_url() for result in sqs
    }
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
    	'results': suggestions
    })
    print(the_data)
    return HttpResponse(the_data, content_type='application/json')