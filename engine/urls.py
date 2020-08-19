from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'masters', views.MasterViewSet)

urlpatterns = [
    # path('masters/', views.MasterViewSet.as_view(), name = 'list-masters'),

    path('', include(router.urls)),
    path('user/signup', views.SignUpView.as_view(), name = 'sign-up-form'),
    path('record_list/', views.RecordList.as_view(), name = 'sign-up-form'),
]