from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.PostList.as_view()), # CBV 방식의 함수 호출 # 클래스 방식 # blog/
    path('<int:pk>/new_comment/', views.new_comment), #/blog/1/new_comment/
    path('update_comment/<int:pk>/',views.CommentUpdate.as_view()), #blog/update_comment/2/ 2번 댓글을 수정해라
    path('delete_comment/<int:pk>/',views.delete_comment), #/blog/delete_comment/2 2번 댓글을 지워라.

    # path('', views.index), # FBV 방식의 함수 호출
    path('<int:pk>/', views.PostDetail.as_view()), # CBV, 키를 이용해서 하나만 검색해온다.
    # path('<int:pk>/', views.single_post_page), # FBV
    path('category/<str:slug>/', views.category_page),
    path('create_post/', views.PostCreate.as_view()), # 새 포스트 만들기 /blog/create_post/
    path('update_post/<int:pk>/', views.PostUpdate.as_view()), # /blog/update_post/5
]
