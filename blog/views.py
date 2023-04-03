from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Crop, Weather
import random
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Rest API
# Rest
from django.http import JsonResponse
from .serializers import PostSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.decorators import login_required

import pandas as pd
import pickle
import joblib
import sklearn
from sklearn import linear_model
import math
import os


# Load ML models
model_crop_loaded = joblib.load('./MLmodels/agri_forest_com_django.pkl')
model_weather_loaded = joblib.load('./MLmodels/W_LR_Model.pkl')


# Function based view (home)
def home(request):
    if request.method == 'POST':
        # Random User and color
        users = Post.objects.all()
        random_users = random.sample(set(users), 2)
        #SearchField
        page_obj = searched_item = request.POST['search']
        if searched_item != "" and searched_item is not None:
            page_obj = Post.objects.filter(content__contains=searched_item)  # Must be a field of model
        #Pagination
        per_page = request.GET.get("per_page", 2)
        paginator = Paginator(page_obj, per_page)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj':page_obj,
            'title':'Home',
            'random_users': random_users
        }
        return render(request, 'blog/home.html', context=context)
    
    
    posts = Post.objects.all().order_by('-date_posted')
    users = Post.objects.all()
    random_users = random.sample(set(users), 2)
    #Pagination
    per_page = request.GET.get("per_page", 2)
    paginator = Paginator(posts, per_page)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context={
        'page_obj':page_obj,
        'title':'Home',
        'random_users': random_users
    }
    return render(request, 'blog/home.html', context=context)

# Class based view (home)
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' 
    context_object_name = 'posts'
    ordering = '-date_posted'
    paginate_by = 3

# Class based view (home)
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' 
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# Class based view (Every single post)
class PostDetailView(DetailView):
    model=Post   # default template:   <app>/<model>_<viewtype>.html > blog/post_detail.html


# Class based view (Create Post)
class PostCreateView(LoginRequiredMixin, CreateView):
    model=Post 
    fields = ['author_link', 'title', 'content']  # template default is post_form.html

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Class based view (Update Post)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=Post 
    fields = ['author_link', 'title', 'content'] 
    # template default is post_form.html we don't need make it again 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# Class based view (Delete post)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Post 
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html')

@login_required
def projects(request):
    return render(request, 'blog/projects.html')

@login_required
def morgan_stanley(request):
    return render(request, 'blog/morgan_stanley.html')

@login_required
def crop_model(request):
    if request.method == 'POST':
        temp={}
        temp['Year'] = request.POST.get('year')
        temp['Latitude'] = request.POST.get('latitude')
        temp['Longitude'] = request.POST.get('longitude')
        temp['Crop'] = request.POST.get('crop')
        temp['Acres'] = request.POST.get('acres')
        temp['Measured'] = request.POST.get('measure')

        crop = Crop(Year=temp['Year'], Latitude=temp['Latitude'], Longitude=temp['Longitude'],
                        Crop=temp['Crop'], Acres=temp['Acres'], Measured=temp['Measured'])
        
        crop.save()

        testData = pd.DataFrame({'x':temp}).transpose(copy=True)
        testData = testData[['Year', 'Latitude', 'Longitude', 'Crop', 'Acres', 'Measured']]
        # print(testData)
        # print(type(testData))

        crop_pred = round(model_crop_loaded.predict(testData)[0], 2)

        context = {
            'crop_pred': crop_pred
        }
        return render(request, 'blog/crop_model.html', context=context)
    return render(request, 'blog/crop_model.html')


@login_required
def weather_model(request):
    if request.method == 'POST':
        temp={}
        temp['Year'] = request.POST.get('year')
        temp['Latitude'] = request.POST.get('latitude')
        temp['Longitude'] = request.POST.get('longitude')
        temp['tavg'] = request.POST.get('tavg')
        temp['tmin'] = request.POST.get('tmin')
        temp['tmax'] = request.POST.get('tmax')

        weather = Weather(Year=temp['Year'], Latitude=temp['Latitude'], Longitude=temp['Longitude'],
                        tavg=temp['tavg'], tmin=temp['tmin'], tmax=temp['tmax'])
        
        weather.save()

        testData = pd.DataFrame({'x':temp}).transpose(copy=True)
        testData = testData[['Year', 'Latitude', 'Longitude', 'tavg', 'tmin', 'tmax']]
        # print(testData)
        # print(type(testData))

        weather_pred = round(model_weather_loaded.predict(testData)[0], 1)

        context = {
            'weather_pred': weather_pred
        }
        return render(request, 'blog/weather_model.html', context=context)
    return render(request, 'blog/weather_model.html')


def contact(request):
    return render(request, 'blog/contact.html')


# Rest API
@api_view(['GET', 'POST'])
def post_api_list(request, format=None):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        data = {
        'message': 'POST is just possible when you Login in your account'
        }
        return JsonResponse(data)