from django.shortcuts import render, redirect, get_object_or_404

from shopApp.cart import Cart
from shopApp.forms import BestellingForm
from shopApp.models import Product, Categorie


# def home(request):
#     return render(request, 'shopApp/base.html', {
#         'categories': Categorie.objects.all()
#     })


def product_filter(request, cat="alles"):
    if cat == "alles":
        producten = Product.objects.all()
    else:
        producten = Product.objects.filter(categorie__naam__contains=cat)

    return render(request, 'shopApp/producten.html', {
        'categories': Categorie.objects.all(),
        'producten': producten,
        'filter': cat
    })


def bestelling(request):
    if request.method == 'POST':
        form = BestellingForm(request.POST)

        if form.is_valid():
            nieuwe_bestelling = form.save(commit=False)
            producten = [int(prod_id) for prod_id in request.session['cart'].keys()]

            nieuwe_bestelling.producten = producten
            nieuwe_bestelling.save()
            return redirect('home')
        else:
            return render(request, 'shopApp/bestellling.html', {
                'categories': Categorie.objects.all(),
                'form': form
            })

    elif not request.session.get('cart') or len(request.session['cart']) < 1:
        return redirect('home')
    else:
        return render(request, 'shopApp/bestellling.html', {
            'categories': Categorie.objects.all(),
            'form': BestellingForm()
        })


# ----- CART FUNCTIES --------------------------------------------------------------

def cart_view(request):
    return render(request, 'shopApp/cart.html', {
        'categories': Categorie.objects.all()
    })


def cart_add(request, prod_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=prod_id)
    cart.add(product=product)
    referer = request.headers['Referer'].split('/')
    return redirect('/filter/' + referer[len(referer) - 1])


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart')


def cart_item_increment(request, prod_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=prod_id)
    cart.add(product=product)
    return redirect('cart')


def cart_item_decrement(request, prod_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=prod_id)
    cart.decrement(product=product)
    return redirect('cart')


def cart_item_remove(request, prod_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=prod_id)
    cart.remove(product=product)
    return redirect('cart')
