from  django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("cart_product_detele/<int:cart_product_id>/",views.CartProductDelete.as_view(),name="delete"),
    path("cart/increment/<int:cart_id>/",views.IncrementView.as_view(),name="increment",),
    path("cart/decrement/<int:cart_id>/",views.DecrementView.as_view(),name="decrement",),
    path('add-to-cart/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path("cart/", views.CartListView.as_view(), name="cart"),

    path('product/<int:id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path("category/<int:id>/", views.CategoryDetailView.as_view(), name="category_detail"),

    path("", views.ProductListView.as_view(), name="home"),
    path('account/<int:user_id>/', views.AccountView.as_view(), name='account'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
