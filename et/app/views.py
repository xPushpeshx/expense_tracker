from django.shortcuts import render ,HttpResponseRedirect , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import limit_val , expense  , year , month , daily
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
            today=datetime.today()
            this_month = today.strftime('%B')
            months=['January','February','March','April','May','June','July','August','September','October','November','December']
            this_month_index=months.index(this_month)
            for x in months[:this_month_index]:
                data=month(user=user,month_name=x)
                data.save()
            

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
    month_data=month.objects.filter(user=user)
    if month_data.exists():
        total_exp=month.objects.filter(user=user,month_name=this_month).values_list('total_expense',flat=True)[0]
    else:
        total_exp=0
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
                if daily.objects.filter(user=user).exists():
                    daily_data=daily.objects.get(user=user)
                else:
                    daily_data=daily.objects.create(user=user)
                daily_data.record_daily_expense(amount)
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
    if limit.exists():
        cap=limit[0].limit
        left=cap-total
    else:
        cap=0
        left=0
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
    if daily.objects.filter(user=user).exists():
        daily_data=daily.objects.filter(user=user).values('daily_exp')[0]['daily_exp']
    else:
        daily_data=None
    print("daily data",daily_data)
    if request.method == 'POST':     
        if user is not None:
            limit = request.POST.get('limit')
            limit_val(user=user,limit=limit).save()
            month_data=month(user=user,month_name=this_month,total_limit=limit)
            month_data.save()
            messages.success(request, ('Limit has been added to the list!'))
            return redirect('/homepage/')
    if limit:
        val=limit_val.objects.filter(user=user).values('limit').reverse()[0]['limit']
    else:
        val=0
    data_month=month.objects.filter(user=user)
    context={'daily_data':daily_data,'val':val,'total':total,'month':data_month}
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
