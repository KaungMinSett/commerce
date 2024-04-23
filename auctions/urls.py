from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create', views.create_list, name='create'),
    path('create/new_category', views.create_category, name='new_category'),
    path('/<int:id>', views.view_details, name='view_details'),
    path('/<int:id>/watchlist', views.toggle_watchlist, name='watchlist'),
    path('/<int:id>/bid', views.place_bid, name='bid'),
]

