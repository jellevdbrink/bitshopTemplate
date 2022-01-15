from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from shopApp.cart import Cart
from shopApp.forms import BestellingForm, KlantForm
from shopApp.models import Product, Categorie


# def home(request):
#     return render(request, 'shopApp/base.html', {
#         'categories': Categorie.objects.all()
#     })


def product_filter(request, cat="alles"):
    return render(request, 'shopApp/producten.html', {
        'categories': Categorie.objects.all(),
        'header_text': 'Alle producten' if cat == "alles" else 'Categorie: ' + cat,
        'header_colour': 'teal',
        'producten': Product.objects.all() if cat == "alles" else Product.objects.filter(categorie__naam__contains=cat),
    })


def bestelling(request):
    if request.method == 'POST':
        form = BestellingForm(request.POST)

        if form.is_valid():
            # Producten in mandje + mandje opslaan
            nieuwe_bestelling = form.save(commit=False)
            producten = [int(prod_id) for prod_id in request.session['cart'].keys()]

            nieuwe_bestelling.producten = producten
            nieuwe_bestelling.save()

            # Mandje resetten
            cart = Cart(request)
            cart.clear()

            # Melding neerzetten
            messages.success(request, 'Bestelling is gemaakt, er wordt een mail gestuurd naar ' + nieuwe_bestelling.klant.email)

            return redirect('home')

    elif not request.session.get('cart') or len(request.session['cart']) < 1:
        return redirect('home')
    else:
        form = BestellingForm()

    return render(request, 'shopApp/bestelling.html', {
        'categories': Categorie.objects.all(),
        'header_text': 'Bestelling',
        'header_colour': 'amber',
        'form': form
    })


def nieuwe_klant(request):
    if request.method == 'POST':
        form = KlantForm(request.POST)

        if form.is_valid():
            nieuw_klant = form.save()

            messages.success(request, "Klant '" + nieuw_klant.naam + "' toegevoegd aan het systeem.")
            return redirect('bestelling')
    else:
        form = KlantForm()

    return render(request, 'shopApp/nieuwe_klant.html', {
        'categories': Categorie.objects.all(),
        'header_text': 'Nieuwe klant',
        'header_colour': 'lime',
        'form': form
    })


# ----- CART FUNCTIES --------------------------------------------------------------

def cart_view(request):
    if request.session.get('cart'):
        producten_id_list = [int(key) for key in request.session.get('cart').keys()]
        producten = Product.objects.filter(id__in=producten_id_list)
    else:
        producten = []

    return render(request, 'shopApp/cart.html', {
        'categories': Categorie.objects.all(),
        'header_text': 'Winkelwagen',
        'header_colour': 'purple',
        'producten_text': 'product' if len(producten) == 1 else 'producten',
        'producten': producten
    })


def cart_add(request, prod_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=prod_id)
    cart.add(product=product)

    referer = request.headers['Referer'].split('/')
    if not referer[len(referer) - 1]:
        referer.append('alles')

    return redirect('/filter/' + referer[len(referer) - 1] + '#' + str(prod_id))


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
