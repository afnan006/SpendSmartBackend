from django.urls import path
from .views import UserCreateView, ExpenseListCreateView, ExpenseDetailView

urlpatterns = [
    path('auth/register/', UserCreateView.as_view(), name='register_user'),
    path('expenses/', ExpenseListCreateView.as_view(), name='list_create_expenses'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='retrieve_update_delete_expense'),
]
