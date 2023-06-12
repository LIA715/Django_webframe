from django.shortcuts import render, redirect
from .models import Post, Category, Tag,Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.

# CBV
class PostList(ListView):
    model = Post
    ordering = '-pk'
    paginate_by = 3
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
        context['comment_form'] = CommentForm
        return context  # => 리턴은 post_detail.html로 들어가게된다. (post.categories,no_category_post_count) 값이 넘어가게됌.


def category_page(request, slug):  # 프로그래밍, 문화-예술, 웹개발, 미분류 -> no_category로 가게됌
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)  # .all()
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

def new_comment(request,pk):
   if request.user.is_authenticated:
       post = get_object_or_404(Post, pk=pk) #post모델에서 pk번호에 해당되는 하나만 가져오기.

       if request.method == "POST":
           comment_form = CommentForm(request.POST)
           if comment_form.is_valid():
               comment = comment_form.save(commit=False)
               comment.post = post
               comment.author = request.user
               comment.save()
               return redirect(comment.get_absolute_url())
       else:
           return redirect(post.get_absolute_url())
   else:
       return PermissionDenied

def delete_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']
    # template_name=post_form.html

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if (current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser)):
            form.instance.author = current_user
            # not tag
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')  # 강제적으로 '/blog/'로 보내버림

# blog/update_post/pk/
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    # post_form.html 기본 템플렛
    template_name='blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

# 오류를 넘겨주는 코드
def csrf_failure(request, reason=""):
    return redirect('/blog/')


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
#
# def new_comment(request,pk):

class CommentUpdate(LoginRequiredMixin,UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request,*args,**kwargs)
        else:
            raise PermissionDenied

    #class PostList(ListView):
    #   model = Post;
    #   template_name = post_list.html
    #   def gett_qeuryset(self):
    #   post_list= Post.objects.all


class PostSearch(PostList):  # post_list.html
    paginated_by = None  # pagination 안해.

    def get_queryset(self):  # Post(Post.objects.all) 불러옴.
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs): #검색한 단어 결과 보여주기 위한 작업.
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q'] #검색어 가져옴.
        context['search_info'] = f'Search:{q}({self.get_queryset().count()})'

        return context