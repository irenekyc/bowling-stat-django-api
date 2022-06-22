"""bowlingstat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from bowlingstat import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("teams/", views.team_list),
    path("teams/add", views.add_team),
    path("teams/<str:teamid>/", views.team_data),
    path("teams/<str:teamid>/events", views.team_events_all),
    path("teams/<str:teamid>/events/<str:eventid>", views.team_events_single),
    # path("events/add", views.add_team_event_data),
    # path("events-summary/add", views.add_team_event_summary_data),
    path("teams/<str:teamid>/upload", views.upload_event_csv),
]
