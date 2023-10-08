from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, User
from cart.forms import CartCountForm

from cart.cart import Cart


def product_list(request, category_slug=None):
    category=None
    categories=Category.objects.all()
    products=Product.objects.filter(available=True)
    if category_slug:
        category=get_object_or_404(Category,slug=category_slug)
        products=products.filter(category=category)
    context={
        'category':category,
        'categories':categories,
        'products':products
    }
    return render(request,'shop/product_list.html',context)


def product_detail(request,id,slug):
    product=get_object_or_404(Product,id=id,slug=slug,available=True)
    cart_add_form=CartCountForm()
    context={
        'product':product,
        'form':cart_add_form
    }
    return render(request,'shop/product_detail.html',context)


def login_user(request):
    if request.method=="POST":
        email=request.POST["email"]
        password=request.POST["password"]
        print("email: ",email,"   password: ",password)
        user=authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('shop:product_list')
        else:
            messages.success(request,"없는 사람입니다. 다시 로그인 하세욥!")
            return redirect('shop:login_user')
    else:
        return render(request,'authenticate/login.html',{})



def logout_user(request):
    logout(request)
    return redirect('shop:product_list')


def sign_up(request):
    if request.method=="POST":
        user=User()
        user.name=request.POST["name"]
        user.email=request.POST["email"]
        user.phone=request.POST["phone"]
        temp=request.POST["address1"]+ " " +request.POST["address2"]
        user.address=temp
        user.password=request.POST["password"]
        user.set_password(user.password)
        user.save()
        return redirect('shop:login_user')
    else:
        return render(request,'authenticate/sign_up.html',{})

def profile_edit(request):
    user=User.objects.get(id=request.user.id)
    if request.method=="POST":
        name=request.POST["name"]
        phone=request.POST["phone"]
        email=request.POST["email"]
        User.objects.filter(id=request.user.id).update(name=name,phone=phone,email=email)
        messages.success(request,"정보를 수정하였습니다")
        return redirect('shop:profile_edit')
    else:
        context={
            'name':user.name,
            'phone':user.phone,
            'email':user.email
        }
        return render(request,'authenticate/profile_edit.html',context)


