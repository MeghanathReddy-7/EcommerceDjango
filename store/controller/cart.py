from django.shortcuts import render,redirect
from django.contrib import messages
from django.http.response import JsonResponse
from store.models import Product,Cart
from django.contrib.auth.decorators import login_required
def addtocart(request):
    if request.method=='POST':
        #if user is logged in 
        if request.user.is_authenticated:
            prod_id =int( request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            #if such product exists
            if product_check:
                #if already user added it to cart
                if(Cart.objects.filter(user=request.user.id,product_id=prod_id)):
                    return JsonResponse({'status':"product already in cart"})
                else:
                    #get(product_qty ) is from ajax funcion in custom .js
                    productqty = int(request.POST.get('product_qty'))
                    #if we  have enough stock
                    if product_check.quantity >= productqty:
                        Cart.objects.create(user=request.user,product_id=prod_id,product_qty=productqty)
                        return JsonResponse({'status':"product added successfully"})
                    #if we dont have enough stock of the requested product 
                    else:
                        return JsonResponse({'status':"only"+str(product_check.quantity)+"quantity available"})
            else:
                return JsonResponse({'status':"no such product found"})
        else:
            return JsonResponse({'status':"login to continue"})
    return redirect('/')

@login_required(login_url='loginpage')
def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    context = {'cart':cart}
    return render(request,"store/cart.html",context)

def updatecart(request):
    if request.method=='POST':
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user,product_id=prod_id):
             prod_qty = int(request.POST.get('product_qty'))
             cart = Cart.objects.get(product_id=prod_id,user=request.user) 
             cart.product_qty = prod_qty
             cart.save()
             return JsonResponse({'status':"Updated successfully"})
             
    return redirect('/')

def deletecartitem(request):
    if request.method=='POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user,product_id = prod_id)):
            cartitem = Cart.objects.get(product_id=prod_id,user=request.user)
            cartitem.delete()
        return JsonResponse({'status':"Deleted Successfully"})
    return redirect('/')