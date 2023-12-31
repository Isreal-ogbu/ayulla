from django.urls import path
from rest_framework.routers import DefaultRouter
from account import views

router = DefaultRouter()
router.register('user', views.UserViewSet, basename="user")

urlpatterns=[
    path("login/", views.LoginViewSet.as_view({'post':'post'}), name="login"),
    path('logout/', views.LogoutViewSet.as_view({'post': 'post'}), name="logout"),
    path('register/', views.RegisterViewSet.as_view({'post':'post'}), name="register"),
    path('reset_password', views.PasswordRecoveryView.as_view({'post':'post'}), name="reset_password"),
    path('rf/', views.GetUserReferalLink.as_view({'get':'get'}), name="referal_link"),
    path('referal/<uuid:code>/welcome', views.ReferralView.as_view({'post':'post'}), name="link")

] + router.urls