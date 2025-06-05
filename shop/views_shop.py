from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from collections import defaultdict
from django.db import transaction
from .models import Product, Order, Customer
import random 
# ----------------- Home Page -----------------
def shop_home(request: HttpRequest):
    logout(request)  # Logs out user on shop home load

    categorized_products = defaultdict(list)
    for product in Product.objects.filter(stock__gt=0).select_related('category'):
        category = product.category.name if product.category else "Uncategorized"
        categorized_products[category].append(product)

    cart = request.session.get('cart', {})
    cart_quantities = {int(k): v for k, v in cart.items()}

    return render(request, "shop/index.html", {
        "categorized_products": dict(categorized_products),
        "cart_quantities": cart_quantities,
    })

# ----------------- Static Pages -----------------
def about(request):
    # Get all products with images
    products_with_images = list(Product.objects.filter(image__isnull=False))
    # Pick 3 random products (if fewer than 3, just all of them)
    random_products = random.sample(products_with_images, min(len(products_with_images), 3))
    
    return render(request, 'shop/about.html', {'products': random_products})

def contact(request: HttpRequest):
    return render(request, "shop/contact.html")

# ----------------- Products View -----------------
def product(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {})
    cart_quantities = {int(k): v for k, v in cart.items()}

    # Group by category
    categorized_products = {}
    for product in products:
        category = product.category if product.category else "Uncategorized"
        categorized_products.setdefault(category, []).append(product)

    context = {
        'categorized_products': categorized_products,
        'cart_quantities': cart_quantities
    }
    return render(request, 'shop/product.html', context)

# ----------------- Order Tracking -----------------
def track_order(request):
    order = None
    error = None

    if request.method == "POST":
        tracking_id = request.POST.get("tracking_id", "").strip()
        if tracking_id:
            try:
                order = Order.objects.get(tracking_id=tracking_id)
            except Order.DoesNotExist:
                error = "Order not found with that Tracking ID."
        else:
            error = "Please enter a Tracking ID."

    return render(request, "shop/track_order.html", {
        "order": order,
        "error": error,
    })

# ----------------- Search View -----------------
def search(request):
    query = request.GET.get('query', '').strip()
    products = Product.objects.filter(name__icontains=query) if query else []

    cart = request.session.get('cart', {})
    cart_quantities = {int(k): v for k, v in cart.items()}

    context = {
        'query': query,
        'products': products,
        'cart_quantities': cart_quantities
    }
    return render(request, 'shop/search.html', context)

# ----------------- Cart View -----------------
def cart(request: HttpRequest):
    cart = request.session.get('cart', {})

    add_id = request.GET.get('add')
    if add_id:
        product = Product.objects.filter(id=add_id, stock__gt=0).first()
        if product:
            cart[add_id] = cart.get(add_id, 0) + 1
            request.session['cart'] = cart
            messages.success(request, f"Added {product.name} to cart.")
        else:
            messages.error(request, "Product not found or out of stock.")
        return redirect('shop_cart')

    remove_id = request.GET.get('remove')
    if remove_id and remove_id in cart:
        cart[remove_id] -= 1
        if cart[remove_id] <= 0:
            del cart[remove_id]
        request.session['cart'] = cart
        messages.info(request, "Updated your cart.")
        return redirect('shop_cart')

    products_in_cart = []
    total_price = 0
    for pid, quantity in cart.items():
        try:
            pid_int = int(pid)
            product = Product.objects.filter(id=pid_int, stock__gt=0).first()
            if product:
                subtotal = product.price * quantity
                total_price += subtotal
                products_in_cart.append({
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'quantity': quantity,
                    'subtotal': subtotal,
                    'image': product.image.url if product.image else None,
                })
        except ValueError:
            continue

    return render(request, 'shop/cart.html', {
        'cart_items': products_in_cart,
        'total': total_price,
    })

# ----------------- Checkout View -----------------
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty!")
        return redirect('shop_cart')

    if request.method == "POST":
        customer_name = request.POST.get("full_name", "").strip()
        customer_email = request.POST.get("email", "").strip()
        customer_address = request.POST.get("address", "").strip()
        payment_method = request.POST.get("payment_method", "").strip()

        if not (customer_name and customer_email and customer_address and payment_method):
            messages.error(request, "Please fill in all required fields.")
            return redirect('shop_checkout')

        customer, created = Customer.objects.get_or_create(
            email=customer_email,
            defaults={'full_name': customer_name, 'address': customer_address}
        )
        if not created:
            customer.full_name = customer_name
            customer.address = customer_address
            customer.save()

        order_items = []
        total_price = 0
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, pk=product_id)
            qty = int(quantity)
            subtotal = product.price * qty
            total_price += subtotal
            order_items.append({
                'product_id': product.id,
                'name': product.name,
                'quantity': qty,
                'unit_price': float(product.price),
                'subtotal': float(subtotal),
            })

        with transaction.atomic():
            order = Order.objects.create(
                customer=customer,
                items=order_items,
                total_price=total_price,
                payment_method=payment_method,
            )

        # Clear cart after order creation
        request.session['cart'] = {}
        request.session.modified = True

        return render(request, 'shop/checkout.html', {
            'order_success': {
                'order_id': order.tracking_id,
                'full_name': customer.full_name,
                'email': customer.email,
                'address': customer.address,
                'total_price': total_price,
                'payment_method': payment_method,
            }
        })

    # GET request - show checkout form with cart summary
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        cart_items.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'image': product.image.url if product.image else None,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal

    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })

# ----------------- Bulk Add to Cart -----------------
@require_POST
def add_multiple_to_cart(request):
    cart = request.session.get('cart', {})

    for key, value in request.POST.items():
        if key.startswith('quantity_'):
            try:
                product_id = key.split('_')[1]
                qty = int(value)
                if qty > 0:
                    cart[product_id] = qty
                elif product_id in cart:
                    del cart[product_id]
            except (ValueError, IndexError):
                continue

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('shop_cart')
