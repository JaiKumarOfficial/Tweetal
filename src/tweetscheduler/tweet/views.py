from django.shortcuts import render, get_object_or_404, redirect
from .models import Users, Template, DmUserList, Tweet
from .forms import UserLoginForm, PostTweet, Search, DmForm, TemplateForm, DmUserListForm
from django.http import HttpResponse, HttpResponseRedirect
import twitter, datetime, json, tweepy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from .serializers import DmUserListSerializer
# Create your views here.


def homepage(request):
    return render(request, "homepage.html", {})


def user_login(request):

    if request.method == 'POST':

        form = UserLoginForm(request.POST)
        if form.is_valid():
            print("working")
            person = form.save(commit=False)
            person.user = form.cleaned_data['name']
            person.con_key = form.cleaned_data['consumer_key']
            person.con_sec_key = form.cleaned_data['consumer_secret_key']
            person.acc_tok = form.cleaned_data['access_token']
            person.acc_sec_tok = form.cleaned_data['access_secret_token']
            api = twitter.Api(consumer_key=person.con_key,
                              consumer_secret=person.con_sec_key,
                              access_token_key=person.acc_tok,
                              access_token_secret=person.acc_sec_tok)
            try:
                api.VerifyCredentials()
                person.save()
                print("redirect next")
                return redirect('login_detail', pk=person.pk)
            except twitter.error.TwitterError:
                return render(request, 'login_error.html', {})

    else:
        print("else working")
        form = UserLoginForm()
        return render(request, 'user_login_input.html', {'user_login_input': form})


def user_details_output(request, pk):
    person = get_object_or_404(Users, pk=pk)
    return render(request, 'login_details.html', {'person': person})


def no_user_found(request):
    return render(request, 'no_user_found.html', {})


def post_tweet(request):
    if len(Users.objects.all()) <= 0:
        return redirect('no_user_found')

    else:
        form = PostTweet()
        return render(request, 'post_tweet.html', {'post_tweet': form})


def user_list(request):
    if len(Users.objects.all()) > 0:
        user = Users.objects.all()
        return render(request, 'users_list.html', {'user': user})
    else:
        return redirect('no_user_found')


def user_delete(request, pk):
    user = get_object_or_404(Users, pk=pk)
    user.delete()
    return redirect('user_list')


def fetch_user():
    get_user = Users.objects.all()[0]
    twitter_api = twitter.Api(consumer_key=get_user.consumer_key,
                             consumer_secret=get_user.consumer_secret_key,
                             access_token_key=get_user.access_token,
                             access_token_secret=get_user.access_secret_token,
                             tweet_mode='extended')
    return twitter_api


def tweet(request):
    if request.method == "POST":
        user_tweet = fetch_user()
        form = PostTweet(request.POST, request.FILES)
        # person = get_object_or_404(Users, pk=pk)
        if form.is_valid():
            print("tweet valid")
            tweet_text = form.cleaned_data['tweet']
            user_tweet.PostUpdate(tweet_text)
            return render(request, 'tweet_posted.html', {})

    elif len(Users.objects.all()) <= 0:
        return redirect('no_user_found')

    else:
        form = PostTweet()
        return render(request, 'post_tweet.html', {'post_tweet': form})


def tweet_search_form(request):
    if len(Users.objects.all()) > 0:
        form = Search()
        return render(request, 'search_form.html', {'search_form': form})
    else:
        return redirect('no_user_found')


def fetch_temp():
    t = Template.objects.all()
    return t


def search_results(request):
    current_date = datetime.datetime.now()
    now = current_date.strftime("%Y-%m-%d")
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text']
            print(search_text)
            since = str(form.cleaned_data['since'])
            until = str(form.cleaned_data['until'])
            count = form.cleaned_data['count']
            result_type = form.cleaned_data['result_type']
            geo_location_lat = str(form.cleaned_data['geo_location_lat'])
            geo_location_long = str(form.cleaned_data['geo_location_long'])
            radius = str(form.cleaned_data['radius'])
            geo = geo_location_lat+","+geo_location_long+","+radius
            geo_code = '"{}"'.format(geo)
            print(geo_code)
            text = '"{}"'.format(search_text)
            print(text)
            if since <= now and since <= until:
                user = fetch_user()
                form = TemplateForm()
                stored_temp = fetch_temp()
                data = {
                    'result': user.GetSearch(term=search_text, since=since, until=until, count=count,
                                        result_type=result_type, lang='en', ),
                    'form': form,
                    'stored_form': stored_temp
                }
                return render(request, 'search_result.html', data)
            else:
                return render(request, 'search_error.html', {})
        else:
            return render(request, 'search_error.html', {})


def dm(request, user_id):
    if request.method == "POST":
        form = DmForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data['text']
            # document = request.FILES['document']

            user = fetch_user()
            user.PostDirectMessage(text=text, user_id=user_id)
            print("SENT - " + text)
    else:
        form = DmForm()
        return render(request, 'dm.html', {'dm_form': form})


@csrf_exempt
def dmAPI(request):
    user = fetch_user()
    try:
        if request.method == "POST":
            data_list = json.loads(request.body)
            for elem in data_list:
                print(elem['dmId'])
                print(elem['dmText'])
                text = elem['dmText']
                user_id = elem['dmId']
                user.PostDirectMessage(text=text, user_id=user_id)

            return JsonResponse({'isSuccess': True, 'message': 'Success'})
        else:
            return JsonResponse({'isSuccess': False, 'message': 'Use only http post verb'})
    except BaseException as e:
        return JsonResponse({'isSuccess': False, 'message': 'Exception '+str(e)})


# def test_dm(request):
#     user = fetch_user()
#     text = 'test direct message twitter'
#     user_id = '751125390933000192'
#     user.PostDirectMessage(text=text, user_id=user_id)
#     return HttpResponse("<h1>SENT :D</h1>")


# def postDmUserList(request):
#     if request.method == 'POST':
#         form = DmUserListForm(request.POST)
#         form.save()
#         return JsonResponse({"success": True}, status=200)
#     else:
#         return JsonResponse({'success': False}, status=400)




# class DmUserListView(viewsets.ModelViewSet):
#     queryset = DmUserList.objects.all()
#     serializer_class = DmUserListSerializer
#


@csrf_exempt
def dm_list(request):
    print("in function")
    u = request.POST.getlist('key1[]')
    n = request.POST.getlist('key2[]')
    user_len = len(u)
    form = DmForm()
    if request.method == 'POST':
        print("in IF")
        print(n)
        print(u)

        return HttpResponse("<h2>POSTED</h2>")
    else:
        return render(request, 'dm_list.html', {'dm_form': form, 'n': n, 'len': user_len})
