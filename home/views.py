from unittest import result
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import size_data
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.template.loader import render_to_string

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score




def home(request):
    
    data = size_data.objects.all() 
    
    
    context = {
        "segment": "home",
        
        "datas": data
        }

    return render(request, "home.html", context=context)
# Create your views here.

def delete_data(request, pk):
    data = get_object_or_404(size_data, pk=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('home')  # Redirect back to the home page or any other page
    return render(request, 'home/delete_confirmation.html', {'data': data})

def add_data(request):
    if request.method == 'POST':
        x_value = request.POST["x"]  # Retrieve 'x' value from form
        y_value = request.POST["y"]  # Retrieve 'x' value from form
        date_value = request.POST.get('date')  # Retrieve 'date' value from POST data
        if date_value:
            try:
                # Parse the date_value assuming it's in the format provided by datetime-local input
                date_value = timezone.datetime.strptime(date_value, '%Y-%m-%dT%H:%M')
            except ValueError:
                return HttpResponse('Invalid date format. Please use YYYY-MM-DDTHH:MM format.')
        else:
            return HttpResponse('Date field cannot be empty.')

        if x_value is not None and y_value is not None and date_value is not None:
            obj = size_data(x=x_value, y=y_value, date=date_value)
            obj.save()
            return redirect('home')

    return redirect('home')


def edit_data(request, pk):
    obj = get_object_or_404(size_data, pk=pk)
    if request.method == 'POST':
        x_value = request.POST.get('x')
        y_value = request.POST.get('y')

        if x_value and y_value:
            obj.x = x_value
            obj.y = y_value
            obj.save()
            return redirect('home')
        else:
            return HttpResponse('Invalid input.')
    return redirect('home')

def prediction_data(request):
    
    if request.method == 'POST':
        x_value = request.POST.get('input1')

        # Convert x_value to float (assuming x_value is numeric input)
        try:
            x_value = float(x_value)
        except ValueError:
            return render(request, 'home.html', {'error': 'Invalid input. Please enter a numeric value.'})

        # Fetch data from the database
        data_points = size_data.objects.all()

        # Prepare the data
        x = np.array([float(data_point.x) for data_point in data_points]).reshape(-1, 1)
        y = np.array([float(data_point.y) for data_point in data_points])

        # Split the data into training and testing sets
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        # Train the model
        model = LinearRegression()
        model.fit(x_train, y_train)

        # Function to predict the y value for a new input x
        def predict_new_value(input_value):
            new_data = np.array([[input_value]])  # Convert input value to the required shape
            prediction = model.predict(new_data)
            return prediction[0]

        # Get the predicted y value for the new input x_value
        predicted_y = predict_new_value(x_value)

        # Fetch all data points for rendering
        data = size_data.objects.all()

        context = {
            'ysegment': predicted_y,
            'xsegment': x_value,
            
            'datas': data
        }

        return render(request, 'home.html', context=context)


    return redirect('home')

@csrf_exempt
def submit_data_ajax(request):
    # context = {}
    
    if request.method == 'POST':
        input1 = request.POST.get('input1')
        
        print(input1)
        data = size_data.objects.filter(x=input1)
        
        
        data_list = list(data.values('x', 'y', 'date'))  # Customize fields as needed
        print(data_list)
        return JsonResponse({'message': 'Search successful', 'data': data_list})
    
    # Handle GET request or non-ajax POST request
    return JsonResponse({'error': 'Invalid request'})