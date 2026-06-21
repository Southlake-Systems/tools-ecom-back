from product.models.product import Product
from .services.brand_service import get_brand_list
from brands.models import Brand
from .services.product_service import get_products_by_brand
from .utils import send_whatsapp_message, send_interactive_buttons
from .utils import send_image_message
def send_main_menu(phone):
    text = """
👋 Welcome to Yessare

Choose an option:

1️⃣ View Brands
2️⃣ Explore Products
3️⃣ Search Products
4️⃣ Visit Website
5️⃣ Contact Support

Reply with a number.
"""

    send_whatsapp_message(phone, text)

    return True

def show_brands(phone):
    brands = get_brand_list()

    text = "🏷 Available Brands\n\n"

    for brand in brands:
        text += f"• {brand.name}\n"

    text += "\nReply with brand name."

    send_whatsapp_message(
        phone,
        text
    )

    return True



def handle_message(phone, message):
    message = message.lower().strip()

    # Menu
    if message in ["hi", "hello", "menu"]:
        send_interactive_buttons(phone)
        return True

    # Brands list
    if message in ["brands", "1"]:
        show_brands(phone)
        return True
    if message == "products":
        send_whatsapp_message(
            phone,
            "🔍 Send a product name to search.")
        return True
    if message == "website":
        send_whatsapp_message( phone, "🌐 https://yessaretools.com" ) 
        return True
    
    # BRAND PRODUCTS SECTION ← PUT IT HERE
    brand = Brand.objects.filter(
        name__iexact=message
    ).first()

    if brand:

        products = Product.objects.filter(
            brand=brand
        )[:10]

        text = f"🔥 {brand.name} Products\n\n"

        for product in products:
            text += f"• {product.name}\n"

        text += "\nReply with product name to view details."

        send_whatsapp_message(
            phone,
            text
        )

        return True
    
    # Product search
    # Product search
    products = Product.objects.filter(
        name__icontains=message
    )[:5]

    if products.exists():

        exact_product = Product.objects.filter(
            name__iexact=message
        ).first()

        if exact_product:

            image_url = None

            product_image = exact_product.images.first()

            if product_image:

                variant = product_image.variants.filter(
                    quality="MID"
                ).first()

                if variant and variant.file:
                    image_url = (
    variant.jpg_file.url
    if variant.jpg_file
    else variant.file.url
)

                elif product_image.original:
                    image_url = product_image.original.url

            print("IMAGE URL:", image_url)

            caption = f"""🔥 {exact_product.name}\n💰 ₹{exact_product.price.selling_price}\n🛡 Warranty: {exact_product.warranty}\n🔗 https://yessaretools.com/product/{exact_product.id}
"""

            if image_url:
                send_image_message(
                    phone,
                    image_url,
                    caption
                )
            else:
                send_whatsapp_message(
                    phone,
                    caption
                )

            return True

        # Multiple search results
        text = "🔍 Search Results\n\n"

        for product in products:
            text += f"• {product.name}\n"

        text += "\nReply with the exact product name."

        send_whatsapp_message(
            phone,
            text
        )

        return True