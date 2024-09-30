from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .form_news import NewsForm
from . import dataMapper_news

def get_all_news(request):
    all_news = dataMapper_news.NewsMapper().get_all_news()
    if len(all_news) != 0:
        news_list = [
            {
                'id': one_news[0],
                'title': one_news[1],
                'description': one_news[2],
                'date': one_news[3],
                'createdAt': one_news[4],
                'updatedAt': one_news[5],
            } for one_news in all_news
        ]
        return JsonResponse(news_list, safe=False)
    else:
        return JsonResponse({'error': 'News not found'}, status=404)


def get_one_news(request, news_id):
    one_news = dataMapper_news.NewsMapper().get_news_by_id(news_id)
    if one_news:
        news_data = {
            'id': one_news[0],
            'title': one_news[1],
            'description': one_news[2],
            'date': one_news[3],
            'createdAt': one_news[4],
            'updatedAt': one_news[5],
        }
        return JsonResponse(news_data, safe=False)
    else:
        return JsonResponse({'error': 'News not found'}, status=404)


@csrf_exempt
def create_news(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = NewsForm(data)

            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                date = form.cleaned_data['date']

                news_id = dataMapper_news.NewsMapper().create_news(
                    title=title, description=description, date=date
                )
                return JsonResponse({'news_id': news_id, 'message': 'News created successfully'})
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def update_news(request, news_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            form = NewsForm(data)

            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                date = form.cleaned_data['date']

                result = dataMapper_news.NewsMapper().update_news(
                    news_id, title, description, date
                )
                return JsonResponse(result)
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_news(request, news_id):
    if request.method == 'DELETE':
        result = dataMapper_news.NewsMapper().delete_news(news_id)
        return JsonResponse(result)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
