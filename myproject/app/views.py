from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import Register
# from django.core.mail import send_mail
from .models import Product,Course,Teacher,FAQ,ContactInfo, ContactMessage,Newsletter, Footer, FooterContact
from .models import Product, Course
from django.shortcuts import render
import os

# ai
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from groq import Groq

# payment 
import razorpay
from django.conf import settings
import hmac
import hashlib
from django.http import HttpResponse
from .models import Order, OrderItem
import uuid
# strip 
import stripe
from django.conf import settings
# message 
from django.contrib import messages


def index(request):
    products = Product.objects.all()
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    faqs = FAQ.objects.all()
    contact = ContactInfo.objects.first()
    footer = Footer.objects.first()
    footer_contact = FooterContact.objects.first()

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')


        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
            
        )
        return redirect('/')# reload page
    
    return render(request, "index2.html", {
        'products': products,
        'courses': courses,
        'teachers':teachers,
        'faq':faqs,
        'contact':contact,
        'footer': footer,
        'footer_contact': footer_contact
    })

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


# REGISTER VIEW
def register_user(request):

    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        country = request.POST.get('country')

        # print(username, email, country)

        try:

            # check duplicate email
            if Register.objects.filter(email=email).exists():

                return JsonResponse({
                    "status": "error",
                    "message": "Email already registered"
                })

            # create user with hashed password
            user = Register.objects.create(
                username=username,
                country=country,
                email=email,
                password=make_password(password)
            )

            return JsonResponse({
                "status": "success",
                "username": user.username,
                "country": user.country,
                "email": user.email
            })

        except Exception as e:

            return JsonResponse({
                "status": "error",
                "message": "Registration failed"
            })

    return JsonResponse({
        "status": "error",
        "message": "Invalid request"
    })


# LOGIN VIEW
def login_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = Register.objects.filter(username=username).first()

        if user and check_password(password, user.password):

            request.session['username'] = user.username

            return JsonResponse({
                "status": "success",
                "redirect": "/"
            })

        else:

            return JsonResponse({
                "status": "error",
                "message": "Invalid username or password"
            })

def logout_user(request):
    request.session.flush()   # ✅ clear all session data
    messages.success(request, "Logged out successfully ✅")
    return redirect('/')

# DASHBOARD
def dashboard(request):

    if 'username' not in request.session:
        return redirect("index")

    username = request.session.get("username")

    return render(request, "dashboard.html", {"username": username})


# # ADD TO CART
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     cart = request.session.get('cart', {})

#     if str(product_id) in cart:
#         cart[str(product_id)]['quantity'] += 1
#     else:
#         cart[str(product_id)] = {
#             'name': product.pr_name,
#             'price': float(product.pr_price),
#             'image': product.pr_url_image.url,
#             'quantity': 1
#         }

#     request.session['cart'] = cart
#     return redirect('cart')

# order
def order_history(request):
    username = request.session.get('username')

    orders = Order.objects.filter(customer_name=username).order_by('-created_at')

    return render(request, 'orders.html', {'orders': orders})

# ADD TO CART
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id]['qty'] += 1
    else:
        from .models import Product
        product = Product.objects.get(id=product_id)

        cart[product_id] = {
            'name': product.pr_name,
            'price': float(product.pr_price),
            'image': product.pr_url_image.url,
            'qty': 1
        }

    request.session['cart'] = cart

    # ✅ success message
    messages.success(request, "Item added to cart")

    # ✅ redirect to homepage (where navbar is)
    return redirect('/')


# VIEW CART
def cart_view(request):
    cart = request.session.get('cart', {})

    total = 0
    for item in cart.values():
        qty = item.get('qty', 1)
        total += item['price'] * qty

    return render(request, 'cart.html', {'cart': cart, 'total': total})


# REMOVE ITEM
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart')

# INCREASE QTY
def increase_qty(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id]['qty'] += 1

    request.session['cart'] = cart
    return redirect('cart')


