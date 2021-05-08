from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.
def input_user(request):
    return render(request, "recommender/input_user.html")

def recommendations(request):
    user_id = request.GET.get('user_id', '')
    if user_id == '' or int(user_id) <= 0:
        return HttpResponseRedirect('/user/')
    # TODO: get real recommendations
    movies = {1: ['Star Wars', 2020], 2: ['Shooter', 2008]}
    context = {
        'movies':movies,
        'user_id':user_id
    }
    return render(request, "recommender/recommendations.html", context)