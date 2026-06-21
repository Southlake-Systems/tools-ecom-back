

def handle_message(phone, message):
    message = message.lower().strip()

    if message == "hi":
        return welcome(phone)

    if message == "brands":
        return show_brands(phone)

    if message.startswith("search "):
        return search_product(phone, message[7:])