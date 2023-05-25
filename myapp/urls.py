from django.urls import path
from . import views


urlpatterns = [
	path('login/', views.login_user, name='login'),
	path('logout/', views.logout_user, name='logout'),
	path('register/', views.register_user, name='register'),
	path('past', views.past, name='past'),
	path('delete_past/<Past_id>', views.delete_past, name='delete_past'),
	path('api/customers/', views.customers, name='customers'),
	path('api/customer/<int:id>', views.customer, name='customer'),
	path('clients/<int:client_id>/<str:popupEngagementUniqueIdentifier>/chatgpt/', views.ChatGPTByClientView.as_view(), name='chatgpt-by-client'),
]