from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .cart import Cart
from shop.models import Product,User,Order
from .forms import CartCountForm



@require_POST
def cart_add(request,product_id):
    if request.user.is_authenticated:
        userid=request.user.id
    else:
        return redirect('shop:login_user')
    cart=Cart(request,userid)
    product=get_object_or_404(Product,id=product_id)
    form=CartCountForm(request.POST)
    if form.is_valid():
        quantity=form.cleaned_data['quantity']
        cart.add(product,quantity)

    return redirect('cart:cart_detail')

def cart_detail(request):
    cart=Cart(request,request.user.id)
    obj = User.objects.get(id=request.user.id)
    if request.method=="POST":
        order=Order()
        order.user=request.user
        order.name = request.POST["name"]
        order.phone = request.POST["phone"]
        order.address = request.POST["address"]
        order.email = request.POST["email"]
        order.orderitem=cart.for_ordered_item()
        order.save()
        messages.success(request,"주문 성공 하였습니다!!!")
        cart.clear()
        return redirect('cart:order_success')
    else:
        return render(request,'cart/detail.html',{'cart':cart,'obj':obj})

def cart_remove(request,product_id):
    cart=Cart(request,request.user.id)
    product=get_object_or_404(Product,id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def order_success(request):
    order=Order.objects.filter(user_id=request.user.id).order_by('-created_at')

    return render(request,'cart/ordered.html',{'order':order})

