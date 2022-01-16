
class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session

        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def add(self, product, aantal=1):
        id = product.id

        if str(id) not in self.cart.keys():

            self.cart[id] = {
                'product_id': id,
                'naam': product.naam,
                'aantal': aantal,
                'hoeveelheid': product.hoeveelheid,
                'eenheid': product.eenheid,
                'foto_url': product.foto.url
            }
        else:
            for key, value in self.cart.items():
                if key == str(id):
                    self.cart[key]['aantal'] += aantal
                    break

        self.save()

    def decrement(self, product):
        for key, value in self.cart.items():
            if key == str(product.id):
                if value['aantal'] > 1:
                    self.cart[key]['aantal'] -= 1
                    self.save()
                    break

    def remove(self, product):
        prod_id = str(product.id)
        if prod_id in self.cart.keys():
            del self.cart[prod_id]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True


