from django.urls import path
from .views import Dashboard, AddDepot, OutDepot, OutDepotClose, OutDepotPrint, ListDepot
urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('depot/', ListDepot.as_view(), name='list_depot'),
    path('depot/add/', AddDepot.as_view(), name='add_depot'),
    path('depot/out/', OutDepot.as_view(), name='out_depot'),
    path('depot/out/<int:pk>/print/', OutDepotPrint.as_view(), name='out_depot_print'),
    path('depot/out/<int:pk>/close/', OutDepotClose.as_view(), name='out_depot_close'),
]
