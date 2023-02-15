from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
import random
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator


# Function based view (home)
def home(request):
    if request.method == 'POST':
        # Random User
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


def contact(request):
    return render(request, 'blog/contact.html')