from django.urls import path
from .views import FeatureDetectionView

urlpatterns = [
    path('', FeatureDetectionView.as_view(), name='home')
]
