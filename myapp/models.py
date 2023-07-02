import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Client(models.Model):
	clientId = models.ForeignKey(User, related_name='client', on_delete=models.CASCADE)
	subscription = models.SmallIntegerField()
	aboutClient = models.TextField(max_length=3000, null=True)
	helpPage = models.CharField(max_length=200, null=True)
	website = models.CharField(max_length=200, null=True)
	clientHasProducts = models.BooleanField(default=False)
	clientHasPromotions = models.BooleanField(default=False)

class PromoCode(models.Model):
	client = models.ForeignKey(Client, related_name='promoCodes', on_delete=models.CASCADE)
	code = models.CharField(max_length=50)

class Popup(models.Model):
	popupId = models.ForeignKey(Client, related_name='popup', on_delete=models.CASCADE)

	popupHasLogo = models.BooleanField(default=False,null=True)
	popupLogo = models.ImageField(null=True)
	popupGoal = models.SmallIntegerField(null=True)
	popupHeight = models.SmallIntegerField(null=True)
	popupWidth = models.SmallIntegerField(null=True)
	popupEmailSubscription = models.BooleanField(null=True)
	popupPromo = models.BooleanField(null=True)

	popupBackgroundColor = models.CharField(max_length=20, null=True)
	popupBorderColor = models.CharField(max_length=20, null=True)
	popupBorderWidth = models.CharField(max_length=4, null=True)
	popupBorderRadius = models.CharField(max_length=5, null=True)
	popupBorderBoxShadow = models.CharField(max_length=5, null=True)

	popupImage = models.ImageField( null=True)
	popupImageBorderWidth = models.CharField(max_length=4, null=True)
	popupImageBorderColor = models.CharField(max_length=8, null=True)
	popupImageHeight = models.CharField(max_length=4, null=True)
	popupImageWidth = models.CharField(max_length=4, null=True)

	popupChatHistoryFontSize = models.CharField(max_length=8, null=True)

	popupTitle = models.CharField(max_length=200, null=True)
	popupTitleHeight = models.SmallIntegerField(null=True)
	popupTitleWidth = models.SmallIntegerField(null=True)

	popupTextMarginLeft = models.SmallIntegerField(null=True)
	popupTextMarginRight = models.SmallIntegerField(null=True)

	popupTitlePositioning = models.SmallIntegerField(null=True)
	popupTitleTextColor = models.CharField(max_length=8, null=True)

	popupTitleFontSize = models.CharField(max_length=9, null=True)
	popupTitleFontWeight = models.CharField(max_length=9,null=True)
	popupContentFontSize = models.CharField(max_length=9, null=True)
	popupContentFontWeight = models.CharField(max_length=9, null=True)

	popupContent = models.CharField(max_length=200, null=True)
	popupContentHasBorder = models.BooleanField(null=True)
	popupContentHeight = models.SmallIntegerField(null=True)
	popupContentWidth = models.SmallIntegerField(null=True)
	popupContentPositioning = models.SmallIntegerField(null=True)
	popupContentTextColor = models.CharField(max_length=8, null=True)
	#BoxShadow, BorderRadius

	popupChatHistoryPositioning = models.SmallIntegerField(null=True)
	popupChatHistoryInputTextColor = models.CharField(max_length=20, null=True)
	popupChatHistoryOutputTextColor = models.CharField(max_length=20, null=True)
	popupChatHistoryTextSize = models.SmallIntegerField(null=True)
	popupChatHistoryInputBoxColor = models.CharField(max_length=20, null=True)
	popupChatHistoryInputFocusBorderColor = models.CharField(max_length=20, null=True)
	popupChatHistoryOutputBoxColor = models.CharField(max_length=20, null=True)
	popupChatHistoryOutputFocusBorderColor = models.CharField(max_length=20, null=True)

	popupChatButtonText = models.CharField(max_length=50, null=True)
	popupChatButtonPositioning = models.SmallIntegerField(null=True)
	popupChatButtonTextColor = models.CharField(max_length=20, null=True)
	popupChatButtonTextSize = models.SmallIntegerField(null=True)
	popupChatButtonBoxColor = models.CharField(max_length=20, null=True)
	popupChatButtonFocusBorderColor = models.CharField(max_length=20, null=True)

	popupSuggestionButtonPositioning = models.SmallIntegerField(null=True)
	popupSuggestionButtonTextColor = models.CharField(max_length=20, null=True)
	popupSuggestionButtonTextSize = models.SmallIntegerField(null=True)
	popupSuggestionButtonBoxColor = models.CharField(max_length=20, null=True)
	popupSuggestionButtonFocusBorderColor = models.CharField(max_length=20, null=True)

	popupCloseButtonText = models.CharField(max_length=50, null=True)
	popupCloseButtonPositioning = models.SmallIntegerField(null=True)
	popupCloseButtonTextColor = models.CharField(max_length=8, null=True)
	popupCloseButtonBoxColor = models.CharField(max_length=8, null=True)
	popupCloseButtonTextSize = models.CharField(max_length=10,null=True)
	popupCloseButtonVariant = models.CharField(max_length=10,null=True)
	popupCloseButtonColorScheme = models.CharField(max_length=10,null=True)

	popupSendButtonColor = models.CharField(max_length=10, null=True)
	popupSendButtonTextColor = models.CharField(max_length=10, null=True)
	popupSendButtonText = models.CharField(max_length=10, null=True)
	popupSendButtonVariant = models.CharField(max_length=10,null=True)
	popupSendButtonScheme = models.CharField(max_length=10,null=True)

	popupCTAButtonText = models.CharField(max_length=200, null=True)
	popupCTAButtonPositioning = models.SmallIntegerField(null=True)
	popupCTAButtonTextColor = models.CharField(max_length=200, null=True)
	popupCTAButtonHeight = models.SmallIntegerField(null=True)
	popupCTAButtonWidth = models.SmallIntegerField(null=True)
	popupCTAButtonLink = models.CharField(max_length=50, null=True)
	popupCTAButtonBorderColor = models.CharField(max_length=20, null=True)
	popupCTAButtonHasBorder = models.BooleanField(null=True)


	popupTitleAndContentPercentage = models.CharField(max_length=10, null=True)
	popupChatHistoryPercentage = models.CharField(max_length=10, null=True)
	popupChatSendPercentage = models.CharField(max_length=10, null=True)
	popupCTAPercentage = models.CharField(max_length=10, null=True)
	#popupImage =  models.ImageField(upload_to ='uploads/', null=True)

	popupExampleInputChatGPT = models.CharField(max_length=200, null=True)
	popupExampleOutputChatGPT = models.CharField(max_length=200, null=True)


