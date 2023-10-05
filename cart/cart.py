from _decimal import Decimal
from django.core import serializers
from shop.models import Product


class Cart(object):

    def __init__(self,request,userid):
        self.userid=str(userid)
        self.session=request.session
        cart=self.session.get(self.userid)

        if not cart:
            cart=self.session[self.userid]={}
        self.cart=cart


    def add(self,product,quantity=1):
        product_id=str(product.id)
        if product_id not in self.cart:
            self.cart[product_id]={'quantity':0, 'price':str(product.price)}
        self.cart[product_id]['quantity']+=quantity
        self.save()


    def save(self):
        self.session.modified=True


    def remove(self,product):
        product_id=str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def __iter__(self):
        product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)
        cart=self.cart.copy()
        for product in products:
            cart[str(product.id)]['product']=product

        for item in cart.values():
            item['price']=Decimal(item['price'])
            item['total_price']=item['price']*item['quantity']
            yield item


    def for_ordered_item(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product_name'] = product.name
            cart[str(product.id)]['product_image'] = product.image.url
            cart[str(product.id)]['product_available'] = product.available
            cart[str(product.id)]['product_category'] = product.category.name
            cart[str(product.id)]['total_price'] = product.price*cart[str(product.id)]['quantity']

        return cart


    def get_total_price(self):
        return sum(Decimal(item['price']*item['quantity'])for item in self.cart.values())

    def clear(self):
        del self.session[self.userid]
        self.save()