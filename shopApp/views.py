from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from shopApp.cart import Cart
from shopApp.forms import BestellingForm, KlantForm, ProductPlusForm
from shopApp.models import Product, Categorie, BestellingProduct


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
        'plus_form': ProductPlusForm(initial={'aantal': 1})
    })


def bestelling(request):
    if request.method == 'POST':
        form = BestellingForm(request.POST)

        if form.is_valid():
            # Producten in mandje + mandje opslaan
            nieuwe_bestelling = form.save()

            # Bestelling producten maken en toevoegen
            for prod_id, item in request.session['cart'].items():
                product = get_object_or_404(Product, id=int(prod_id))
                bestel_prod = BestellingProduct(product=product, bestelling=nieuwe_bestelling, aantal=item['aantal'])
                bestel_prod.save()

            # Mandje resetten
            cart = Cart(request)
            cart.clear()

            # Melding neerzetten
            messages.success(request, f'Bestelling is gemaakt, er wordt een bevestiging gestuurd naar {nieuwe_bestelling.klant.email}')

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

            messages.success(request, f"Klant '{nieuw_klant.naam}' toegevoegd aan het systeem.")
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
    aantal = 1

    if request.method == 'POST':
        form = ProductPlusForm(request.POST)

        if form.is_valid():
            aantal = form.cleaned_data['aantal']
        else:
            messages.error(request, "Er is iets mis gegaan met het toevoegen aan winkelwagen.")
            return redirect('home')

    cart = Cart(request)
    product = get_object_or_404(Product, id=prod_id)
    cart.add(product=product, aantal=aantal)

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
