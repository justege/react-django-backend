from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from myapp.models import Client, Popup, ChatGPT, PopupEngagement
from django.http import JsonResponse, Http404
from myapp.serializers import *
import openai
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import random
import string
from django.core.exceptions import ObjectDoesNotExist

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!  Woohoo!")
            return redirect('home')
        else:
            messages.success(request, "Error Logging In. Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out... Have A Nice Day!")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Registered...Congrats!!")
            return redirect('home')

    else:
        form = SignUpForm()

    return render(request, 'register.html', {"form": form})

@api_view(['POST'])
def newPopupEngagementCreation(request, popupId, clientId):
    try:
        client = Client.objects.get(clientId=clientId)
        popup = Popup.objects.get(id=popupId, popupId=client)
        # Generate a random unique identifier
        popupEngagementUniqueIdentifier = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        serializer = PopupEngagementSerializer(data={'popupEngagementId': popup.id, 'popupEngagementUniqueIdentifier': popupEngagementUniqueIdentifier})
        if serializer.is_valid():
            serializer.save()
            return Response({'customer': serializer.data})
    except Client.DoesNotExist:
        return Response({'error': 'Client does not exist'}, status=404)


@api_view(['GET', 'POST'])
def popup(request, popupId, clientId):
    """invoke serializer and return to client"""
    if request.method == 'GET':
        client = Client.objects.get(clientId=clientId)
        popup = Popup.objects.get(id=popupId, popupId=client)
        serializer = PopupSerializer(popup)
        return Response({'popup': serializer.data})
    elif request.method == 'POST':
        serializer = PopupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'popup': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatGPTByClientView(APIView):
    def get(self, request, clientId, popupId, popupEngagementUniqueIdentifier):
        try:
            client = Client.objects.get(clientId=clientId)
            popup = Popup.objects.get(id=popupId, popupId=client)
            popupEngagement = PopupEngagement.objects.filter(popupEngagementId=popup, popupEngagementUniqueIdentifier=popupEngagementUniqueIdentifier).first()
            popupAdditional = PopupAdditional.objects.filter(popupAdditionalId=popup)
            Additionalserializer = AdditionalSerializer(popupAdditional, many=True)

            if popupEngagement and popupAdditional:
                chatgpts = ChatGPT.objects.filter(requestId=popupEngagement)
                ChatGPTserializer = ChatGPTSerializer(chatgpts, many=True)

                return Response({'chatgpt': ChatGPTserializer.data, 'popupAdditional': Additionalserializer.data})
            else:
                return Response({'error': 'Popup engagement does not exist'}, status=404)

        except Client.DoesNotExist:
            return Response({'error': 'Client does not exist'}, status=404)

    def post(self, request, clientId, popupId, popupEngagementUniqueIdentifier):
        try:
            client = Client.objects.get(clientId=clientId)
            popup = Popup.objects.get(id=popupId, popupId=client)
            popupEngagement = PopupEngagement.objects.filter(popupEngagementId=popup, popupEngagementUniqueIdentifier=popupEngagementUniqueIdentifier).first()

            if popupEngagement:
                """
                The rest of your code
                """
                serializer = ChatGPTSerializer(data={
                    'requestId': popupEngagement.id,
                    'inputChatGPT': request.data['inputChatGPT'],
                    'chatWebsiteURL': request.data['chatWebsiteURL'],
                    'outputChatGPT': 'Well, in this case, we can make a discount for you, here is your discount code: HELLOWorld1202. You can go ahead and buy the article buy closing this popup!',
                })

                if serializer.is_valid():
                    serializer.save()
                    chatGPT_object = serializer.instance  # Get the saved chatGPT object
                    chatgpts = [chatGPT_object]  # Create a list with the new chatGPT object
                    ChatGPTserializer = ChatGPTSerializer(chatgpts, many=True)  # Serialize the list
                    return Response({'chatgpt': ChatGPTserializer.data})
                else:
                    return Response(serializer.errors, status=400)
            else:
                return Response({'error': 'Popup engagement does not exist'}, status=404)

        except Client.DoesNotExist:
            return Response({'error': 'Client does not exist'}, status=404)
