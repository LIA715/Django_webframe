from django.shortcuts import render, redirect
from .models import Post, Category
from django.views.generic import ListView, DetailView,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.core.exceptions import PermissionDenied

# Create your views here.

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title','hook_text','content','head_image','file_upload','category','tags']

    #template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request,*args,**kwargs)
        else:
            raise PermissionDenied


#post 권한을 위해 2개에서 상속 받음. 마지막 createview는 formview.
#CreatView로 상속받은 폼 클래스. 사용자 인증처리.
#기본적으로 form 지원. 상위에서 로그인 되어 있는지 처리.
class PostCreate(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model=Post
    fields=['title','hook_text','content', 'head_image', 'file_upload', 'category','tags']#페이지를 띄워서 템플릿으로 넘겨줘
    # default template_name => "post_form.html"
    template_name="blog/post_update_form.html"

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    # is_superuser는 관리자. superuser/staff/일반. 세개로 나뉨. 권한 확인. super, staff 여야 내용 보여줘.
    # 사용자 인증이 안된 상태에서는 글 쓸 수 없음.

    def form_valid(self,form):
        current_user=self.request.user #현재 user를 current_user에 저장
        if(current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser)):
            #로그인이 되어있다면. authenticated = 로그인되어있음.
            #동시에 staff, superuser라면. 이 조건을 모두 만족할때만 진행.
            form.instance.author=current_user
            #form안에 author라는 필드. 작성자 필드. 로그인 되어있는 사용자가. 자동적으로 채워짐.
            # not tag
            return super(PostCreate,self).form_valid(form)
        else:
            return redirect('/blog/')
            #강제적으로 '/blog/'로 보내버림

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
