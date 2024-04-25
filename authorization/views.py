from django.shortcuts import render,redirect
from django.http import HttpResponse
from core.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Profile,File,DataUpload
from django.contrib import messages
import pandas as pd
import io
from django.core.exceptions import ValidationError
from pathlib import Path,os
import csv
from .statistics import DataPreprocessor
from django.utils import timezone
import time
import hashlib

def Home(request):
    return render(request, 'authorization/index.html')


def Signup(request):
    if request.user.is_authenticated:
    
        messages.info(request, "You are already logged in. Please log out to sign up with a different account.")
        return redirect('home') 
       
    if request.method=='POST':
        username=request.POST.get('username')
        firstname=request.POST.get('fname')
        lastname=request.POST.get('lname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('dob')
        mobile_number = request.POST.get('mobile')

        print(username,firstname,lastname,email,pass1,pass2)
        try:
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered")
                return redirect('home')            

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different username.")
                return redirect('home')
                # return HttpResponse("Username already exists ")
            my_user=User.objects.create_user(username=username,email=email,password=pass1)
            my_user.first_name=firstname
            my_user.last_name=lastname

            if pass1!=pass2:
                return HttpResponse("Your password and confirm password are not same .")
            else:
                my_user.save()
                messages.success(request, "Account created successfully. Please Login.")
                # Create Profile instance
                profile = Profile.objects.create(
                    first_name=firstname,
                    last_name=lastname,
                    username=username,
                    email=email,
                    gender=gender,
                    date_of_birth=date_of_birth,
                    mobile_number=mobile_number,                    
                    user=my_user
                )
                return redirect('login')
        except Exception as e:
            messages.error(request, f"An error occurred while creating user: {str(e)}")
    return render(request,'authorization/signup.html')


def Login(request):
    fname=""
    if request.user.is_authenticated:  # Check if the user is already authenticated
        messages.info(request, "You are already logged in.")
        return redirect('home')    
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('pass1')
        print(username,password)
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            fname=user.first_name
            return redirect('home')
        else:
            messages.error(request,'Bad Credentials')
    return render(request,'authorization/login.html',{'fname':fname})
        

def Logout(request):
    logout(request)
    messages.success(request,'Logged out Successfully !')
    return redirect('home')

def create_db(file_path):
    df=pd.read_csv(file_path,delimiter=',')


def Exist_file(file_name):
    if File.objects.filter(file__icontains=file_name).exists():
        raise ValueError("A file with the same name already exists.")



def validate_csv_file(file):
    # Read the CSV file
    file_content = file.read().decode('utf-8')
    df = pd.read_csv(io.StringIO(file_content))
    
    # Check for duplicate rows
    duplicate_rows = df[df.duplicated()]
    if not duplicate_rows.empty:
        # Remove duplicate rows
        df = df.drop_duplicates()
    
    # Check for missing values
    missing_values = df.isnull().sum().sum()
    if missing_values > 0:
        # Remove rows with missing values
        df = df.dropna()
    
    # Save the cleaned DataFrame to a new CSV file
    # cleaned_csv_file = io.BytesIO()
    cleaned_csv_file = io.StringIO()
    df.to_csv(cleaned_csv_file, index=False, encoding='utf-8')
    
    # Reset file pointer to the beginning
    cleaned_csv_file.seek(0)
    
    return cleaned_csv_file


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # Get the file extension
    valid_extensions = ['.csv', '.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError("Only CSV and Excel files are allowed.")



def Dataupload(request):
    required_columns=['cl1','cl2']
    if request.method == 'POST':
        username = request.POST.get('username', None)
        file = request.FILES.get('file')
        # Check if file is uploaded
        if not file:
            messages.error(request, "No file uploaded.")
            return redirect('home')
        # Validate file extension
        try:
            validate_file_extension(file)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('home')
        try:
           csvfile=validate_csv_file(file)
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('home')        
        try:
            # reader=csv.reader(csvfile)
            user = User.objects.filter(username=username).first()
            if user:
                filename = file.name.split('.')[0]
                reader=pd.read_csv(csvfile)
                # timestamp = timezone.now().strftime("%Y%m%d%H%M%S%f")  # Generate unique timestamp
                # tablename = f"{user.username}_data_{timestamp}"
                # tablename = f"{user.username}_data_{DataUpload.objects.count() + 1}"
                # timestamp = int(time.time() * 1000)  # Unique timestamp in milliseconds
                # tablename = f"{user.username}_data_{timestamp}"             
                # filename_hash = hashlib.sha1(file.name.encode()).hexdigest()[:5]  # Shortened version of filename hash
                # unique_id = str(hash(file.name))[-4:]  # Small unique identifier
                # tablename = f"{user.username}_{filename_hash}_{unique_id}"
                last_row_number = DataUpload.objects.count() + 1
                tablename = f"{user.username}_data_{filename}_{last_row_number}"
    


             # if list(reader.columns)==required_columns:
                #     for row in range(1,len(reader)):
                #         data=list(reader.iloc[row])
                #         instance=DataUpload.objects.create(cl1=data[0],cl2=data[1],user=user)
                #         instance.save()
                #     messages.success(request, "File uploaded successfully.")
                # else:
                #     messages.error(request,'Columns are not macthing')
                for row in range(1,len(reader)):
                    data=list(reader.iloc[row])
                    # timestamp = timezone.now().strftime("%Y%m%d%H%M%S%f")  # Generate unique timestamp
                    # tablename = f"{user.username}_data_{timestamp}"
                    instance=DataUpload.objects.create(cl1=data[0],cl2=data[1],tablename=tablename,user=user)
                    instance.save()
                messages.success(request, "File uploaded successfully.")                
            else:
                messages.error(request,'user does not exist')
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('home')
          
    return render(request,'authorization/datauplod.html')





@login_required(login_url='login')
def Fupload(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        file = request.FILES.get('file')
        # Check if file is uploaded
        if not file:
            messages.error(request, "No file uploaded.")
            return redirect('home')
        # Validate file extension
        try:
            validate_file_extension(file)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('home')
        if username:
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                try:
                    Exist_file(file.name)
                except ValueError as e:
                    messages.error(request,str(e))
                    return redirect('home')   
                try:
                    validate_csv_file(file)
                except ValueError as e:
                    messages.error(request, str(e))
                    return redirect('home')
                          
                obj = File.objects.create(file=file, profile=user) 
                create_db(obj.file)
                messages.success(request, "File uploaded successfully.")
            else:
                messages.error(request, "Username does not exist. Please choose a different username.")
                return redirect('home')
        else:
            messages.error(request, "Username is required.")
            return redirect('home')
    return render(request, 'authorization/fileupload.html')


# def DscriptiveStats(request):
#     context={}
#     df=pd.DataFrame()
#     if request.method=='POST':
#         username = request.POST.get('username', None)
#         try:
#             user = User.objects.filter(username=username).first()
#             if user:
#                 data = DataUpload.objects.filter(user=user)
#                 if data.exists():
#                     cl1_values = [obj.cl1 for obj in data]
#                     cl2_values = [obj.cl2 for obj in data]
#                     # print(cl1_values)
#                     df['cl1']=cl1_values
#                     df['cl2']=cl2_values
#                     # print(df.head(10))
#                 else:
#                     print('No Data Found')
#             else:
#                 print("User not found")
#         except Exception as e:
#             print(e)
#     if not df.empty:
#         preprocessor=DataPreprocessor(df)
#         # info,null_values=preprocessor.analyze_dataset()
#         mean=preprocessor.mean()
#         max=preprocessor.max()
#         df_info=df.describe()
#         context['info']=df_info
#         # context['null_values']=null_values
#         context['mean']=mean
#         context['max']=max
#         context['df']=df
#         graph_filename = preprocessor.linegraph()  # Get the filename of the generated graph
#         context['graph_filename'] = graph_filename  # Pass the filename to the context
#     else:
#         print("Dat Frame is empty")
#         return render(request, 'authorization/error.html', context)
#     return render(request,'authorization/dscriptstats.html',context)


def DscriptiveStats(request):
    context = {}
    df = pd.DataFrame()
    if request.method == 'POST':
        username = request.POST.get('username', None)
        selected_table = request.POST.get('table_name')
        try:
            user = User.objects.filter(username=username).first()
            if user:
                data = DataUpload.objects.filter(user=user, tablename=selected_table)
                if data.exists():
                    cl1_values = [obj.cl1 for obj in data]
                    cl2_values = [obj.cl2 for obj in data]
                    df['cl1'] = cl1_values
                    df['cl2'] = cl2_values
                else:
                    print('No Data Found')
            else:
                print("User not found")
        except Exception as e:
            print(e)
    if not df.empty:
        preprocessor = DataPreprocessor(df)
        mean = preprocessor.mean()
        max = preprocessor.max()
        preprocessor.dropNull()
        preprocessor.fillNull()

        desc=preprocessor.describe().to_dict() 
        quantiles_cl1 = preprocessor.calculate_quantiles('cl1', [0.25, 0.50, 0.75])
        quantiles_cl2 = preprocessor.calculate_quantiles('cl2', [0.25, 0.50, 0.75])
        
        context['quantiles_cl1'] = quantiles_cl1
        context['quantiles_cl2'] = quantiles_cl2         
        context['describe']=desc
        context['mean'] = mean
        context['max'] = max
        context['df'] = df.head(5)
        graph_filename = preprocessor.linegraph()  # Get the filename of the generated graph
        context['graph_filename'] = graph_filename  # Pass the filename to the context
        return render(request, 'authorization/dscriptstats.html', context)
    else:
        return render(request, 'authorization/error.html', context)



# def select_table(request):
#     table_names = []  # Initialize an empty list to store table names
#     if request.method == 'POST':
#         username = request.POST.get('username', None)
#         if username:
#             # Retrieve table names for the given user
#             table_names = DataUpload.objects.filter(user__username=username).values_list('tablename', flat=True).distinct()
#     else:
#         # Retrieve all table names
#         table_names = DataUpload.objects.values_list('tablename', flat=True).distinct()
#     # Pass table_names to the template context
#     return render(request, 'authorization/select_table.html', {'table_names': table_names})


def select_table(request):
    if request.user.is_authenticated:
        username = request.user.username
        # Retrieve table names for the authenticated user
        table_names = DataUpload.objects.filter(user__username=username).values_list('tablename', flat=True).distinct()
        if not table_names:
            # If no tables found for the user, redirect to the data upload page
            return redirect('dataupload')  # Assuming 'data_upload' is the URL name for the data upload page
        else:
            # If tables exist, render the select table page
            return render(request, 'authorization/select_table.html', {'table_names': table_names})
    else:
        # If user is not authenticated, redirect to login page
        return redirect('login')  # Assuming 'login' is the URL name for the login page