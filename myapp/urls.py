from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('login/', views.login_user, name='login'),
	path('logout/', views.logout_user, name='logout'),
	path('register/', views.register_user, name='register'),
	path('past', views.past, name='past'),
	path('delete_past/<Past_id>', views.delete_past, name='delete_past'),
	path('api/customers/', views.customers, name='customers'),
	path('api/customer/<int:id>', views.customer, name='customer'),
	path('popup/createNewPopupEngagement/<int:clientId>', views.newPopupEngagementCreation, name='newPopupEngagementCreation'),
	path('popup/<int:popupId>', views.popup, name='popup'),
	path('popup/chatgpt/<int:client_id>/<str:popupEngagementUniqueIdentifier>', views.ChatGPTByClientView.as_view(), name='chatgpt-by-client'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
