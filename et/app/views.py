from django.shortcuts import render ,HttpResponseRedirect , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import limit_val , expense  , year , month
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login
from .forms import UserRegisterForm ,AuthenticateForm
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail


def login_page(request):
    if request.method == 'POST':
        # Login form submitted
        login_form = AuthenticateForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('/homepage/')  # Replace 'home' with your desired URL after login

        # Signup form submitted
        signup_form = UserRegisterForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            subject = 'Successfully Registered'
            message = f'Hi {user.username}, thank you for registering in Exepense Tracker.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            messages.success(request, ('Succesfully account created!'))
            username = signup_form.cleaned_data.get('username')
            raw_password = signup_form.cleaned_data.get('password1')
            email = signup_form.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password, email=email)
            login(request,user)
            return redirect('/homepage/')  # Replace 'home' with your desired URL after login

    else:
        # Show both login and signup forms
        login_form = AuthenticateForm()
        signup_form = UserRegisterForm()
        return render(request, 'login_signup.html', {'login_form': login_form, 'signup_form': signup_form})
    login_form = AuthenticateForm()
    signup_form = UserRegisterForm()
    # If forms are invalid or GET request, show the login/signup page
    return render(request, 'login_signup.html', {'login_form': login_form, 'signup_form': signup_form})



@csrf_exempt
@login_required
def add(request):
    user=request.user
    today=datetime.today()
    this_month = today.strftime('%B')
    print(this_month)
    
    month_data=month.objects.filter(user=user)
    total_exp=month.objects.filter(user=user,month_name=this_month).values_list('total_expense',flat=True)[0]
    print(total_exp)
    if request.method == 'POST':
        exp_name = request.POST.get('exp_name')
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        pay_mode = request.POST.get('pay_mode')
        total, cap ,left=total_money(request)
        if user is not None and (total+int(amount))<=cap:
                data=expense(user=user,exp_name=exp_name,amount=amount,category=category,pay_mode=pay_mode)
                data.save()
                if month.objects.filter(user=user,month_name=this_month).exists():
                    month.objects.filter(user=user,month_name=this_month).update(total_expense=total_exp+int(amount))
                else:
                    data=month(user=user,month_name=this_month,total_expense=total_exp+int(amount))
                    data.save()
                if left < (cap)*2/10:
                    subject = 'Expense Limit'
                    message = f'You have {left} rupee left of your expense limit'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [user.email, ]
                    send_mail( subject, message, email_from, recipient_list )
                messages.success(request, ('Expense has been added to the list!'))
                
                print(month_data)
                return redirect('/add/')
    else:
        obj=expense.objects.filter(user=user).order_by('-exp_id')[:5]
        context={'obj':obj}
        return render(request, 'add.html', context)
    obj=expense.objects.filter(user=user).order_by('-exp_id')[:5]
    context={'obj':obj}
    return render(request, 'add.html', context)

def total_money(request):
    user=request.user
    obj=expense.objects.filter(user=user)
    limit=limit_val.objects.filter(user=user)
    food_amount,entertainment_amount,stocks_amount,rent_amount,emi_amount,others_amount=0,0,0,0,0,0
    for x in obj:
        if x.category=='food':
            food_amount+=x.amount
        elif x.category=='entertainment':
            entertainment_amount+=x.amount
        elif x.category=='stocks':
            stocks_amount+=x.amount
        elif x.category=='rent':
            rent_amount+=x.amount
        elif x.category=='emi':
            emi_amount+=x.amount
        elif x.category=='others':
            others_amount+=x.amount
    total=food_amount+entertainment_amount+stocks_amount+rent_amount+emi_amount+others_amount
    cap=limit[0].limit
    left=cap-total
    return total, cap ,left

def display(request):
    user=request.user
    obj=expense.objects.filter(user=user)
    limit=limit_val.objects.filter(user=user)
    if user.is_authenticated:
        food_amount,entertainment_amount,stocks_amount,rent_amount,emi_amount,others_amount=0,0,0,0,0,0
        for x in obj:
            if x.category=='food':
                food_amount+=x.amount
            elif x.category=='entertainment':
                entertainment_amount+=x.amount
            elif x.category=='stocks':
                stocks_amount+=x.amount
            elif x.category=='rent':
                rent_amount+=x.amount
            elif x.category=='emi':
                emi_amount+=x.amount
            elif x.category=='others':
                others_amount+=x.amount
        total=food_amount+entertainment_amount+stocks_amount+rent_amount+emi_amount+others_amount
        left=limit[0].limit-total
        combine=[food_amount,entertainment_amount,stocks_amount,rent_amount,emi_amount,others_amount,total,left]
        context={'combine':combine}
        print(context)
        return render(request,"display.html",context)
    else:
        return render(request, 'display.html', {})

def edit(request):
    return render(request, 'edit.html', {})

@csrf_exempt
def homepage(request):
    today=datetime.today()
    this_month = today.strftime('%B')
    user=request.user
    total, cap ,left=total_money(request)
    limit=limit_val.objects.filter(user=user).exists()
    val=0
    if not limit:
        print('limit is none')
        if request.method == 'POST':     
            if user is not None:
                limit = request.POST.get('limit')
                data=limit_val(user=user,limit=limit)
                data.save()
                month_data=month(user=user,month=this_month,total_limit=limit)
                month_data.save()
                messages.success(request, ('Limit has been added to the list!'))
                return redirect('/limit/')
    else:
        print('limit is not none')
        messages.error(request, ('Limit has been set for the month'))
        val=(limit_val.objects.filter(user=user)[0].limit)
    data_month=month.objects.filter(user=user)
    data_daily=expense.objects.filter(user=user).values('date')
    context={'data_daily':data_daily,'val':val,'total':total,'month':data_month}
    return render(request, 'homepage.html', context)

def signup(request):
    return render(request, 'signup.html', {})

def month_view(request):  
    user=request.user
    obj=expense.objects.filter(user=user)
    context={'obj':obj}
    return render(request, 'month.html', context)

def news(request):
    import requests 
    import json
    news_api_request=requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=c9d36ebf21234679820ae4df3eb4f688")
    api=json.loads(news_api_request.content)
    return render(request,'news.html',{'api':api})
