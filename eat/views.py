from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import MenuItem
from django.contrib.auth import login, authenticate  # Add these imports
from .forms import CustomUserCreationForm
# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Process the form data (e.g., save to database or send an email)
        return HttpResponse("Thank you for contacting us!")
    return render(request, 'home/contact.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('eat:index')  # Redirect to home page
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'home/register.html', {'form': form})


def menu(request):
    # Get all available items from the database
    menu_items = MenuItem.objects.filter(available=True).order_by('category')
    return render(request, 'home/menu.html', {'menu_items': menu_items})

# eat/views.py
def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for item_id, quantity in cart.items():
        item = get_object_or_404(MenuItem, id=item_id)
        item_total = item.price * quantity
        cart_items.append({
            'item': item,
            'quantity': quantity,
            'total': item_total
        })
        total += item_total
    
    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'home/cart.html', context)

def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart = request.session.get('cart', {})
    
    if str(item_id) in cart:
        cart[str(item_id)] += 1
    else:
        cart[str(item_id)] = 1
    
    request.session['cart'] = cart
    return redirect('eat:menu')

def update_cart(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        for item_id, quantity in request.POST.items():
            if item_id.isdigit():
                quantity = int(quantity)
                if quantity > 0:
                    cart[str(item_id)] = quantity
                else:
                    del cart[str(item_id)]
        request.session['cart'] = cart
    return redirect('eat:cart')

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        del cart[str(item_id)]
        request.session['cart'] = cart
    return redirect('eat:cart')
