from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:id>/", views.listing, name="listing"),
    path("new_listing/", views.create_listing, name="create"),
    path("closed_auction/<int:id>/", views.close_auction, name="closed_auction"),
    path("close_auction/<int:id>/remove_from_wishlist", views.remove_wishlist_closed, name="remove_wishlist_closed"),
    path("listing/<int:id>/new_comment/", views.new_comment, name="new_comment"),
    path("listing/<int:id>/add_to_wishlist/", views.add_wishlist, name="add_wishlist"),
    path("listing/<int:id>/remove_from_wishlist", views.remove_wishlist, name="remove_wishlist"),
    path("user/wishlist/", views.wishlist, name="wishlist"),
    path("categories/", views.categories, name="categories"),
    path("category/<str:code>", views.category, name="category"),
    path("delete_auction/<int:id>", views.delete_auction, name="delete_auction")
]
