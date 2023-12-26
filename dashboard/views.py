from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django. contrib import messages 
from django.contrib.auth.models import User,auth,Permission
from .models import ShopType
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
import os
import fitz 
from .forms import ShopForm   
from .models import Shop

from django.http import JsonResponse


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(request,username=username,password=password)
        if user is not None:

            auth.login(request,user)
            return redirect('dashboard')
        else:
            messages.info(request,'invalid info')
            return redirect('login')
    
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'you have been logged out')
    return redirect('login')


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def dashboard(request):
    user = request.user.username

    return render (request , 'dashboard.html',{'user':user})

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
# @user_passes_test(lambda u: u.has_perm('dashboard.view_shoptype'))
def shoptype(request):
    lists=ShopType.objects.order_by('id')
    

    return render (request, 'shoptype/shoptype.html',{'shop_types':lists})
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# def shoptype(request):
    
#     all_shop_types = ShopType.objects.order_by('id')

#     paginator = Paginator(all_shop_types, 2)

#     page = request.GET.get('page')

#     try:
#         shop_types = paginator.page(page)
#     except PageNotAnInteger:
#         # If the page parameter is not an integer, deliver the first page
#         shop_types = paginator.page(1)
#     except EmptyPage:
#         # If the page is out of range (e.g., 9999), deliver the last page
#         shop_types = paginator.page(paginator.num_pages)

#     # Pass the paginated ShopType objects to the template
#     return render(request, 'shoptype/shoptype.html', {'shop_types': shop_types})
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def viewshoptype(request, pk):
    shop = Shop.objects.get(id=pk)
    return render(request, 'shoptype/shoptype.html', {'shop': shop})
