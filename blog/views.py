from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url
import os
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView, detail
from django.views.generic.edit import DeleteView
from .models import Post, Like, Category
from .forms import LoginForm, PostForm, SearchForm, SignUpForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


class OnlyMyPostMixin(UserPassesTestMixin):
    raise_exception = True
    def test_func(self):
        post = Post.objects.get(id = self.kwargs['pk'])
        return post.user == self.request.user


class IndexView(TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.fetch_all_posts()[:6] # 6件表示
        context = {
            'post_list': post_list,
        }
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = os.path.join('blog', 'post_create.html')
    model = Post
    form_class = PostForm
    # success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(PostCreateView, self).form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Postを登録しました')
        return resolve_url('blog:index')


class PostDetailView(DetailView):
    template_name = os.path.join('blog', 'post_detail.html')
    model = Post

    def get_context_data(self, *args, **kwargs):
        detail_data = Post.objects.fetch_by_post_id(self.kwargs['pk'])
        category_posts = Post.objects.fetch_by_category_name(category = detail_data.category)[:5]
        context = {
            'object': detail_data,
            'category_posts': category_posts,
        }
        return context


class PostUpdateView(OnlyMyPostMixin, UpdateView):
    template_name = os.path.join('blog', 'post_update.html')
    model = Post
    form_class = PostForm

    def get_success_url(self):
        messages.success(self.request, 'Postを更新しました')
        return resolve_url('blog:post_detail', pk=self.kwargs['pk'])


class PostDeleteView(OnlyMyPostMixin, DeleteView):
    template_name = os.path.join('blog', 'post_delete.html')
    model = Post
    
    def get_success_url(self):
        messages.success(self.request, 'Postを削除しました')
        return resolve_url('blog:index')


class PostListView(ListView):
    template_name = os.path.join('blog', 'post_list.html')
    model = Post
    paginate_by = 5

    def get_queryset(self):
        post_list = Post.objects.fetch_all_posts()
        return post_list


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        messages.info(self.request, 'ユーザー登録をしました')
        return HttpResponseRedirect(self.get_success_url())


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm


class UserLogoutView(LogoutView):
    template_name = 'logout.html'


@login_required
def like_add(request, pk):
    post = Post.objects.fetch_by_post_id(pk)
    is_liked = Like.objects.fetch_is_liked(user=request.user, post_id=pk)
    if is_liked > 0:
        messages.info(request, 'すでにお気に入りに追加済みです')
        return redirect('blog:post_detail', pk=post.id)
    like = Like()
    like.user = request.user
    like.post = post
    like.save()

    messages.success(request, 'お気に入りに追加しました!')
    return redirect('blog:post_detail', pk=post.id)


class CategoryListView(ListView):
    template_name = os.path.join('blog', 'category_list.html')
    model = Category


class CategoryDetailView(DetailView):
    template_name = os.path.join('blog', 'category_detail.html')
    model = Category
    '''
    URLに文字列を渡すためには、

    slug_field: モデルのフィールドの名前
    slug_url_kwarg: urlsのキーワードの名前を指定

    を行う
    '''
    slug_field = 'name_en'
    slug_url_kwarg = 'name_en'

    def get_context_data(self, *args,**kwargs):
        detail_data = Category.objects.fetch_category(name_en=self.kwargs['name_en'])
        category_posts = Post.objects.fetch_by_category(category_id=detail_data.id)

        context = {
            'object': detail_data,
            'category_posts': category_posts
        }
        return context


def search(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)

        if search_form.is_valid():
            freeword = search_form.cleaned_data['freeword']
            search_list = Post.objects.fetch_by_search_freeword(freeword)
        
        context = {
            'search_list': search_list,
        }
        return render (request, 'blog/search.html', context)