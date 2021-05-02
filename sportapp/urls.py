from django.urls import path
import uuid
from sportapp import views

urlpatterns = [
    path('',views.Index,name='Home'),
    path('AddClub/', views.ClubsView, name='clubs'),
    path('superindent/', views.superindent, name='superindent'),
    path('accept/<pk>', views.accept, name='accept'),
    path('deny/<pk>', views.deny, name='deny'),
    path('clubsList/',views.ClubsListView.as_view(),name='clubsList'),
    path('editClub/<pk>/', views.UpdateClubView.as_view(), name='editClub'),
    path('<pk>/add_equipment/', views.EquipmentView, name='equipments'),
    path('<pk>/equipmentsList/', views.EquipmentListView, name='equipmentsList'),
    path('<pk>/<uuid:id>/delete/',views.deleteEquipmentView,name='equipmentDelete'),
    path('<pk>/<uuid:id>/Issue/',views.IssueFormView,name='Issue'),
    path('<pk>/IssueList/',views.IssueListView,name='IssueList'),
    path('IssueList/',views.TotalListView.as_view(),name='TotalIssueList'),
   path('Return/<int:pk>/<slug:id>',views.returnequipment,name='Return'),

]