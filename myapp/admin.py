from django.contrib import admin
from .models import *

# Register Codes
admin.site.register(Client)
admin.site.register(Popup)
admin.site.register(ChatGPT)
admin.site.register(PromoCode)
admin.site.register(PopupEngagement)
admin.site.register(PopupAdditional)
admin.site.register(PopupFiles)
admin.site.register(GeneralInformationForChatGPT)
admin.site.register(PopupProducts)
admin.site.register(PopupEngagementForwardToGroup)
admin.site.register(PopupEngagementForwardToResponse)
admin.site.register(PopupEngagementForwardToItem)