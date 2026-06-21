from brands.models import Brand


def get_brand_list():
    return Brand.objects.all()[:20]