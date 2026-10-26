from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("car/<int:id>/", views.car_detail, name="car_detail"),
    path("payment/<int:id>/", views.payment, name="payment"),
    path("success/<int:order_id>/", views.success, name="success"),
]
