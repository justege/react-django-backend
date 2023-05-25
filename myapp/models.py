import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Code(models.Model):
	user = models.ForeignKey(User, related_name="code", on_delete=models.DO_NOTHING)
	question = models.TextField(max_length=3000)
	code_answer = models.TextField(max_length=3000)
	language = models.CharField(max_length=50)
	def __str__(self):
		return self.question

class Customer(models.Model):
	name = models.CharField(max_length=200)
	industry = models.CharField(max_length=200)

class Client(models.Model):
	clientId = models.ForeignKey(User, related_name='client', on_delete=models.CASCADE)
	subscription = models.SmallIntegerField()
	aboutClient = models.TextField(max_length=3000, null=True)
	helpPage = models.CharField(max_length=200, null=True)
	website = models.CharField(max_length=200, null=True)
	clientHasProducts = models.BooleanField(default=False)
	clientHasPromotions = models.BooleanField(default=False)

class ClientProducts(models.Model):
	clientProductId = models.ForeignKey(Client, related_name='clientProducts', on_delete=models.CASCADE)
	productPrice = models.SmallIntegerField(null=True)
	productLink = models.CharField(max_length=300, null=True)
	productDetails = models.TextField(max_length=3000,null=True)
	productPriceWithPromo = models.CharField(max_length=300, null=True)

class PromoCode(models.Model):
	client = models.ForeignKey(Client, related_name='promoCodes', on_delete=models.CASCADE)
	code = models.CharField(max_length=50)

class Popup(models.Model):
	popupId = models.ForeignKey(Client, related_name='popup', on_delete=models.CASCADE)
	popupTitle = models.CharField(max_length=200, null=True)
	popupContent = models.CharField(max_length=200, null=True)

class PopupEngagement(models.Model):
	popupEngagementId = models.ForeignKey(Popup, related_name='popupEngagement', on_delete=models.CASCADE)
	popupEngagementUniqueIdentifier = models.CharField(max_length=15, null=True)
	popupEngagementStart = models.DateTimeField(default=now)
	popupEngagementEnd = models.DateTimeField(null=True)
	#conversationLocation, conversationStartedAtWebsiteLink,

class ChatGPT(models.Model):
	requestId = models.ForeignKey(PopupEngagement, related_name='chatgpt', on_delete=models.CASCADE)
	inputChatGPT = models.TextField(max_length=2000)
	outputChatGPT = models.TextField(max_length=5000, null=True)

