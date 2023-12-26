from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.decorators import login_required
from django. contrib import messages 
from django.contrib.auth.models import User,auth
from django.http import HttpResponse
from dashboard.models import ShopType
# @login_required(login_url='user_login') 
def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(request,username=username,password=password)
        if user is not None:

            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'invalid info')
            return redirect('user_login')
    
    else:
        # return render(request,'login.html')

        return render (request,'front/userlogin.html')
    
def user_signup(request):
    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('user_signup')

        if len(password1) < 1:
            messages.error(request, 'Password must be at least 8 characters long')
            return redirect('user_signup')

  
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is not available')
            return redirect('user_signup')

        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered')
            return redirect('user_signup')

 
        user = User.objects.create_user(username=username, email=email, password=password1)
        auth.login(request, user)
        return redirect('home')

    else:
        return render(request, 'front/usersignup.html')
    
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        shop=ShopType.objects.all()
        user=request.user
       
        return render(request, 'front/home.html',{'shop':shop,'user':user})
    else:
        
        return redirect('user_login')
def user_logout(request):
    auth.logout(request)
    messages.info(request,'you have been logged out')
    return redirect('user_login')
    
    
from dashboard.models import Shop

  
# def add_shop(request):
#     user=request.user
#     if user.has_perm('dashboard.add_shop'):
#         if request.method == 'POST':
      
#             shop_name = request.POST.get('shop_name')
#             shop_name_local = request.POST.get('shop_name_local')

#             new_shop = Shop.objects.create(shop_name=shop_name,shop_name_local=shop_name_local)

#             new_shop.user = user
#             new_shop.save()
      
#             return redirect('home')
#         else:

#             return render(request, 'front/add_shop.html')
#     else:
#         return HttpResponse(f'you have no permission to add shop')

@user_passes_test(lambda u: u.has_perm('dashboard.add_shop'))
def add_shop(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        shop_name_local = request.POST.get('shop_name_local')

        new_shop = Shop.objects.create(shop_name=shop_name, shop_name_local=shop_name_local)

        new_shop.user = request.user
        new_shop.save()

        return redirect('home')
    else:
        return render(request, 'front/add_shop.html')
    



      