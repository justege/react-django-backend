from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('login/', views.login_user, name='login'),
	path('logout/', views.logout_user, name='logout'),
	path('register/', views.register_user, name='register'),
	path('files/<int:clientId>', views.PopupFilesView, name='PopupFilesView'),
	path('popup/createNewPopupEngagement/<int:popupId>/<int:clientId>', views.newPopupEngagementCreation, name='newPopupEngagementCreation'),
	path('popup/<int:popupId>/<int:clientId>', views.popup, name='popup'),
	path('popup/chatgpt/<int:clientId>/<int:popupId>/<str:popupEngagementUniqueIdentifier>', views.ChatGPTByClientView.as_view(), name='chatgpt-by-client'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

