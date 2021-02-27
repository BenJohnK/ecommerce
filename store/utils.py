import json
from . models import *

def cookieCart(request):
    items=[]
    cartitems=0
    order={'get_cart_items':0,'get_cart_total':0}
    try:
        data=json.loads(request.COOKIES['cart'])
    except:
        data={}
    total=order['get_cart_total']
    shipping=False
    for k in data:
        try:
             order['get_cart_items']+=data[k]['quantity']
             product=Product.objects.get(id=k)
             total+=product.price*data[k]['quantity']
             s={
                "product":{
                    "id":k,
                    "name":product.name,
                    "price":product.price,
                    "imageURL":product.imageURL
                },
                "quantity":data[k]['quantity'],
                "get_total":product.price*data[k]['quantity']
             }
             items.append(s)
             if product.digital==False:
                shipping =True
        except:
                pass
        cartitems=order['get_cart_items']
        order['get_cart_total']=total
    return {'items':items,'order':order,'cartitems':cartitems,'shipping':shipping}