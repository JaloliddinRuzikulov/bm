from django.urls import path
from .views import AddView, LaventView, LaventPrintView, LaventCloseView, ReturnView, DataView, ManageView

urlpatterns = [
    path('add/', AddView.as_view(), name='add_twoway'),
    path('manage/', ManageView.as_view(), name='manage_twoway'),
    path('lavent/', LaventView.as_view(), name='lavent_twoway'),
    path('lavent/<int:pk>/print/', LaventPrintView.as_view(), name='lavent_print_twoway'),
    path('lavent/<int:pk>/close/', LaventCloseView.as_view(), name='lavent_close_twoway'),
    path('return/', ReturnView.as_view(), name='return_twoway'),
    path('data/', DataView.as_view(), name='data_twoway'),
]
