from django import template
from core.models import CartOrderProduct, Product

register = template.Library()


@register.filter
def get_cart_quantity(p_id, user):
    try:
        cart_product = CartOrderProduct.objects.filter(
            cart__user=user, product=Product.objects.get(id=p_id))
        if cart_product.exists():
            quanti = cart_product.first().qty
            return quanti
        else:
            return 0
    except CartOrderProduct.DoesNotExist:
        return 0
