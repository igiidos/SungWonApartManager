from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('fake_list/', views.fake_list, name='fake_list'),
    path('fake_list_all/', views.fake_list_all, name='fake_list_all'),
    path('saving/', views.pre_cron, name='saving'),
    path('change_to_doctor_status_ajax/', views.change_to_doctor_status_ajax, name='change_to_doctor_status_ajax'),
    path('change_back_singo_ajax/', views.change_back_singo_ajax, name='change_back_singo_ajax'),
    path('all_apart_lists/', views.all_apart_lists, name='all_apart_lists')
]