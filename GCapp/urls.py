from django.urls import path
from django.urls import include

from . import views

app_name = 'GCapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name = 'logout'),
    path('main/', views.main, name = 'main'),
    path('<int:collection_gameid>/',views.game, name = 'game'),
    path('<int:news_id>/', views.detail, name='detail'),
    path('errors/', views.error, name = 'errors'),
    path('results/', views.search ,name = 'results'),
    path('delete/', views.delete, name = 'delete'),
    path('add/', views.add, name = 'add'),
    path('community/<int:communityid>/', views.community, name = 'community'),
    path('post/<int:postid>',views.post,name = 'post'),
    #path('captcha/', include('captcha.urls'))
]