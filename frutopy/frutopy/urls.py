from django.conf.urls import url, include
from rest_framework import routers
from tables import views

router = routers.DefaultRouter()
router.register(r'samples', views.SampleViewSet)
router.register(r'ml_models', views.ML_ModelViewSet)
router.register(r'sp_models', views.SP_ModelViewSet)
# router.register(r'samples_list', views.SampleViewSet)


urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), # login URLs for browsable API
    url(r'^$', 'tables.views.upload_file', name='upload_file'),
    url(r'^success/$', 'tables.views.success', name='success'),
    url(r'^samples_list/$', views.SampleListView.as_view(), name='list'),
    url(r'^', include(router.urls))
]