# DECREASE QTY
# DECREASE QTY (MIN = 1)
def decrease_qty(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        if cart[product_id]['qty'] > 1:
            cart[product_id]['qty'] -= 1
        # ❌ Do NOT delete item when qty = 1

    request.session['cart'] = cart
    return redirect('cart')


# UPDATE QUANTITY
def update_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        action = request.POST.get('action')
        qty = cart[str(product_id)].get('qty', 1)

        if action == 'increase':
            cart[str(product_id)]['qty'] = qty + 1
        elif action == 'decrease':
            cart[str(product_id)]['qty'] = qty - 1
            if cart[str(product_id)]['qty'] <= 0:
                del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart')


# Razorpay 
# # # VERIFY PAYMENT
# # @csrf_exempt
# # def verify_payment(request):
# #     if request.method == "POST":

# #         client = razorpay.Client(
# #             auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
# #         )

# #         params_dict = {
# #             'razorpay_order_id': request.POST.get('razorpay_order_id'),
# #             'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
# #             'razorpay_signature': request.POST.get('razorpay_signature')
# #         }

# #         try:
# #             client.utility.verify_payment_signature(params_dict)

# #             # ✅ clear cart after success
# #             request.session['cart'] = {}

# #             messages.success(request, "Payment Successful ✅")

# #             return redirect('/')

# #         except:
# #             messages.error(request, "Payment Failed ❌")
# #             return redirect('/cart/')


# @csrf_exempt
# def verify_payment(request):
#     if request.method == "POST":

#         client = razorpay.Client(
#             auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
#         )

#         params_dict = {
#             'razorpay_order_id': request.POST.get('razorpay_order_id'),
#             'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
#             'razorpay_signature': request.POST.get('razorpay_signature')
#         }

#         try:
#             client.utility.verify_payment_signature(params_dict)

#             cart = request.session.get('cart', {})

#             total = 0
#             for item in cart.values():
#                 total += float(item['price']) * int(item.get('qty', 1))

#             # ✅ Create Order
#             order = Order.objects.create(
#                 order_id=str(uuid.uuid4()),
#                 customer_name=request.session.get('username', 'Guest'),
#                 total_amount=total
#             )

#             # ✅ Save each product
#             for item in cart.values():
#                 OrderItem.objects.create(
#                     order=order,
#                     product_name=item['name'],
#                     price=item['price'],
#                     quantity=item['qty']
#                 )

#             # ✅ Clear cart
#             request.session['cart'] = {}

#             messages.success(request, "Payment Successful ✅")
#             return redirect('/orders/')

#         except:
#             messages.error(request, "Payment Failed ❌")
#             return redirect('/cart/')



# Strip 
stripe.api_key = settings.STRIPE_SECRET_KEY


# CREATE CHECKOUT SESSION
def stripe_checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "Cart is empty!")
        return redirect('/')

    line_items = []

    for item in cart.values():
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': item['name'],
                },
                'unit_amount': int(float(item['price']) * 100),
            },
            'quantity': item.get('qty', 1),
        })

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://127.0.0.1:8000/payment-success/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/payment-cancel/',
        )

        return redirect(session.url)

    except Exception as e:
        return str(e)
    
def payment_success(request):
    session_id = request.GET.get('session_id')

    if not session_id:
        return redirect('/')

    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == "paid":

        cart = request.session.get('cart', {})

        if not cart:
            return render(request, 'success.html')

        total = 0
        for item in cart.values():
            total += float(item['price']) * int(item.get('qty', 1))

        # ✅ Create Order
        order = Order.objects.create(
            order_id=str(uuid.uuid4()),
            customer_name=request.session.get('username', 'Guest'),
            total_amount=total
        )

        # ✅ Save Items
        for item in cart.values():
            OrderItem.objects.create(
                order=order,
                product_name=item.get('name'),
                price=item.get('price'),
                quantity=item.get('qty')
            )

        # ✅ Clear cart AFTER saving
        request.session['cart'] = {}

        messages.success(request, "Payment Successful ✅")

        return render(request, 'success.html', {'order': order})

    return redirect('/')


def payment_cancel(request):
    messages.error(request, "Payment Cancelled ❌")
    return render(request, 'cancel.html')

def order_history(request):
    username = request.session.get('username')

    orders = Order.objects.filter(
        customer_name=username
    ).order_by('-created_at')

    return render(request, 'orders.html', {'orders': orders})

# ai chatbot
@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "")

        headers = {
            "Authorization": os.getenv("GROQ_API_KEY")
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        result = response.json()
        print("GROQ RESPONSE:", result)

        # Safe parsing
        if "choices" in result:
            reply = result["choices"][0]["message"]["content"].strip()

            # Basic dynamic comment check
            bad_keywords = ["bad", "hate", "stupid", "ugly", "idiot", "nonsense"]
            if any(word in reply.lower() for word in bad_keywords):
                reply = "⚠️ Sorry, your comment cannot be shown."

        else:
            reply = result.get("error", {}).get("message", "⚠️ Groq API error")

    except Exception as e:
        print("ERROR:", e)
        reply = "⚠️ Groq API error"

    return JsonResponse({"reply": reply})
