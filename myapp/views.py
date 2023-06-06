from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .models import Code, Customer
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

def home(request):
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'html', 'java', 'javascript', 'markup',
                 'markup-templating', 'matlab', 'mongodb', 'objectivec', 'perl', 'php', 'powershell', 'python', 'r',
                 'regex', 'ruby', 'rust', 'sass', 'scala', 'sql', 'swift', 'yaml']

    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        # Check to make sure they picked a lang
        if lang == "Select Programming Language":
            messages.success(request, "Hey! You Forgot To Pick A Programming Language...")
            return render(request, 'home.html', {'lang_list': lang_list, 'response': code, 'code': code, 'lang': lang})
        else:
            # OpenAI Key
            openai.api_key = "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"
            # Create OpenAI Instance
            openai.Model.list()
            # Make an OpenAI Request
            try:
                response = openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=f"Respond only with code. Fix this {lang} code: {code}",
                    temperature=0,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )
                # Parse the response
                response = (response["choices"][0]["text"]).strip()
                # Save To Database
                record = Code(question=code, code_answer=response, language=lang, user=request.user)
                record.save()

                return render(request, 'home.html', {'lang_list': lang_list, 'response': response, 'lang': lang})

            except Exception as e:
                return render(request, 'home.html', {'lang_list': lang_list, 'response': e, 'lang': lang})

    return render(request, 'home.html', {'lang_list': lang_list})


def suggest(request):
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'dart', 'django', 'go', 'html', 'java', 'javascript', 'markup',
                 'markup-templating', 'matlab', 'mongodb', 'objectivec', 'perl', 'php', 'powershell', 'python', 'r',
                 'regex', 'ruby', 'rust', 'sass', 'scala', 'sql', 'swift', 'yaml']

    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']

        # Check to make sure they picked a lang
        if lang == "Select Programming Language":
            messages.success(request, "Hey! You Forgot To Pick A Programming Language...")
            return render(request, 'suggest.html',
                          {'lang_list': lang_list, 'code': code, 'lang': lang, 'response': code})
        else:
            # OpenAI Key
            openai.api_key = "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"
            # Create OpenAI Instance
            openai.Model.list()
            # Make an OpenAI Request
            try:
                response = openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=f"Respond only with code. Using {lang}. {code}",
                    temperature=0,
                    max_tokens=1000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )
                # Parse the response
                response = (response["choices"][0]["text"]).strip()

                # Save To Database
                record = Code(question=code, code_answer=response, language=lang, user=request.user)
                record.save()

                return render(request, 'suggest.html', {'lang_list': lang_list, 'response': response, 'lang': lang})

            except Exception as e:
                return render(request, 'suggest.html', {'lang_list': lang_list, 'response': e, 'lang': lang})

    return render(request, 'suggest.html', {'lang_list': lang_list})



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


def past(request):
    if request.user.is_authenticated:
        code = Code.objects.filter(user_id=request.user.id)
        return render(request, 'past.html', {"code": code})
    else:
        messages.success(request, "You Must Be Logged In To View This Page")
        return redirect('home')


def delete_past(request, Past_id):
    past = Code.objects.get(pk=Past_id)
    past.delete()
    messages.success(request, "Deleted Successfully...")
    return redirect('past')

@api_view(['GET', 'POST'])
def customers(request):
    """invoke serializer and return to client"""
    if request.method == 'GET':
        data = Customer.objects.all()
        serializer = CustomerSerializer(data, many=True)
        return Response({'customer': serializer.data})
    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'customer': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
def customer(request,id):
    try:
        data = Customer.objects.get(pk=id)
    except Customer.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomerSerializer(data)
        return Response({'customer': serializer.data})
    elif request.method == 'DELETE':
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'POST':
        serializer = CustomerSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'customer': serializer.data})
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def newPopupEngagementCreation(request, clientId):
    try:
        client = Client.objects.get(clientId=clientId)
        popup = Popup.objects.get(popupId=client)
        # Generate a random unique identifier
        popupEngagementUniqueIdentifier = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        serializer = PopupEngagementSerializer(data={'popupEngagementId': popup.id, 'popupEngagementUniqueIdentifier': popupEngagementUniqueIdentifier})
        if serializer.is_valid():
            serializer.save()
            return Response({'customer': serializer.data})
    except Client.DoesNotExist:
        return Response({'error': 'Client does not exist'}, status=404)


@api_view(['GET', 'POST'])
def popup(request, popupId):
    """invoke serializer and return to client"""
    if request.method == 'GET':
        popup = Popup.objects.get(popupId=popupId)
        serializer = PopupSerializer(popup)
        return Response({'popup': serializer.data})
    elif request.method == 'POST':
        serializer = PopupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'popup': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatGPTByClientView(APIView):
    def get(self, request, client_id, popupEngagementUniqueIdentifier):
        try:
            client = Client.objects.get(pk=client_id)
            popup = Popup.objects.get(popupId=client)
            popupEngagement = PopupEngagement.objects.filter(popupEngagementId=popup,
                                                             popupEngagementUniqueIdentifier=popupEngagementUniqueIdentifier).first()
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

    def post(self, request, client_id, popupEngagementUniqueIdentifier):
        try:
            client = Client.objects.get(pk=client_id)
            popup = Popup.objects.get(popupId=client)
            popupEngagement = PopupEngagement.objects.filter(popupEngagementId=popup,


                                                             popupEngagementUniqueIdentifier=popupEngagementUniqueIdentifier).first()

            if popupEngagement:
                """
                openai.api_key = "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"
                # Create OpenAI Instance
                openai.Model.list()
                # Make an OpenAI Request

                response = openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=f"{request.data['inputChatGPT']}",
                    temperature=0,
                    max_tokens=10,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )
                # Parse the response
                response = (response["choices"][0]["text"]).strip()
                """




                serializer = ChatGPTSerializer(data={
                    'requestId': popupEngagement.id,  # Use the primary key of the popupEngagement object
                    'inputChatGPT': request.data['inputChatGPT'],  # Assign the value of 'inputChatGPT' field
                    'outputChatGPT': 'hellooo',  # Assign the value of 'inputChatGPT' field
                })

                if serializer.is_valid():
                    serializer.save()
                    return Response({'popup': serializer.data})
                else:
                    return Response(serializer.errors, status=400)  # Return errors if serializer is not valid
            else:
                return Response({'error': 'Popup engagement does not exist'}, status=404)

        except Client.DoesNotExist:
            return Response({'error': 'Client does not exist'}, status=404)


