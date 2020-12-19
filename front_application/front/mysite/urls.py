
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('delete',views.delete,name='delete'),
    path('boardlist',views.boardlist,name='boardlist'),
    path('edit',views.edit,name='edit'),
    path('update',views.update,name='update')
]

