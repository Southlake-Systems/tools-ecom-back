from product.models import Product


def get_products_by_brand(name):
    return Product.objects.filter(
        brand__name__iexact=name
    )[:10]