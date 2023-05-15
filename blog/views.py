from django.shortcuts import render, redirect
from .models import Post, Category
from django.views.generic import ListView, DetailView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# Create your views here.

# CBV
class PostList(ListView):
    model = Post
    ordering = '-pk'
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()  # post_list를 가져옴 # 상위에서 가져오기때문
        context['categories'] = Category.objects.all()  # Category DB의 내용
        context['no_category_post_count'] = Post.objects.filter(
            category=None).count()  # category가 없을수 있기때문에 no_category이고 뒤에는 없는것 카운트
        return context  # => 리턴은 post_list.html로 들어가게된다.


# FBV
# def index(request):
#     posts = Post.objects.all().order_by('-pk')  # -사용시 내림차순, 없을시 오름차순 pk는 primary key의 약자를 의미함
#
#     return render(
#         request,
#         'blog/post_list.html',
#         {
#             'posts': posts,
#         }
#     )

class PostDetail(DetailView):
    model = Post

    # template_name='blog/single_post_page.html'
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()  # post_list를 가져옴 # 상위에서 가져오기때문
        context['categories'] = Category.objects.all()  # Category DB의 내용
        context['no_category_post_count'] = Post.objects.filter(
            category=None).count()  # category가 없을수 있기때문에 no_category
        return context  # => 리턴은 post_detail.html로 들어가게된다. (post.categories,no_category_post_count) 값이 넘어가게됌.


def category_page(request, slug):  # 프로그래밍, 문화-예술, 웹개발, 미분류 -> no_category로 가게됌
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None) # .all()
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )

class PostCreate(LoginRequiredMixin,UserPassesTestMixin, CreateView):

    model=Post
    fields=['title','hook_text','content', 'head_image', 'file_upload', 'category','tags']
    # template_name=post_form.html

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self,form):
        current_user=self.request.user
        if(current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser)):
            form.instance.author=current_user
            # not tag
            return super(PostCreate,self).form_valid(form)
        else:
            return redirect('/blog/') # 강제적으로 '/blog/'로 보내버림





    # def single_post_page(request, pk):
    #     post = Post.objects.get(pk=pk) # objects.get은 괄호안에 만족하는 레코드를 가져오라는 의미이다.
    #
    #     return render(
    #         request,
    #         'blog/index.html',
    #         {
    #             'post':post,
    #         }
    #     )
