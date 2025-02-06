from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json, random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from .models import R_image, Slide_img, Bestsell, Profile, Cart, OrderHistory
from .forms import UserForm, UserProfileForm


# Create your views here.


#Register / SignUp
def register(request):
    if request.method == 'POST':
        # Instantiate the forms with POST data
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                # Create user
                user = user_form.save(commit=False)  # Save without committing
                password = user_form.cleaned_data.get('password1')

                # Validate and set the password
                validate_password(password, user)  # Use Django's password validation
                user.set_password(password)
                user.save()
                
                #Create and Save the profile
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                # login(request, user)
                # Redirecting to login page
                return redirect('log_in')  # Redirect to the profile page

            except Exception as e:
                return HttpResponse(f"Error: {str(e)}", status=400)

        else:
            # Provide feedback if the forms are invalid
            context = {
                'user_form': user_form,
                'profile_form': profile_form,
            }
            return render(request, 'register.html', context)

    else:
        # Render empty forms for GET requests
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'register.html', context)

#Login
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to homepage/index
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'enter.html')

# Logout
def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url='log_in')         #Homepage
def index(req):
    images = R_image.objects.all().order_by('order')  # Sort by the 'order' field
    images2 = Slide_img.objects.all().order_by('order')  # Sort by the 'order' field
    best = Bestsell.objects.all().order_by('order')  # Sort by the 'order' field
    
    for bg in best:
        bg.is_nonveg = bg.order in [16, 19, 20,27]
    context = {
        'images': images,
        'images2': images2,
        'best': best,
    }
    
    return render(req,'index.html',context)

@login_required(login_url='log_in')
def user_profile(request):
    user = request.user  # Get the logged-in user
    profile = get_object_or_404(Profile, user=user)
    
    context = {
        'profile': profile,
        'user': user,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='log_in')
def update(request):
    user = request.user  # Get the logged-in user
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        password = request.POST.get('password')

        # Update User model
        user.email = email
        
        if password:  # Check if a new password was provided
            user.set_password(password)
            update_session_auth_hash(request, user)  # Prevent logout by updating the session hash
        
        user.save()

        # Update Profile model
        if 'user_img' in request.FILES:  # Check if a new profile picture was uploaded
            uploaded_file = request.FILES['user_img']
            profile.user_img = uploaded_file
            print(f"Profile image updated to: {uploaded_file.name}")
    
        profile.phone = phone if phone else profile.phone
        profile.age = int(age) if age else profile.age
        profile.dob = dob if dob else profile.dob
        profile.gender = gender if gender else profile.gender
        profile.save()

        return redirect('user_profile')

    context = {
        'user': user,
        'profile': profile
    }

    return render(request, 'update.html', context)


@login_required(login_url='log_in')
def cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    # Calculate the total price of all items in the cart
    total_price = sum(item.get_total_price() for item in cart_items)
    gst = round((18 / 100) * total_price, 2)
    delivery_fee = 40  # Default delivery fee
    total_with_delivery = round(total_price + delivery_fee + gst, 2)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'delivery_fee': delivery_fee,
        'total_with_delivery': total_with_delivery,
        'gst' : gst,
    }
    return render(request, 'cart.html', context)


@login_required(login_url='log_in')
def add_to_cart(request, item_id):
    user = request.user
    item = get_object_or_404(Bestsell, id=item_id)

    # Check if the item is already in the cart
    cart_item, created = Cart.objects.get_or_create(user=user, item=item)

    if not created:
        # If the item is already in the cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect('index')

@login_required(login_url='log_in')
def remove(request, c_id):
    cart_item = get_object_or_404(Cart, id=c_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='log_in')
def hremove(request, h_id):
    hist_item = get_object_or_404(OrderHistory, id=h_id, user=request.user)
    hist_item.delete()
    return redirect('order_history')

@csrf_exempt
@login_required
def update_quantity(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            action = data.get("action")
            item_id = data.get("item_id")

            # Fetch the cart item
            cart_item = get_object_or_404(Cart, id=item_id, user=request.user)

            # Update quantity
            if action == "increase":
                cart_item.quantity += 1
            elif action == "decrease" and cart_item.quantity > 1:
                cart_item.quantity -= 1
            cart_item.save()

            # Recalculate totals
            cart_items = Cart.objects.filter(user=request.user)
            total_price = sum(item.item.price * item.quantity for item in cart_items)
            gst = round(0.18 * total_price, 2)  # Round GST to two decimal places
            delivery_fee = 40  # Example delivery fee
            total_with_delivery = round(total_price + gst + delivery_fee, 2)

            return JsonResponse({
                "success": True,
                "new_quantity": cart_item.quantity,
                "item_total": round(cart_item.item.price * cart_item.quantity, 2),
                "total_price": round(total_price, 2),
                "gst": gst,
                "total_with_delivery": total_with_delivery,
            })

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method"})

@login_required(login_url='log_in')
def order_history(request):
    user = request.user
    orders = OrderHistory.objects.filter(user=user).order_by("-order_date")
    return render(request, "history.html", {"orders": orders})

@login_required(login_url='log_in')
def checkout(request):
    if request.method == "POST":
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        
        if not cart_items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect("cart")

        # Save cart items to OrderHistory
        order_details = []
        total_price = 0          # Calculating total cart price
        for cart_item in cart_items:
            OrderHistory.objects.create(
                user=user,
                item=cart_item.item,
                quantity=cart_item.quantity,
                total_price=cart_item.quantity * cart_item.item.price,
                image=cart_item.item.image,
            )
        
            # Add item details for the email
            item_total = cart_item.quantity * cart_item.item.price
            order_details.append(
                f"{cart_item.quantity} x {cart_item.item.name} - ₹{item_total}"
            )
            total_price += item_total  # Update the total price
        
        # Compose the email
        subject = 'Your Order has been taken for delivery!'
        message = (
            f"Dear {user.username},\n\n"
            "Thank you for your order! Your items are as follows:\n\n"
            f"{chr(10).join(order_details)}\n\n"
            f"Total Price: ₹{total_price + 40}\n\n"
            "Please have patience, your order will arrive soon.\n\n"
            "Best regards,\nDomino's"
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        # Send the email
        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")        
        
        # Clear the cart after checkout
        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect("order_history")
    else:
        return redirect("cart")