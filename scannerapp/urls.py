"""scannerapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
from django.conf.urls import url, include
from rest_framework import routers
from people import views as PeopleViews
from entryexit import views as EntryExitViews

router = routers.DefaultRouter()
router.register(r'users', PeopleViews.UserViewSet)
router.register(r'groups', PeopleViews.GroupViewSet)
router.register(r'entries', EntryExitViews.EntriesViewSet)
router.register(r'building', EntryExitViews.BuildingViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/login', PeopleViews.login),
    url(r'^people/$', PeopleViews.PeopleList.as_view(), name = 'peoplelist'),
    url(r'^people/(?P<pk>\w+)/$', PeopleViews.PeopleDetail.as_view(), name = 'people_detail'),
    url(r'^entryexit/$', EntryExitViews.EntriesList.as_view(), name = 'entryexitlist'),
    url(r'^entryexit/(?P<pk>\d+)/$', EntryExitViews.EntriesDetail.as_view(), name = 'entryexit_detail'),
]
