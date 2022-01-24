
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

    def add(self, product, extra_optie="", aantal=1):
        the_key = str(product.id) + '_' + extra_optie

        if the_key in self.cart.keys():
            for key, value in self.cart.items():
                if key == the_key:
                    self.cart[key]['aantal'] += aantal
                    self.save()
                    return

        if aantal < product.min_aantal:
            aantal = product.min_aantal

        self.cart[the_key] = {
            'product_id': product.id,
            'naam': product.naam,
            'aantal': aantal,
            'extra_optie': extra_optie
        }

        self.save()

    def decrement(self, product, extra_optie):
        the_key = str(product.id) + '_' + extra_optie
        for key, value in self.cart.items():
            if key == the_key:
                if value['aantal'] > product.min_aantal:
                    self.cart[the_key]['aantal'] -= 1
                    self.save()

                break

    def remove(self, product, extra_optie):
        the_key = str(product.id) + '_' + extra_optie
        if the_key in self.cart.keys():
            del self.cart[the_key]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True


