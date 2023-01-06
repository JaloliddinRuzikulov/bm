from django.urls import path
from .views import Dashboard, AddDepot, OutDepot, OutDepotClose, OutDepotPrint, ListDepot, AddWalTalKie, InWalTalKie, \
    OutWalTalKie, \
    ListWalTalKie, WalTalKiePrint, WalTalKieClose, WalTalKieView

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('depot/', ListDepot.as_view(), name='list_depot'),
    path('depot/add/', AddDepot.as_view(), name='add_depot'),
    path('depot/out/', OutDepot.as_view(), name='out_depot'),
    path('depot/out/<int:pk>/print/', OutDepotPrint.as_view(), name='out_depot_print'),
    path('depot/out/<int:pk>/close/', OutDepotClose.as_view(), name='out_depot_close'),
    path('waltalkie/', ListWalTalKie.as_view(), name='list_waltalkie'),
    path('waltalkie/add/', AddWalTalKie.as_view(), name='add_waltalkie'),
    path('waltalkie/out/', WalTalKieView.as_view(), name='out_waltalkie'),
    path('waltalkie/out/<int:pk>/print/', WalTalKiePrint.as_view(), name='out_waltalkie_print'),
    path('waltalkie/out/<int:pk>/close/', WalTalKieClose.as_view(), name='out_waltalkie_close'),
    path('waltalkie/in/', InWalTalKie.as_view(), name='in_waltalkie'),
    path('archive/', ListWalTalKie.as_view(), name='archive'),
]