class PopupAdditional(models.Model):
	popupAdditionalId = models.ForeignKey(Popup, related_name='popupAdditional', on_delete=models.CASCADE)
	popupAdditionalText = models.CharField(max_length=200, null=True)
	popupAdditionalLink = models.CharField(max_length=50, null=True)

class PopupEngagement(models.Model):
	popupEngagementId = models.ForeignKey(Popup, related_name='popupEngagement', on_delete=models.CASCADE)
	popupEngagementUniqueIdentifier = models.CharField(max_length=15, null=True)
	popupEngagementStart = models.DateTimeField(default=now)
	popupEngagementEnd = models.DateTimeField(null=True)
	conversationStartedAtWebsiteLink = models.CharField(max_length=150,null=True)

class ChatGPT(models.Model):
	requestId = models.ForeignKey(PopupEngagement, related_name='chatgpt', on_delete=models.CASCADE)
	inputChatGPT = models.TextField(max_length=2000)
	outputChatGPT = models.TextField(max_length=5000, null=True)


class PopupChatSuggestion(models.Model):
	popupChatSuggestion = models.ForeignKey(Popup, related_name='popupChatSuggestion', on_delete=models.CASCADE)
	popupSuggestion = models.TextField(max_length=50, null=True)

class GeneralInformationForChatGPT(models.Model):
	chatGPTInformationKey = models.ForeignKey(Popup, related_name='informationForChatGPT', on_delete=models.CASCADE)
	whatProblemIsYourCompanySolving = models.TextField(max_length=400, null=True)
	whatServicesDoYouOffer = models.TextField(max_length=400, null=True)
	howCanCustomersReachYouOrYourTeam = models.TextField(max_length=400, null=True)
	whatAreFAQs = models.TextField(max_length=2000, null=True)
	anyOtherInformation = models.TextField(max_length=2000, null=True)
	howMuchDiscountCanYouDoMaximum = models.TextField(max_length=2000, null=True)
	doYouWantYourOwnPopupTitleAndContent = models.BooleanField(default=True)
	whatIsYourMostSoldProduct = models.TextField(max_length=2000, null=True)

class PopupProducts(models.Model):
	productSpecificChatGPTInformationKey = models.ForeignKey(Popup, related_name='productSpecificInformationForChatGPT',on_delete=models.CASCADE)
	productPrice = models.IntegerField(null=True)
	productCurrency = models.CharField(max_length=3, null=True)
	productIsDiscountable = models.BooleanField(default=False)
	productPriceAfterDiscount = models.IntegerField(null=True)
	productPromoCode = models.CharField(max_length=300, null=True)
	productLink = models.CharField(max_length=200, null=True)
	productSpecs = models.TextField(max_length=3000, null=True)
	productImage = models.ImageField(null=True)

class PopupFiles(models.Model):
	uploaded_by = models.ForeignKey(Client, on_delete=models.CASCADE)
	file = models.FileField(upload_to='popups/%Y/%m/%d/')
	uploaded_at = models.DateTimeField(default=now)

	def __str__(self):
		return self.file.name

