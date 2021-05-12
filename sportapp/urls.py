


from django.urls import path
import uuid
from sportapp import views

urlpatterns = [
    path('', views.Home1, name='Home1'),
    path('home/',views.Index,name='Home'),
    path('AddClub/', views.ClubsView, name='clubs'),
    path('superindent/<int:num>', views.superindent, name='superindent'),
    path('accept/<pk>', views.accept, name='accept'),
    path('deny/<pk>', views.deny, name='deny'),
    path('clubsList/',views.ClubsListView,name='clubsList'),
    path('editClub/<pk>/', views.UpdateClubsView, name='editClub'),
    path('<pk>/add_equipment/', views.EquipmentView, name='equipments'),
    path('<pk>/equipmentsList/', views.EquipmentListView, name='equipmentsList'),
    path('<pk>/<uuid:id>/delete/',views.deleteEquipmentView,name='equipmentDelete'),
    path('<pk>/<uuid:id>/Issue/',views.IssueFormView,name='Issue'),
    path('<pk>/IssueList/',views.IssueListView,name='IssueList'),
    path('total_list/',views.total_list,name='total_list'),
    path('Return/<int:pk>/<slug:id>',views.returnequipment,name='Return'),
    path('general/',views.general,name='general'),
    path('addgeneral/',views.addgeneral,name='addgeneral'),
    path('generalissue/<int:pk>',views.generalissue,name='generalissue'),
    path('generalIssueList/',views.generallist,name='generalIssueList'),
    path('generalreturn/<slug:id>',views.generalreturn,name='generalreturn'),
    path('generaldelete/<slug:id>',views.generaldelete,name='generaldelete'),
    path('gensecissuelist',views.gensecissuelist,name='gensecissuelist')

]
