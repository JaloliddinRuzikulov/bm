from django.urls import path
from .views import AddView
urlpatterns = [
    # path('/', ListDepot.as_view(), name='list_depot'),
    # path('/<int:id>', ListDepot.as_view(), name='list_depot'),
    path('add/', AddView.as_view(), name='add_walktalkio'),
    # path('/out/', OutDepot.as_view(), name='out_depot'),
]