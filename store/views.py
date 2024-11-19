from django.shortcuts import render, get_object_or_404 ,redirect
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem

def product_list(request):
    category = request.GET.get('category', 'all')  # Default to 'all' if no category is provided
    if category == 'all':
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category=category)
    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})




@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if product.stock > 0:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        product.stock -= 1
        product.save()
    return redirect('product_list')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'store/cart.html', {'cart_items': cart_items})


@login_required
def update_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id, user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart_view')

@login_required
def delete_cart_item(request, item_id):
    cart_item = CartItem.objects.get(id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')

##############
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem
from .forms import ShippingForm

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            return redirect('order_confirmation')
    else:
        form = ShippingForm()

    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'form': form})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem, Order
from .forms import ShippingForm

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            # Collect items in a dictionary
            items = {}
            for item in cart_items:
                items[item.product.id] = {
                    'name': item.product.name,
                    'quantity': item.quantity,
                    'price': float(item.product.price) 
                }

            # Create Order instance
            order = Order.objects.create(
                user=request.user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zip_code=form.cleaned_data['zip_code'],
                items=items  # Save items as JSON
            )
            # Clear the cart
            cart_items.delete()
            return redirect('order_confirmation')
    else:
        form = ShippingForm()

    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'form': form})

