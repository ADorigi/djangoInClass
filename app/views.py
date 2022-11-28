import random
import string

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import OrderForm, InterestForm, LoginForm, RegisterForm, ForgotPasswordForm
from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from django.conf import settings
from django.core.mail import send_mail

from datetime import datetime

# Create your views here.


def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(datetime.now())
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('app:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'app/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('app:index')))


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            register_form = form.save(commit=False)
            register_form.save()
            return HttpResponse('<h2>You have been registered!</h2>')
        else:
            return HttpResponse('<h2>Invalid Form</h2>')
    else:
        form = RegisterForm()
        return render(request, 'app/register.html', {'form': form})


def myorders(request):
    try:
        client = Client.objects.get(id = request.user.id)
        orders = Order.objects.filter(client=client)
        return render(request, 'app/myorders.html', {'orders': orders})
    except:
        # return HttpResponse('<h2>You are not a registered client!</h2>')
        form = LoginForm()
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    request.session['last_login'] = str(datetime.now())
                    request.session.set_expiry(3600)
                    client = Client.objects.get(id=request.user.id)
                    orders = Order.objects.filter(client=client)
                    return render(request, 'app/myorders.html', {'orders': orders})
                    # return HttpResponseRedirect(reverse('app:index'))
                else:
                    return HttpResponse('Your account is disabled.')
            else:
                return HttpResponse('Invalid login details.')
        else:
            return render(request, 'app/login.html', {'form': form})


def index(request):
    last = "more than one hour ago"
    if 'last_login' in request.session:
        last = str(request.session['last_login'])
    cat_list = Category.objects.all().order_by('id')[:10]
    return render(request, 'app/index.html', {'cat_list': cat_list, 'last_login': "Your last login was "+ last})


def about(request):

    if 'about_visits' in request.session:
        request.session['about_visits'] += 1
    else:
        request.session['about_visits'] = 1
    request.session.set_expiry(300)
    return render(request, 'app/about.html', {'about_visits': request.session['about_visits']})


def detail(request, cat_no):

    category = get_object_or_404(Category, name=cat_no)
    product_list = Product.objects.filter(category=category)
    return render(request, 'app/detail.html',
                  {'cat_no': cat_no,
                   'category': category,
                   'product_list': product_list})


def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'app/products.html', {'prodlist': prodlist})


def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                Product.objects.filter(id=order.product.id).update(stock = (order.product.stock - order.num_units))
                order.save()
                msg = 'Your order has been placed successfully.'
                return render(request, 'app/order_response.html', {'msg': msg})
            else:
                msg = 'We do not have sufficient stock to fill your order.'
                return render(request, 'app/order_response.html', {'msg': msg})

    else:
        form = OrderForm()
        return render(request, 'app/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


def productdetail(request, prod_id):
    product = Product.objects.get(id=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['interested'] == '1':
                Product.objects.filter(id=product.id).update(interested=(product.interested + 1))
                cat_list = Category.objects.all().order_by('id')[:10]
                return render(request, 'app/index.html', {'cat_list': cat_list})

    else:
        if product.stock == 0:
            msg = "Product out of stock"
        else:
            msg = ''
        form = InterestForm()
        return render(request, 'app/productdetail.html', {'form': form,
                                                          'name': product.name,
                                                          'interested': product.interested,
                                                          'price': product.price,
                                                          'msg': msg})


def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        username = request.POST['username']
        try:
            client = Client.objects.get(username=username)
            letters = string.ascii_lowercase + string.ascii_uppercase
            new_password = ''.join(random.choice(letters) for i in range(10))
            subject = 'New password requested'
            message = f"Hi {client.username}, your new password is '{new_password}'"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [client.email,]
            send_mail(subject, message, email_from, recipient_list)
            client.set_password(new_password)
            client.save()
            return HttpResponse("<h2>Check email for your new password</h2>")
        except:
            return HttpResponse("<h2>Username does not exist</h2>")
    else:
        return render(request, 'app/forgot_password.html', {'form': form})