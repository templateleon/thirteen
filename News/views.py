import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.db.models import Exists, OuterRef



from .models import Post, Category, Subscription
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    # название модели
    model = Post
    # поле для сортировки - по дате создания ( '-' - от конца)
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10



class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

class NewCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.categoryType = 'NV'
        return super().form_valid(form)


class NewEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.categoryType = 'NV'
        return super().form_valid(form)

class NewDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.categoryType = 'AR'
        return super().form_valid(form)

class ArticleEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.categoryType = 'AR'
        return super().form_valid(form)

class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

"""
class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context
"""
#@login_required
#def subscribe(request, pk):
#    user = request.user
#    category = Category.objects.get(id=pk)
#    category.subscribers.add(user)
#
#    message = 'Вы успешно подписаны на рассылку новостей категории'
#    return render(request, 'subscribe.html', {'category': category, 'message':message})


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

