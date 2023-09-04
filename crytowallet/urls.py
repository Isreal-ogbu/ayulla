from django.urls import path
from rest_framework.routers import DefaultRouter
from crytowallet import views

router = DefaultRouter()
router.register('crypto', views.CryptoViewset, basename="crypto")
router.register('user_crypto', views.UserCrytoWalletViewSet, basename="mycrypto")

urlpatterns=[
    path("overview/", views.UserTotalCrypto.as_view(), name="crypto_overview")

] + router.urls