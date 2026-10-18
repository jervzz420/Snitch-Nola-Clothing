from pyscript import document

# Product prices are demo prices for the school project.
PRODUCT_PRICES = {
    "Graphic T-shirt": 450,
    "Casual Top": 399,
    "Hoodie": 799,
    "Shorts": 349,
}

active_filter = "all"


def peso(amount):
    """Format a number as Philippine pesos."""
    return "₱" + format(amount, ",.0f")


def get_selected_product():
    return document.getElementById("product").value


def get_quantity():
    quantity_input = document.getElementById("quantity")
    try:
        quantity = int(quantity_input.value)
    except (TypeError, ValueError):
        quantity = 1

    quantity = max(1, min(20, quantity))
    quantity_input.value = str(quantity)
    return quantity


def update_total(event=None):
    """Update the price when product or quantity changes."""
    product = get_selected_product()
    quantity = get_quantity()
    unit_price = PRODUCT_PRICES.get(product, 450)
    total = unit_price * quantity

    document.getElementById("unit-price").textContent = peso(unit_price)
    document.getElementById("quantity-display").textContent = str(quantity)
    document.getElementById("total-price").textContent = peso(total)


def show_toast(message):
    toast = document.getElementById("toast")
    toast.textContent = message
    toast.classList.add("show")

    # Remove the visual notification after a short delay using a browser timer.
    from js import setTimeout
    setTimeout(lambda: toast.classList.remove("show"), 2200)


def select_product(event):
    """A product-card button selects the matching item in the order form."""
    product_name = event.currentTarget.getAttribute("data-select-product")
    product_select = document.getElementById("product")
    product_select.value = product_name
    update_total()
    document.getElementById("order").scrollIntoView({"behavior": "smooth"})
    show_toast(product_name + " selected. Finish your order details below.")


def change_quantity(amount):
    quantity_input = document.getElementById("quantity")
    try:
        current = int(quantity_input.value)
    except (TypeError, ValueError):
        current = 1
    quantity_input.value = str(max(1, min(20, current + amount)))
    update_total()


def create_order_summary(event):
    """Validate the form and display a local demo order summary."""
    event.preventDefault()

    name = document.getElementById("customer-name").value.strip()
    if not name:
        document.getElementById("customer-name").focus()
        show_toast("Please enter your name first.")
        return

    product = get_selected_product()
    size = document.getElementById("size").value
    color = document.getElementById("color").value
    quantity = get_quantity()
    total = PRODUCT_PRICES.get(product, 450) * quantity

    result = document.getElementById("order-result")
    result.hidden = False
    result.textContent = (
        "ORDER SUMMARY — DEMO ONLY\\n"
        "Customer: " + name + "\\n"
        "Product: " + product + "\\n"
        "Size: " + size + "  |  Color: " + color + "\\n"
        "Quantity: " + str(quantity) + "\\n"
        "Estimated total: " + peso(total) + "\\n\\n"
        "This is a sample summary only. No order or payment has been sent."
    )
    result.scrollIntoView({"behavior": "smooth", "block": "nearest"})


def search_products(event=None):
    query = document.getElementById("product-search").value.strip().lower()
    visible_count = 0

    for card in document.querySelectorAll(".product-card"):
        name = card.getAttribute("data-name").lower()
        category = card.getAttribute("data-category")
        matches_query = query in name
        matches_filter = active_filter == "all" or category == active_filter
        visible = matches_query and matches_filter
        card.style.display = "block" if visible else "none"
        if visible:
            visible_count += 1

    grid = document.getElementById("product-grid")
    old_message = document.getElementById("empty-results")
    if old_message:
        old_message.remove()

    if visible_count == 0:
        message = document.createElement("p")
        message.id = "empty-results"
        message.className = "empty-results"
        message.textContent = "No products found. Try another search or choose All items."
        grid.appendChild(message)


def filter_products(event):
    global active_filter
    active_filter = event.currentTarget.getAttribute("data-filter")

    for button in document.querySelectorAll(".filter-button"):
        button.classList.remove("active")
    event.currentTarget.classList.add("active")
    search_products()


def toggle_menu(event=None):
    nav = document.getElementById("main-nav")
    button = document.getElementById("menu-toggle")
    is_open = nav.classList.toggle("open")
    button.setAttribute("aria-expanded", "true" if is_open else "false")


def update_video_overlay(event=None):
    video = document.getElementById("promo-video")
    overlay = document.getElementById("video-placeholder")
    # Hide the poster overlay after the local MP4 can be loaded.
    if video.readyState >= 2:
        overlay.style.display = "none"


# Register event handlers only when their elements exist on the current page.
def bind(element_id, event_name, callback):
    element = document.getElementById(element_id)
    if element:
        element.addEventListener(event_name, callback)

bind("product", "change", update_total)
bind("quantity", "input", update_total)
bind("qty-minus", "click", lambda event: change_quantity(-1))
bind("qty-plus", "click", lambda event: change_quantity(1))
bind("order-form", "submit", create_order_summary)
bind("product-search", "input", search_products)
bind("menu-toggle", "click", toggle_menu)
bind("promo-video", "loadeddata", update_video_overlay)

for button in document.querySelectorAll(".add-button"):
    button.addEventListener("click", select_product)

for button in document.querySelectorAll(".filter-button"):
    button.addEventListener("click", filter_products)

if document.getElementById("product"):
    update_total()
