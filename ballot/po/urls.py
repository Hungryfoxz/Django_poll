from django.contrib import admin
from django.urls import path,include
from . import views
 

urlpatterns = [
    path("", views.index, name='index'),
    path("login/", views.login_view, name='login_view'),
    path("povo_home/", views.povo_home, name= 'povo_home'),
    path("preciding_officer/", views.officer, name= 'officer'),
    path("voter/", views.voter, name= 'voter'),
    #path("voter_show_ballot/", views.voter_show_ballot, name='voter_show_ballot'),
    path("admitted_from_po/", views.admitted_from_po, name= 'admitted_from_po'),
    path("aGlkZGVuLXJlc3VsdC1wYW5lbAoK/", views.tables, name= 'tables'),
    path("logout/", views.logout_view, name= 'logout_view'),
    path("clear_votes/", views.clear_votes, name= 'clear_votes'),
    path("mock_panel/", views.mock_panel, name= 'mock_panel'),
    path("total_students_voted/", views.total_students_voted, name='total_students_voted'),
    path("mock_results/", views.mock_results, name='mock_results'),
    path("mock_clear/", views.mock_clear, name='mock_clear'),
    #path("my_ajax_check/",views.my_ajax_check, name='my_ajax_check'),
    path("my_ajax_check/",views.my_ajax_check, name='my_ajax_check'), 
    path("tot_mock/", views.tot_mock, name='tot_mock'),
    path("original_voting/", views.original_voting, name= 'original_voting'),

]
