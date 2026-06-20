from urllib import request

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User #default user model
from .models import Profile, FoodItem,Order

#home page
def home(request):
    foods=FoodItem.objects.all()
    return render(request, 'home.html', {'foods': foods})

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        role=request.POST['role']
        user=User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, role=role)
        return render(request, 'login.html')
    return render(request,'register.html')

def login_view(request):
    if (request.method=='POST'):
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  #return render(request, 'home.html')
        return render(request, 'login.html')
    return render(request, 'login.html')
    
def logout_view(request):
    logout(request)
    return render(request, 'login.html')

#customer

@login_required
#first page
def place_order(request, food_id):
    food=FoodItem.objects.get(id=food_id)
    order=Order.objects.create(customer=request.user, food=food)
    order.items.add(food)
    return redirect('my_orders')

@login_required
#second page
def my_orders(request):
    orders=Order.objects.filter(customer=request.user)
    return render(request, 'my_orders.html', {'orders': orders})

#delivery partner
@login_required
def delivery_orders(request):
    orders=Order.objects.filter(delivery_partner=request.user)
    return render(request, 'delivery_orders.html', {'orders': orders})

@login_required
def complete_order(request, order_id):
    order=Order.objects.get(id=order_id)
    order.status='delivered'
    order.save()
    return redirect('delivery_orders')