from django.urls import path
from . import views

urlpatterns=[
    # 이 부분을 채울 예정!

    path('',views.PostList.as_view()), #server/blog/
    # path('', views.index),
    path('<int:pk>/',views.PostDetail.as_view()), #server/blog/1
    path('<int:pk>/', views.single_post_page),
    path('category/<str:slug>/', views.category_page), # category_page 함수 호출   as_view가 있으면 class 없으면 함수.
    path('create_post/',views.PostCreate.as_view()), # blog로 와서 postcreate 주소 참조
    path('update_post/<int:pk>/',views.PostUpdate.as_view()),
]