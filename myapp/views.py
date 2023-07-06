from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from myapp.models import Client, Popup, ChatGPT, PopupEngagement
from django.http import JsonResponse, Http404, HttpResponse
from myapp.serializers import *
import openai
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import random
import string
from django.core.exceptions import ObjectDoesNotExist
# Initialize the OpenAI API client
openai.api_key = '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'


def PopupFilesView(request, clientId):
    # Retrieve the latest PopupFiles instance uploaded by the current user
    popup_file = get_object_or_404(PopupFiles, uploaded_by=clientId)

    if popup_file:
        return popup_file.file
    else:
        return HttpResponse("No file uploaded")

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
            additionalSerializer = AdditionalSerializer(popupAdditional, many=True)

            if popupEngagement and popupAdditional:
                chatgpts = ChatGPT.objects.filter(requestId=popupEngagement)
                ChatGPTserializer = ChatGPTSerializer(chatgpts, many=True)

                return Response({'chatgpt': ChatGPTserializer.data, 'popupAdditional': additionalSerializer.data})
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


                general_info = GeneralInformationForChatGPT.objects.filter(chatGPTInformationKey=popup).first()
                product_info = PopupProducts.objects.filter(productSpecificChatGPTInformationKey=popup).first()

                # Construct the input prompt for the ChatGPT API
                input_prompt = []

                conversation_history = ChatGPT.objects.filter(requestId=popupEngagement).values_list('inputChatGPT', flat=True)

                input_prompt.append(
                    f"\n I created a chatbot on a popup that is embedded at my customers website where visitors can engage with that chatbot which is you. I will provide you the informations of my customers data below so that you can answer visitors questions or help them along.  Additionally i will provide you the chat history if there is any in my database storing all you and the visitors inputs. Some abbreviations I use in my database are as follows:PreviousInputOfCustomer is the previous chat history of the visitor of my customer, PreviousOutputOfChatGPT is your previous historical answer saved on my server (so please stay consistent in your answers), latestInputOfCustomer is the latest input of the websites visitor which needs to be answered/guided by you (according to all other historical text and information i gave you).Please act as a support and marketing chatbot.  Please give the answer directly without using ‘LatestOutputOfChatGPT' or 'outputChatGPT' or 'PreviousOutputOfChatGPT:' etc ... you are directly engaging with the visitor.Please write in a happy and helpful mood. Write an answer that is shorter than 100 characters.")

                input_prompt.append(f"Visitor is currently at website url: {popupEngagement.conversationStartedAtWebsiteLink}")

                if general_info:
                    input_prompt.append(f"Problem: {general_info.whatProblemIsYourCompanySolving}")
                    input_prompt.append(f"Services: {general_info.whatServicesDoYouOffer}")
                    input_prompt.append(f"Contact: {general_info.howCanCustomersReachYouOrYourTeam}")
                    input_prompt.append(f"FAQs: {general_info.whatAreFAQs}")
                    input_prompt.append(f"Other Info: {general_info.anyOtherInformation}")
                    input_prompt.append(f"Discount: {general_info.howMuchDiscountCanYouDoMaximum}")
                    input_prompt.append(f"Popup Title and Content: {general_info.doYouWantYourOwnPopupTitleAndContent}")
                    input_prompt.append(f"Most Sold Product: {general_info.whatIsYourMostSoldProduct}")

                if product_info:
                    input_prompt.append(f"Product Price: {product_info.productPrice}")
                    input_prompt.append(f"Product Currency: {product_info.productCurrency}")
                    input_prompt.append(f"Discountable: {product_info.productIsDiscountable}")
                    input_prompt.append(f"Product Specs: {product_info.productSpecs}")

                # Append the existing inputChatGPT to the conversation history
                # Retrieve the existing conversation history for the popupEngagementUniqueIdentifier

                previous_outputs = ChatGPT.objects.filter(requestId=popupEngagement).values_list('outputChatGPT', flat=True)

                # Concatenate the previous inputs and outputs with the conversation history
                for i in range(len(conversation_history)):
                    input_prompt.append(f"PreviousInputOfCustomer: {conversation_history[i]}")
                    input_prompt.append(f"PreviousOutputOfChatGPT: {previous_outputs[i]}")
                input_prompt.append(f"latestInputOfCustomer: {request.data['inputChatGPT']}")

                conversation_prompt = '\n'.join(input_prompt)
                print('conversation_history', conversation_history)
                # Call the ChatGPT API to generate the response

                response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages = [{'role': 'user', 'content': conversation_prompt}],
                )

                # Extract the generated output from the API response
                output_gpt = response.choices[0]["message"]["content"]

                print(output_gpt)

                # Continue with the rest of your code
                serializer = ChatGPTSerializer(data={
                    'requestId': popupEngagement.id,
                    'inputChatGPT': request.data['inputChatGPT'],
                    'outputChatGPT': str(output_gpt),
                })

                if serializer.is_valid():
                    serializer.save()
                    chatGPT_object = serializer.instance  # Get the saved chatGPT object
                    chatgpts = [chatGPT_object]  # Create a list with the new chatGPT object
                    ChatGPTserializer = ChatGPTSerializer(chatgpts, many=True)  # Serialize the list
                    return Response({'chatgpt': ChatGPTserializer.data})
                else:
                    return Response(serializer.errors, status=400)


        except Client.DoesNotExist:
            return Response({'error': 'Client does not exist'}, status=404)