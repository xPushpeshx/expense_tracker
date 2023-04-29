from django.shortcuts import render ,HttpResponseRedirect , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import limit_val , expense
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def login_page(request):
    if request.method == 'POST':
        # Login form submitted
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('/homepage/')  # Replace 'home' with your desired URL after login

        # Signup form submitted
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            messages.success(request, ('Succesfully account created!'))
            username = signup_form.cleaned_data.get('username')
            raw_password = signup_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            return redirect('/homepage/')  # Replace 'home' with your desired URL after login

    else:
        # Show both login and signup forms
        login_form = AuthenticationForm()
        signup_form = UserCreationForm()
        return render(request, 'login.html', {'login_form': login_form, 'signup_form': signup_form})
    login_form = AuthenticationForm()
    signup_form = UserCreationForm()
    # If forms are invalid or GET request, show the login/signup page
    return render(request, 'login.html', {'login_form': login_form, 'signup_form': signup_form})



@csrf_exempt
@login_required
def add(request):
    user=request.user
    if request.method == 'POST':
        exp_name = request.POST.get('exp_name')
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        pay_mode = request.POST.get('pay_mode')
        if user is not None:
                data=expense(user=user,exp_name=exp_name,amount=amount,category=category,pay_mode=pay_mode)
                data.save()
                messages.success(request, ('Expense has been added to the list!'))
                return redirect('/add/')
    else:
        return render(request, 'add.html', {})

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

def homepage(request):
    return render(request, 'homepage.html', {})

@csrf_exempt
def limit(request):
    user=request.user
    limit=limit_val.objects.filter(user=user).exists()
    val=0
    if not limit:
        print('limit is none')
        if request.method == 'POST':     
            if user is not None:
                limit = request.POST.get('limit')
                data=limit_val(user=user,limit=limit)
                data.save()
                messages.success(request, ('Limit has been added to the list!'))
                return redirect('/limit/')
    else:
        print('limit is not none')
        messages.error(request, ('Limit has been set for the month'))
        val=(limit_val.objects.filter(user=user)[0].limit)
    return render(request, 'limit.html',{'val':val})

def signup(request):
    return render(request, 'signup.html', {})

def month(request):
    user=request.user
    obj=expense.objects.filter(user=user)
    context={'obj':obj}
    return render(request, 'month.html', context)