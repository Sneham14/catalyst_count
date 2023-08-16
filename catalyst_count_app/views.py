from django.shortcuts import render, redirect
from allauth.account.forms import SignupForm, LoginForm
from allauth.account.views import login, LoginView, LogoutView
from django.contrib import messages
from allauth.account.decorators import login_required
import os
from .forms import *
from .serializers import *
from .models import *
from .models import MyChunkedUpload
import csv
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from django.http import JsonResponse
from django.conf import settings  # Import Django settings




# Create your views here.

@login_required
def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        try:
            if form.is_valid():
                user = form.save(request)  
                login(request, user)  
                messages.success(request, "Registration Successful. You can now log in.")
                return redirect('user_login')  
            else:
                if 'user_password' in form.errors and 'confirm_password' in form.errors:
                    messages.error(request, "Password and Confirm Password do not match.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
    else:
        form = SignupForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        login_view = LoginView.as_view()
        return login_view(request)
    else:
        form = LoginForm()
        return render(request, 'login.html', {"form":form})
    

def user_logout(request):
    if request.user.is_authenticated:
        LogoutView.as_view()(request)
    return redirect('user_login')  


class Chunk_Upload_View(ChunkedUploadView):
    model = MyChunkedUpload  # Replace with your actual model for storing uploaded files

    def check_permissions(self, request):
        # Add any necessary permission checks here
        pass


class Chunk_Upload_Complete(ChunkedUploadCompleteView):
    model = MyChunkedUpload  # Replace with your actual model for storing uploaded files

    def check_permissions(self, request):
        # Add any necessary permission checks here
        pass

    def upload_complete(self, request, uploaded_file):
        try:
            # Create the "uploads" folder if it doesn't exist within MEDIA_ROOT
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            # Save the uploaded file to the "uploads" folder
            file_path = os.path.join(upload_dir, uploaded_file.name)
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            # Process the uploaded CSV file
            with open(file_path, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                csv_fields = set(reader.fieldnames)
                model_fields = set([field.name for field in CompanyDataModel._meta.get_fields()])
                
                if csv_fields != model_fields:
                    return JsonResponse({'message': 'CSV file fields do not match model fields.'}, status=400)
    
                for row in reader:
                    try:
                        # Convert and save data to CompanyDataModel
                        instance = CompanyDataModel(**row)
                        instance.save()
                    except Exception as e:
                        return JsonResponse({'message': f'Error saving data: {str(e)}'}, status=400)
                    
        except Exception as e:
            return JsonResponse({'message': f'Error processing CSV file: {str(e)}'}, status=500)

        return JsonResponse({'message': 'File uploaded successfully.'})
    
def upload_data(request):
    if request.method == 'POST':
        form = CompanyDataForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'File uploaded successfully.'})
    else:
        form = CompanyDataForm()
    
    return render(request, 'uploaddata.html', {'form': form})


@login_required
def query_builder(request):
    localities = CompanyDataModel.objects.values('locality').distinct()
    sorted_localities = []
    for locality in localities:
        components = locality['locality'].split(', ')
        if len(components) == 3:
            city, state, country = components
            sorted_localities.append({'city': city, 'state': state, 'country': country})

    industries = CompanyDataModel.objects.values('industry').distinct()
    year_founded = CompanyDataModel.objects.values('year_founded').annotate().distinct()
    countries = CompanyDataModel.objects.values('country').annotate().distinct()
    employeesfrom = CompanyDataModel.objects.values('current_employee_estimate').annotate().distinct()
    employeeto = CompanyDataModel.objects.values('total_employee_estimate').annotate().distinct()
    company=CompanyDataModel.objects.values('name').distinct()

    context = {
        'industries': industries,
        'year_founded': year_founded,
        'countries': countries,
        'employeesfrom': employeesfrom,
        'employeeto': employeeto,
        'localities': sorted_localities,
        'company': company,
    }

    if request.method == 'POST':
        filtered_data = CompanyDataModel.objects.all()

        company_filter = request.POST.get('name')
        if company_filter:
            filtered_data = filtered_data.filter(name=company_filter)
        industry_filter = request.POST.get('industry')
        if industry_filter:
            filtered_data = filtered_data.filter(industry=industry_filter)

        year_founded_filter = request.POST.get('year_founded')
        if year_founded_filter:
            filtered_data = filtered_data.filter(year_founded=year_founded_filter)

        currentemployee_filter = request.POST.get('employeesfrom')
        if currentemployee_filter:
            filtered_data = filtered_data.filter(current_employee_estimate__gte=currentemployee_filter)

        totalemployee_filter = request.POST.get('employeeto')
        if totalemployee_filter:
            filtered_data = filtered_data.filter(total_employee_estimate__lte=totalemployee_filter)

        locality_filter = request.POST.get('locality')
        if locality_filter:
            filtered_data = filtered_data.filter(locality=locality_filter)

        country_filter = request.POST.get('country')
        if country_filter:
            filtered_data = filtered_data.filter(country=country_filter)

        result_count = filtered_data.count()
        context['result_count'] = {'total_records': result_count}

    else:
        total_records = CompanyDataModel.objects.count()  # Get the total count from entire dataset
        context['result_count'] = {'total_records': total_records}

    return render(request, 'querybuilder.html', context)


@api_view(['GET'])
def result_count_api(request):
    try:
        serializer = CompanyDataSerializer(data=request.GET)
        if serializer.is_valid():

            filtered_data = CompanyDataModel.objects.filter()

            result_count = filtered_data.count()
            return Response({'total_records': result_count})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@login_required
def add_user(request):
    added_user=None
    cancel_user = request.POST.get('cancel_user')
    if request.method == 'POST' and not cancel_user:
        form = UserDataForm(request.POST)
        if form.is_valid():
            added_user = form.save()
            fm=UserDataForm()
            return render(request, 'adduser.html', {'form':fm , 'message': 'User added successfully.'})
    else:
        form = UserDataForm()

    context = {
        'form': form,
        'added_user': added_user,
    }
    return render(request, 'adduser.html', context)

def users(request):
    data=UserModel.objects.all()
    return render(request, 'users.html',{"data":data})




