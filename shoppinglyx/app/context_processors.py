from .models import *


def extracontext(request):
    cartitems = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        cartitems = cart.count()
    return {'cartitems': cartitems}
