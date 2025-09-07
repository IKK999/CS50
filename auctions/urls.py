from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create', views.create, name='create'),
    path('listing/<int:listing_id>', views.listing, name='listing'),
    path('change_watchlist/<int:listing_id>', views.change_watchlist, name='change_watchlist'),
    path('submit_bid/<int:listing_id>', views.submit_bid, name='submit_bid'),
    path('close_auction/<int:listing_id>', views.close_auction, name='close_auction'),
    path('submit_comment/<int:listing_id>', views.submit_comment, name='submit_comment'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('categories', views.categories, name='categories'),
    path('category/<str:category>', views.category, name='category')
]
