from django.urls import path,reverse_lazy
from . views import AnimalList,AnimalDetail, AnimalCreate,AnimalUpdate,AnimalDelete,CustomLoginView,CustomLogoutView,RegisterPage
from . views import  AnimalHealthRecords,AnimalHealthDetail,AnimalHealthCreate,AnimalHealthUpdate,AnimalHealthDelete
from .views import MilkCreate,MilkList,MilkUpdate,MilkDelete
from.views import DashboardView
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/',CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('animals/',AnimalList.as_view(), name='animals',),
    path('animal/<int:pk>/', AnimalDetail.as_view(), name='animals'),
    path('create-animal/', AnimalCreate.as_view(), name='create-animal'),
    path('update-animal/<int:pk>/', AnimalUpdate.as_view(), name='update-animal'),
    path('delete-animal/<int:pk>/', AnimalDelete.as_view(), name='delete-animal'),
    
    #Health urls
    path('animal-health-records/', AnimalHealthRecords.as_view(), name='animal-health-records'),
    path('health-detail/<int:pk>/', AnimalHealthDetail.as_view(), name='health-detail'),
    path('health-create/', AnimalHealthCreate.as_view(), name='health-create'),
    path('health-update/<int:pk>/', AnimalHealthUpdate.as_view(), name='health-update'),
    path('health-delete/<int:pk>/', AnimalHealthDelete.as_view(), name='health-delete'),
    
    # Milk Urls
    path('milk-create/', MilkCreate.as_view(), name='milk-create'),
    path('milk-records/', MilkList.as_view(), name='milk-records'),
    path('milk-update/<int:pk>/', MilkUpdate.as_view(), name='milk-update'),
    path('milk-delete/<int:pk>/', MilkDelete.as_view(), name='milk-delete'),
    # Dashboard
     path('', views.DashboardView, name='dashboard'),
]
