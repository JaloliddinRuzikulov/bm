from django.urls import path
from .views import AddView, LaventView, LaventPrintView, LaventCloseView, ReturnView, DataView, ManageView

urlpatterns = [
    path('add/', AddView.as_view(), name='add_tablet'),
    path('manage/', ManageView.as_view(), name='manage_tablet'),
    path('lavent/', LaventView.as_view(), name='lavent_tablet'),
    path('lavent/<int:pk>/print/', LaventPrintView.as_view(), name='lavent_print_tablet'),
    path('lavent/<int:pk>/close/', LaventCloseView.as_view(), name='lavent_close_tablet'),
    path('return/', ReturnView.as_view(), name='return_tablet'),
    path('data/', DataView.as_view(), name='data_tablet'),
]
