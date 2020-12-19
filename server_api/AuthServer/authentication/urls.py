from django.urls import path
from .views import RegisterView,LoginView,UserListView,UserDetailView

urlpatterns=[
    path('register',RegisterView.as_view()),
    path('login',LoginView.as_view()),
    path('admin',UserListView.as_view()),
    path('<str:username>',UserDetailView.as_view())
]