# ////////////////////////////////////
from django.db.models import Q
# for search
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def shoptypesearch(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton = request.GET.get('submit')

        if query is not None:
            lookups = Q(name__icontains=query)
            results = ShopType.objects.filter(lookups).distinct()

            context = {'results': results, 'submitbutton': submitbutton}
            return render(request, 'shoptype/shoptype.html', context)
        else:
            return render(request, 'shoptype/shoptype.html')
    else:
        return render(request, 'shoptype/shoptype.html')
# ////////////////////////////////////////////



from django.http import HttpResponseForbidden

from .forms import ShopTypeForm
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def addshoptype(request):
    if request.user.has_perm('dashboard.add_shoptype'):
    
        form=ShopTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('shoptype')
        else:
            
            return render (request , 'shoptype/addshoptype.html',{'form':form})
    else:
        return HttpResponseForbidden("You do not have permission to add shop types.")




@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def editshoptype(request , pk):
    if request.user.has_perm('dashboard.change_shoptype'):
        current_shoptype=ShopType.objects.get(id=pk)
        form=ShopTypeForm(request.POST or None ,instance=current_shoptype)
        if form.is_valid():
            form.save()
            return redirect ('shoptype')
        else:
            return render (request , 'shoptype/editshoptype.html',{'form':form})
        
    else:
        return  redirect ('shoptype') 
    

    
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def deleteshoptype(request , pk):
    delete_it=ShopType.objects.get(id=pk)
    delete_it.delete()
    return redirect ('shoptype')

# //////////////////////////////////////////////////////////////////////////////////////////////////////
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def block_shop_type(request, pk):
    shop_type = get_object_or_404(ShopType, id=pk)
    shop_type.is_active = False
    shop_type.save()
    return redirect('shoptype')

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def activate_shop_type(request, pk):
    shop_type = get_object_or_404(ShopType, id=pk)
    shop_type.is_active = True
    shop_type.save()
    return redirect('shoptype')

# //////////////////////////////////////////////////////////////////
from .models import Category
from .forms import CategoryForm
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def category(request):
    lists=Category.objects.order_by('sort_order')


    return render (request ,'category/category.html',{'lists':lists})

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def addcat(request):
    form=CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        print('done')
        return redirect('category')
    else:
        
        return render (request , 'category/addcat.html',{'form':form})
    
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def editcat(request, pk):
    current_cat=Category.objects.get(id=pk)
    form = CategoryForm(request.POST or None ,instance=current_cat)
    if form.is_valid():
        form.save()
        return redirect('category')
    else:


        return render (request ,'category/editcat.html', {'form':form})
    




@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def shop(request):
    lists = Shop.objects.order_by('id')
    current_date = timezone.now().date()

    for shop_instance in lists:
        shop_instance.days_left = (shop_instance.expired_date - current_date).days

    return render(request, 'shops/shop.html', {'lists': lists,})
from datetime import timedelta

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def renew_subscription(request, list_id):
    list_instance = get_object_or_404(Shop, id=list_id)

    if request.method == 'POST':
        months_to_add = int(request.POST.get('date', 0))
        if months_to_add:
            list_instance.expired_date += timedelta(days=30 * months_to_add)
            list_instance.save()
            return redirect ('shop')  

    return render(request, 'shop.html', {'list_instance': list_instance})


  


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def block_shop(request, pk):
    shop_type = get_object_or_404(Shop, id=pk)
    shop_type.is_active = False
    shop_type.save()
    return redirect('shop')

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def activate_shop(request, pk):
    shop_type = get_object_or_404(Shop, id=pk)
    shop_type.is_active = True
    shop_type.save()
    return redirect('shop')








# def addshop(request):
#     if request.method == 'POST':
#         form = ShopForm(request.POST, request.FILES)
#         if form.is_valid():
#             shop = form.save()

#             if shop.menu_brochure.name.endswith('.pdf'):
#                 image_dir = f'media/menu_brochures/images/shop_{shop.id}/'
#                 os.makedirs(image_dir, exist_ok=True)

#                 pdf_path = shop.menu_brochure.path

               
#                 pdf_document = fitz.open(pdf_path)

#                 for page in pdf_document.pages():
#                     page.set_rotation(0)

#                 rotated_pdf_path = image_dir + f'rotated{shop.id}.pdf'
#                 pdf_document.save(rotated_pdf_path)

#                 pdf_document.close()

#                 # openin th rotated file
#                 with open(rotated_pdf_path, 'rb') as rotated_pdf_file:
#                     # Save to men bro field
#                     shop.menu_brochure.save(f'rotated{shop.id}.pdf', rotated_pdf_file)

#                 os.remove(rotated_pdf_path)

#                 if shop.menu_brochure.name.endswith('.pdf'):


#                     image_dir = f'media/menu_brochures/images/shop_{shop.id}/'
#                     os.makedirs(image_dir, exist_ok=True)  
#                     pdf_path = shop.menu_brochure.path

#                     pdf_document = fitz.open(pdf_path)

                    
#                     for page_number in range(pdf_document.page_count):
#                         page = pdf_document.load_page(page_number)
#                         image = page.get_pixmap()
#                         image.save(image_dir + f'page_{page_number + 1}.jpg')

#             return redirect('shop')

#     else:
#         form = ShopForm()

#     return render(request, 'shops/addshop.html', {'form': form})



from .forms import ShopForm, ModelBFormSet
from .models import Icon


from django.db import transaction

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
@user_passes_test(lambda u: u.has_perm('dashboard.add_shop'))
def create(request):
    
    if request.method == 'POST':
        shop_form = ShopForm(request.POST,request.FILES)
        icon_formset = ModelBFormSet(request.POST, request.FILES, prefix='icons')

        if shop_form.is_valid() and icon_formset.is_valid():
            with transaction.atomic():
                # Save the Shop instance
                shop_instance = shop_form.save()

                # Link the Shop instance to each Icon instance in the formset
                icons = icon_formset.save(commit=False)
                for icon in icons:
                    icon.shop = shop_instance
                    icon.save()

                # Save the formset to handle any additional changes
                icon_formset.save_m2m()
                if shop_instance.menu_brochure.name.endswith('.pdf'):
                    image_dir = f'media/menu_brochures/images/shop_{shop_instance.id}/'
                    os.makedirs(image_dir, exist_ok=True)

                    pdf_path = shop_instance.menu_brochure.path

                
                    pdf_document = fitz.open(pdf_path)

                    for page in pdf_document.pages():
                        page.set_rotation(0)

                    rotated_pdf_path = image_dir + f'rotated{shop_instance.id}.pdf'
                    pdf_document.save(rotated_pdf_path)

                    pdf_document.close()

                    # openin th rotated file
                    with open(rotated_pdf_path, 'rb') as rotated_pdf_file:
                        # Save to men bro field
                        shop_instance.menu_brochure.save(f'rotated{shop_instance.id}.pdf', rotated_pdf_file)

                    os.remove(rotated_pdf_path)

                    if shop_instance.menu_brochure.name.endswith('.pdf'):


                        image_dir = f'media/menu_brochures/images/shop_{shop_instance.id}/'
                        os.makedirs(image_dir, exist_ok=True)  
                        pdf_path = shop_instance.menu_brochure.path

                        pdf_document = fitz.open(pdf_path)

                        
                        for page_number in range(pdf_document.page_count):
                            page = pdf_document.load_page(page_number)
                            image = page.get_pixmap()
                            image.save(image_dir + f'page_{page_number + 1}.jpg')

            return redirect('shop')

        else:
             print(shop_form.errors)
             print(icon_formset.errors)
             return HttpResponse('error')
            
            
    else:
        shop_form = ShopForm()
        icon_formset = ModelBFormSet(prefix='icons')

    # Render the initial form or formset
    return render(request, 'tester.html', {'form': shop_form, 'icon_formset': icon_formset})

#  for depended drop down

def get_categories(request):
    shoptype_id = request.GET.get('shoptype_id')
    categories = Category.objects.filter(shoptype_id=shoptype_id).values('id', 'name')
    print(categories)

    return JsonResponse({'categories': list(categories)})



def flipbook(request, pk):
    shop = get_object_or_404(Shop, id=pk)

    
    
    image_dir = f'media/menu_brochures/images/shop_{shop.id}/'
    image_files = []

    for filename in natsorted(os.listdir(image_dir)):
        if filename.endswith('.jpg'):
            image_files.append(f'/{image_dir}{filename}')  

    user_agent = request.META.get('HTTP_USER_AGENT', '')
    parsed_user_agent = parse(user_agent)


    is_phone_request = parsed_user_agent.is_mobile
    

    if is_phone_request:
        
        if shop.pay_type=='basic':
            return render(request, 'shops/basic.html', {'shop': shop, 'image_files': image_files})
        else:
            return render(request, 'test.html', {'shop': shop, 'image_files': image_files})
    
    else:
       
        if shop.pay_type=='basic':
             return render(request, 'shops/basic.html', {'shop': shop, 'image_files': image_files})
            
        else:
             return render(request, 'shops/viewshop.html', {'shop': shop, 'image_files': image_files})















def editshop(request, pk):
    shop = get_object_or_404(Shop, id=pk)

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            if 'menu_brochure' in form.changed_data:
            # Delete previous PDF and images
                delete_previous_files(shop)

            shop = form.save()
            if shop.menu_brochure.name.endswith('.pdf'):
                image_dir = f'media/menu_brochures/images/shop_{shop.id}/'
                os.makedirs(image_dir, exist_ok=True)

                pdf_path = shop.menu_brochure.path

               
                pdf_document = fitz.open(pdf_path)

                for page in pdf_document.pages():
                    page.set_rotation(0)

                rotated_pdf_path = image_dir + f'rotated{shop.id}.pdf'
                pdf_document.save(rotated_pdf_path)

                pdf_document.close()

                # openin th rotated file
                with open(rotated_pdf_path, 'rb') as rotated_pdf_file:
                    # Save to men bro field
                    shop.menu_brochure.save(f'rotated{shop.id}.pdf', rotated_pdf_file)

                os.remove(rotated_pdf_path)

                if shop.menu_brochure.name.endswith('.pdf'):


                    image_dir = f'media/menu_brochures/images/shop_{shop.id}/'
                    os.makedirs(image_dir, exist_ok=True)  
                    pdf_path = shop.menu_brochure.path

                    pdf_document = fitz.open(pdf_path)

                    
                    for page_number in range(pdf_document.page_count):
                        page = pdf_document.load_page(page_number)
                        image = page.get_pixmap()
                        image.save(image_dir + f'page_{page_number + 1}.jpg')

            

            return redirect('shop')  

    else:
        form = ShopForm(instance=shop)

    return render(request, 'shops/editshop.html', {'form': form, 'current_shop': shop})

def delete_previous_files(shop):
    # Delete previous PDF
    previous_pdf_path = shop.menu_brochure.path
    if os.path.exists(previous_pdf_path):
        os.remove(previous_pdf_path)

    # Delete previous images
    previous_images_dir = f'media/menu_brochures/images/shop_{shop.id}/'
    if os.path.exists(previous_images_dir):
        for file_name in os.listdir(previous_images_dir):
            file_path = os.path.join(previous_images_dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(previous_images_dir)










@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def load_cities(request):
    shoptype_id = request.GET.get('shoptype_id')
    category = Category.objects.filter(shoptype_id=shoptype_id).all()
    
    return render(request, 'shops/category_dropdown_list_options.html', {'category': category})




@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def shopmenu(request,shop_url):
    menu=Shop.objects.get(shop_url=shop_url)
    icons = Icon.objects.filter(shop=menu)
    # content={
    #     "icons":icons,
    #     "shop":menu
    # }
   

    return render(request,'shops/shopmenu.html',{'shop':menu,'icons':icons})


# from user_agents import parse
from user_agents import parse
from natsort import natsorted


        


@user_passes_test(lambda u: u.is_superuser )
def viewuser(request):
  
    users = User.objects.all()

    user_info = []

    for user in users:
        user_permissions = user.get_all_permissions()
        user_info.append({'user': user, 'permissions': user_permissions})

    return render(request, 'users/viewuser.html', {'user_info': user_info})


@user_passes_test(lambda u: u.is_superuser )
def addusers(request):
    permissions=Permission.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        is_staff = request.POST.get('is_staff', False)
        selected_permissions = request.POST.getlist('permissions')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('addusers')

        if len(password1) < 1:
            messages.error(request, 'Password must be at least 8 characters long')
            return redirect('addusers')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is not available')
            return redirect('addusers')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered')
            return redirect('addusers')

        user = User.objects.create_user(username=username, email=email, password=password1)

        user.user_permissions.set(selected_permissions)

        if is_staff == 'on':
            user.is_staff = True
            user.save()

        messages.success(request, 'User added successfully')
        return redirect('viewuser')

    else:
        return render(request, 'users/adduser.html',{'permissions':permissions})
    



from .forms import UserForm
def editusers(request, pk):
    user = get_object_or_404(User, id=pk)
    permissions = Permission.objects.all()

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        selected_permissions = request.POST.getlist('permissions')

        if form.is_valid():
            form.save()
            user.user_permissions.set(selected_permissions)

            messages.success(request, 'User updated successfully')
            return redirect('viewuser')
        else:
            messages.error(request, 'Error updating user. Please correct the form.')
            return redirect('editusers')

    else:
        form = UserForm(instance=user)
        return render(request, 'users/edituser.html', {'form': form, 'permissions': permissions, 'user': user})
        















from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import Shop,Icon
from .serializers import ShopTypeSerializer,ShopSerializer

class ShoptypeList(generics.ListCreateAPIView):
    serializer_class=ShopTypeSerializer
    queryset=ShopType.objects.all()


class ShoptypeDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=ShopTypeSerializer
    queryset=ShopType.objects.all() 


class ShopList(generics.ListCreateAPIView):
    serializer_class=ShopSerializer
    queryset=Icon.objects.all()




 
            
        



    
    







