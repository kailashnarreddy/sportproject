


from django.urls import path
import uuid
from sportapp import views

urlpatterns = [
    path('',views.Index,name='Home'),
    path('AddClub/', views.ClubsView, name='clubs'),
    path('superindent/', views.superindent, name='superindent'),
    path('Secy/', views.secyEquipments, name='Secy'),
    path('Secy/<int:pk>/add_equipment', views.SecyEquipmentView, name='SecyEquipments'),
    path('Secy/<int:pk>/<uuid:id>/Issue/',views.SecyIssueFormView,name='SecyIssue'),
    path('Secy/<int:pk>/<uuid:id>/delete/',views.SecyDeleteEquipmentView,name='SecyequipmentDelete'),
    path('Return/<int:pk>/<slug:id>',views.Secyreturnequipment,name='SecyReturn'),
    path('Secy/IssueList', views.secyIssueList, name='SecyIssueList'),
    path('accept/<pk>', views.accept, name='accept'),
    path('deny/<pk>', views.deny, name='deny'),
    path('clubsList/',views.ClubsListView.as_view(),name='clubsList'),
    path('editClub/<pk>/', views.UpdateClubsView, name='editClub'),
    path('<pk>/add_equipment/', views.EquipmentView, name='equipments'),
    path('<pk>/equipmentsList/', views.EquipmentListView, name='equipmentsList'),
    path('<pk>/<uuid:id>/delete/',views.deleteEquipmentView,name='equipmentDelete'),
    path('<pk>/<uuid:id>/Issue/',views.IssueFormView,name='Issue'),
    path('<pk>/IssueList/',views.IssueListView,name='IssueList'),
    path('IssueList/',views.TotalListView.as_view(),name='TotalIssueList'),
    path('Return/<int:pk>/<slug:id>',views.returnequipment,name='Return'),
    path('general/',views.general,name='general'),
    path('addgeneral/',views.addgeneral,name='addgeneral'),
    path('generalissue/<int:pk>',views.generalissue,name='generalissue'),
    path('generalIssueList/',views.generallist,name='generalIssueList')

]
