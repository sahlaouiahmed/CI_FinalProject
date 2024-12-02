from django.shortcuts import render, get_object_or_404 ,redirect
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem
from django.contrib import messages


def product_list(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    category = request.GET.get('category', 'all')
    if category != 'all':
        products = products.filter(category__iexact=category)
    context = {
        'products': products,
        'category': category,
        'query': query,
    }
    return render(request, 'store/product_list.html', context)




from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]  # Fetch related products from the same category, exclude the current product, limit to 4
    return render(request, 'store/product_detail.html', {'product': product, 'related_products': related_products})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock > 0:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        product.stock -= 1
        product.save()
        messages.success(request, f'{product.name} has been added to your cart successfully!')
    else:
        messages.error(request, 'Sorry, this product is out of stock.')
    return redirect('product_list')



@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'store/cart.html', {'cart_items': cart_items})

@login_required
def update_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if quantity > cart_item.product.stock:
            messages.error(request, f"Only {cart_item.product.stock} items available in stock.")
        elif quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully.')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
    return redirect('cart_view')


@login_required
def delete_cart_item(request, item_id):
    cart_item = CartItem.objects.get(id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')


##############
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import CartItem, Order
from .forms import ShippingForm

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            # Extract form data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip_code']

            # Calculate total amount in cents
            amount = int(sum(item.quantity * item.product.price for item in cart_items) * 100)

            # Create Stripe Checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': amount,
                        'product_data': {
                            'name': 'Order from Kitchen Garden'
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('payment_success')) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
            )
            request.session['checkout_data'] = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'address': address,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'amount': amount / 100  # Storing in dollars for display
            }
            return redirect(session.url)
    else:
        form = ShippingForm()

    context = {
        'cart_items': cart_items,
        'form': form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'store/checkout.html', context)

@login_required
def payment_success(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
        return redirect('checkout')  # If no session_id, redirect back to checkout

    # Verify the session with Stripe
    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status != 'paid':
        return redirect('checkout')  # If payment not successful, redirect back to checkout

    # Retrieve the checkout data stored in the session
    checkout_data = request.session.pop('checkout_data', {})
    if not checkout_data:
        return redirect('checkout')  # No checkout data means something went wrong

    # Retrieve cart items
    cart_items = CartItem.objects.filter(user=request.user)

    # Prepare items as a list of dictionaries with prices as strings
    items = []
    for item in cart_items:
        items.append({
            'product_id': item.product.id,
            'name': item.product.name,
            'price': str(item.product.price),  # Convert Decimal to string
            'quantity': item.quantity
        })

    # Create order in the database
    order = Order.objects.create(
        user=request.user,
        first_name=checkout_data['first_name'],
        last_name=checkout_data['last_name'],
        email=checkout_data['email'],
        address=checkout_data['address'],
        city=checkout_data['city'],
        state=checkout_data['state'],
        zip_code=checkout_data['zip_code'],
        items=items,
        total_amount=checkout_data['amount']  # Store the total amount
    )

    # Prepare the email content
    items_list = '\n'.join([f"{item['quantity']} x {item['name']} - ${item['price']}" for item in items])
    email_subject = 'Your Kitchen Garden Order Confirmation'
    email_body = (
        f"Dear {checkout_data['first_name']},\n\n"
        f"Thank you for your order from Kitchen Garden! We're excited to help you grow your garden with our products.\n\n"
        f"Here are the details of your order:\n\n"
        f"Order Number: {order.id}\n"
        f"Total Amount: ${checkout_data['amount']}\n\n"
        f"Shipping Address:\n"
        f"{checkout_data['first_name']} {checkout_data['last_name']}\n"
        f"{checkout_data['address']}\n"
        f"{checkout_data['city']}, {checkout_data['state']} {checkout_data['zip_code']}\n\n"
        f"Order Items:\n"
        f"{items_list}\n\n"
        f"If you have any questions or need further assistance, feel free to contact us.\n\n"
        f"Happy gardening!\n\n"
        f"Best regards,\n"
        f"The Kitchen Garden Team"
    )

    # Send confirmation email
    send_mail(
        email_subject,
        email_body,
        'kitchengardenci@gmail.com',
        [checkout_data['email']],
        fail_silently=False,
    )

    # Clear the cart
    cart_items.delete()

    return render(request, 'store/success.html', {
        'order': order,
        'total_amount': checkout_data['amount']
    })

@login_required
def payment_cancel(request):
    # Render the cancel page
    return render(request, 'store/cancel.html')




@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_list.html', {'orders': orders})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, Product

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = []
    for item in order.items:
        product = get_object_or_404(Product, id=item['product_id'])
        order_items.append({
            'product': product,
            'quantity': item['quantity']
        })
    return render(request, 'store/order_detail.html', {'order': order, 'order_items': order_items})



#SUPERUSER 
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Product
from .forms import ProductForm

def superuser_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_superuser)(view_func)
    return decorated_view_func

@superuser_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

@superuser_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/edit_product.html', {'form': form, 'product': product})

@superuser_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    return render(request, 'store/confirm_delete.html', {'product': product})
