from django.urls import path
from .views import *

app_name = "core"

urlpatterns = [
    path('',HomeView.as_view(),name="homepage"),
    path('checkout/',CheckoutView.as_view(),name="checkout"),
    path('ordersummary/', OrderSummaryView.as_view(), name="order-summary"),
    path('Category/<slug>/',CategoryView.as_view(),name="category"),
    path('products/<slug>/',ItemDetailView.as_view(),name="product"),
    path('add-to-cart/<slug>/',AddToCartView.as_view(),name="add-to-cart"),
    path('request-refund/', RequestFundView.as_view(), name="request-refund"),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/',remove_from_cart,name="remove-from-cart"),
    path('remove-item-from-cart/<slug>/',remove_single_item_from_cart,name="remove-single-item-from-cart"),
    path('payment/<payment_option>',PaymentView.as_view(),name="payment"),
]