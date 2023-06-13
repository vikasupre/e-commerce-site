from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse,JsonResponse

class productView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        context = {'topwears': topwears,
                   'bottomwears': bottomwears, 'mobiles': mobiles}
        return render(request, 'app/home.html', context)


class productDetailsView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_present_in_cart = False
        if request.user.is_authenticated:
            item_present_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product': product, 'item_exist_in_cart': item_present_in_cart})


# adding product to cart

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(pk=product_id)
    cart = Cart(user=user, product=product)
    cart.save()
    return redirect('/cart')


def show_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        amount = 0.0
        shipping = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        if cart:
            for p in cart:
                tempamount = (p.quantity*p.product.discount_price)
                amount += tempamount
                totalamount = amount+shipping
            return render(request, 'app/addtocart.html', {'cart': cart, 'totalamount': totalamount, 'amount': amount, 'shipping': shipping})
        else:
            return render(request, 'app/emptycart.html')
    else:
        return redirect('/accounts/login')

# plus item quantity


def plusCart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping = 70
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity*p.product.discount_price)
            amount += tempamount
            total_amount = amount+shipping
        mydata = {
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': total_amount
        }
        return JsonResponse(mydata)

# minus ite quantity


def minusCart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = p.quantity*p.product.discount_price
            amount += tempamount
            total_amount = amount+shipping
        mydata = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': total_amount
        }
        return JsonResponse(mydata)

# remove item from cart


def removeItem(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = p.quantity*p.product.discount_price
            amount += tempamount
            total_amount = amount+shipping
        mydata = {
            'amount': amount,
            'totalamount': total_amount
        }
        return JsonResponse(mydata)

# Placing order


@login_required
def paymentDone(request):
    user = request.user
    custid = request.GET['custid']
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for p in cart:
        OrederPlaced(user=user, customer=customer,
                     product=p.product, quantity=p.quantity).save()
        p.delete()
    return redirect('/orders')


def buyItem(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(pk=product_id)
    cart = Cart(user=user, product=product)
    addrs = Customer.objects.filter(user=request.user)
    amount = product.discount_price
    shipping = 70.0
    total_amount = 0.0
    total_amount = amount+shipping
    context = {'totalamount': total_amount, 'amount': amount,
               'shipping': shipping, 'product': product, 'addrs': addrs}

    return render(request, 'app/buynow.html', context)


class ProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user  # current user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            phone = form.cleaned_data['phone']
            reg = Customer(user=usr, name=name, locality=locality,
                           city=city, state=state, pincode=pincode, phone=phone)
            reg.save()
            messages.success(
                request, 'Congratilations!! Profile Updated Successfully')
            form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


def address(request):
    adds = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'adds': adds, 'active': 'btn-primary'})


# placed orders

@login_required
def orders(request):
    op = OrederPlaced.objects.filter(user=request.user)

    return render(request, 'app/orders.html', {'orders': op})


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'redmi' or data == 'oppo' or data == 'vivo':
        mobiles = Product.objects.filter(category='M', brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(
            category='M', discount_price__lte=15000)
    elif data == 'above':
        mobiles = Product.objects.filter(
            category='M', discount_price__gte=15000)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})


def topwear(request, data=None):
    if data == None:
        tw = Product.objects.filter(category='TW')
    elif data == 'below':
        tw = Product.objects.filter(
            category='TW', discount_price__lte=500)
    elif data == 'above':
        tw = Product.objects.filter(
            category='TW', discount_price__gte=500)
    return render(request, 'app/topwear.html', {'topwear': tw})


def bottomwear(request, data=None):
    if data == None:
        bw = Product.objects.filter(category='BW')
    elif data == 'below':
        bw = Product.objects.filter(
            category='BW', discount_price__lte=500)
    elif data == 'above':
        bw = Product.objects.filter(
            category='BW', discount_price__gte=500)
    return render(request, 'app/bottomwear.html', {'bottomwear': bw})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerUserCreationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Congratulations! You have registered successfully')
            form.save()
            return HttpResponse('user created successfully')
        # return render(request, 'app/customerregistration.html', {'form': form})


@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user)
    addrs = Customer.objects.filter(user=request.user)
    cart_product = [p for p in Cart.objects.all() if p.user ==
                    request.user]
    amount = 0.0
    shipping = 70.0
    totalamount = 0.0
    if cart:
        for p in cart:
            tempamount = p.quantity*p.product.discount_price
            amount += tempamount
            totalamount = amount+shipping
        context = {'total': totalamount, 'addrs': addrs,
                   'cart': cart, 'total': totalamount}
        return render(request, 'app/checkout.html', context)
    else:
        return render(request, 'app/emptycart.html')


def search(request):
    if request.method == 'GET':
        prodname = request.GET.get('search')
        if len(prodname) == 0:
            prod = Product.objects.none()
            print(prod)
        elif prodname != None:
            prod = Product.objects.filter(title__icontains=prodname)
    return render(request, 'app/searchitems.html', {'prod': prod, 'prodname': prodname})
