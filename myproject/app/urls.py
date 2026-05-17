from django.urls import path
from . import views
from .views import chat_api

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register_user, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    path('chat-api/', chat_api, name='chat_api'),

    # ✅ FIXED HERE
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('increase/<int:product_id>/', views.increase_qty, name='increase_qty'),
    path('decrease/<int:product_id>/', views.decrease_qty, name='decrease_qty'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:product_id>/', views.update_cart, name='update_cart'),

    # path('payment/', views.payment_view, name='payment'),
    # path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('orders/', views.order_history, name='orders'),

    # strip
    path('cart/', views.cart_view, name='cart'),

    # Stripe
    path('stripe-checkout/', views.stripe_checkout, name='stripe_checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),

    # Orders
    path('orders/', views.order_history, name='orders'),
]