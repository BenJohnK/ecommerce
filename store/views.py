from django.shortcuts import render
from . models import *
from django.http import JsonResponse,HttpResponse
import json
import datetime
from .utils import cookieCart

# Create your views here.

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        cartitems=order.get_cart_items
    else:
        cookieData=cookieCart(request)  # for non logged-in user..
        cartitems=cookieData['cartitems']
    products=Product.objects.all()
    return render(request,"store/store.html",{'products':products,'cartitems':cartitems})

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartitems=order.get_cart_items
    else:
        cookieData=cookieCart(request)
        items=cookieData['items']
        order=cookieData['order']
        cartitems=cookieData['cartitems']
        
    return render(request,"store/cart.html",{'items':items,'order':order,'cartitems':cartitems})

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartitems = order.get_cart_items
        shipping= order.get_is_digital 
    else:
        cookieData=cookieCart(request)
        items=cookieData['items']
        order=cookieData['order']
        cartitems=cookieData['cartitems']
        shipping=cookieData['shipping']
    return render(request,"store/checkout.html",{'items':items,'order':order,'cartitems':cartitems,'shipping':shipping})

def updateitem(request):
    data=json.loads(request.body)
    productid=data["productid"]
    action=data["action"]
    

    customer = request.user.customer
    product=Product.objects.get(id=productid)
    print(product)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == "add":
        orderitem.quantity+=1
    elif action == "remove":
        orderitem.quantity-=1
    
    orderitem.save()
    
    if orderitem.quantity<=0:
        orderitem.delete()
    


    return JsonResponse("Item was added",safe=False)
    
def processorder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        
        order.transaction_id=transaction_id
        # print(total)
        # print(data['userdetails']['total'])

    else:
        print("User is not logged in")
        name=data['userdetails']['name']
        email=data['userdetails']['email']
        customer,created = Customer.objects.get_or_create(email=email)
        customer.name=name
        customer.save()
        order=Order.objects.create(
            customer=customer,
            complete=False,
            transaction_id=transaction_id
        )
        cartdata=json.loads(request.COOKIES['cart'])
        for i in cartdata:
            product=Product.objects.get(id=i)
            item=OrderItem.objects.create(
                product=product,
                order=order,
                quantity=cartdata[i]['quantity']
            )
    total=float(order.get_cart_total)
    if total == float(data['userdetails']['total']):
            order.complete=True
    order.save()
    if order.get_is_digital==True:
            ShippingAddress.objects.create(
                 customer=customer,
                 order=order,
                 address=data['shippingdetails']['address'],
                 city=data['shippingdetails']['city'],
                 state=data['shippingdetails']['state'],
                 zipcode=data['shippingdetails']['zipcode'],
                 country=data['shippingdetails']['country'] ,
            )
    return JsonResponse("order processed",safe=False)

def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        cartitems=order.get_cart_items
    else:
        cartitems=0  # for non logged-in user...needs to change user when enabling guest user
    products=Product.objects.all()
    return render(request,"store/home.html",{'cartitems':cartitems,'products':products})