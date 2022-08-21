from django.urls import path
from .views import *
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name="crud"
urlpatterns = [
    path('', views.movie_list_create),
    path('<int:movie_pk>/', views.movie_detail_update_delete),
    path('<int:movie_pk>/reviews', views.review_list_create),
    path('<int:movie_pk>/reviews/<int:review_pk>', views.review_detail_update_delete),
    path('regist', views.user_regist, name="regist"),
    # path("login", views.user_login, name="login"),
    path("test", views.test, name="test"),
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('refresh', TokenRefreshView.as_view(), name='refresh'),
    path('logout', views.logout, name="logout")
]
