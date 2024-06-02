from django.core.mail import send_mail
from django.shortcuts import render
import calendar
import random
from django.utils.translation import gettext_lazy as _
import stripe
from django.core.mail import send_mail
from core.forms import ConsultationForm, ProductReviewForm, InsuranceForm
from core.models import (
    CartOrder,
    CartOrderProduct,
    Category,
    Locations,
    Prescription,
    Product,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Count
from django.db.models.functions import ExtractMonth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import get_language
from userauths.models import ContactUs, User
from django.core.files.images import ImageFile

from .models import (
    Address,
    Advices,
    Coupon,
    Doctor,
    Insurance,
    MainCategory,
    Order,
    OrderProduct,
    ProductReview,
    Shipping,
    SubCategory,
    WishList,
    Consultation
)

stripe.api_key = "sk_test_51L3uK1BvsUtCkGsqXQRmyG0x77zJbliYFGwN8225mCjQUy6CnBZzoKHiDb0cubptFLy16DTIoAYfHMlqvoex4B7Q00YTk5w816"


def get_direction() -> str:
    if get_language() == "en":
        return "ltr"
    elif get_language() == "ar":
        return "rtl"


def index(request):

    current_date = timezone.now()
    featured = Product.objects.filter(featured=True)
    featured_list = Product.objects.filter(featured=True)[:4]
    products = Product.objects.filter(
    ).order_by("-id")

    page = request.GET.get("page", 1)
    paginator = Paginator(products, 30)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    trending = Product.objects.filter(
    ).order_by("-views")[:10]

    recent = Product.objects.filter(
    ).order_by("-id")[:10]

    rated = Product.objects.annotate(
        avg_rating=Avg("reviews__rating")
    ).order_by("-avg_rating")[:10]

    # main_cats = MainCategory.objects.all()

    context = {
        "current_lang": get_language(),
        "dir": get_direction(),
        "featured_list": featured_list,
        "products": products,
        "trending": trending,
        # "main_cats": main_cats,
        "rated": rated,
        "recent": recent,
        "featured": featured,
    }

    return render(request, "core/index.html", context)


def product_list_view(request):
    current_date = timezone.now()
    products = Product.objects.filter(
    ).order_by("-id")
    context = {
        "current_lang": get_language(),
        "dir": get_direction(),
        "products": products,
    }

    return render(request, "core/product-list.html", context)


def category_list_view(request):
    main_cats = MainCategory.objects.all()
    sub_cats = SubCategory.objects.all()
    categories = Category.objects.all()

    context = {
        "current_lang": get_language(),
        "dir": get_direction(),
        "main_cats": main_cats,
        "sub_cats": sub_cats,
        "categories": categories,
    }
    return render(request, "core/category-list.html", context)


def category_product_list__view(request, id):
    current_date = timezone.now()
    category = Category.objects.get(id=id)
    products = Product.objects.filter(category=category)

    context = {
        "current_lang": get_language(),
        "dir": get_direction(),
        "category": category,
        "products": products,
    }
    return render(request, "core/category-product-list.html", context)


def main_category_products(request, id):
    main_category = MainCategory.objects.get(id=id)
    sub_cats = main_category.subcats.all()
    products_list = []
    for i in sub_cats:
        categs = i.cats.all()
        for j in categs:
            products_list.append(j.products.all())
    context = {
        "current_lang": get_language(),
        "dir": get_direction(),
        "category": main_category,
        "products": products_list,
    }

    return render(request, "core/main-cats-.html", context)


def product_detail_view(request, id):
    product = Product.objects.get(id=id)
    product.views += 1
    product.save()

    # product = get_object_or_404(Product, id=id)
    products = Product.objects.filter(category=product.category).exclude(
        id=id
    )

    # Getting all reviews related to a product
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    # Getting average review
    average_rating = ProductReview.objects.filter(product=product).aggregate(
        rating=Avg("rating")
    )
    # Product Review form
    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:

        user_review_count = ProductReview.objects.filter(
            user=request.user, product=product
        ).count()

        if user_review_count > 0:
            make_review = False

    p_image = product.p_images.all()

    context = {
        "current_lang": get_language(),
        "dir": get_direction(),
        "p": product,
        "make_review": make_review,
        "review_form": review_form,
        "p_image": p_image,
        "average_rating": average_rating,
        "reviews": reviews,
        "products": products,
    }

    return render(request, "core/product-detail.html", context)


def ajax_add_review(request, id):
    product = Product.objects.get(pk=id)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST["review"],
        rating=request.POST["rating"],
    )

    context = {
        "current_lang": get_language(),
        "dir": get_direction(),
        "user": user.username,
        "review": request.POST["review"],
        "rating": request.POST["rating"],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(
        rating=Avg("rating")
    )

    return JsonResponse(
        {"bool": True, "context": context, "average_reviews": average_reviews}
    )


def search_view(request):
    current_date = timezone.now()
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by(
        "-date"
    )

    context = {
        "current_lang": get_language(),
        "dir": get_direction(),
        "products": products,
        "query": query,
    }
    return render(request, "core/search.html", context)


def add_to_cart_form(request):
    if request.user.is_authenticated:
        quantity = request.GET.get("qty")
        id = request.GET.get("id")
        user = request.user
        product = Product.objects.get(id=id)
        cart_orders = CartOrder.objects.filter(user=user)
        if cart_orders.exists():
            if CartOrderProduct.objects.filter(cart__user=user, product=product).exists():
                crt_update = CartOrderProduct.objects.filter(
                    cart__user=user, product=product).first()
                if int(quantity) == 0:
                    crt_update.delete()
                else:
                    crt_update.qty = int(quantity)
                    crt_update.save()

                context = {
                    "current_lang": get_language(),
                    "dir": get_direction(),
                    "msg": "Updated",
                    "count": CartOrderProduct.objects.filter(cart__user=user).count(),

                }
                return JsonResponse(context)
                # return redirect('/')
            else:
                cart = CartOrder.objects.filter(user=user).first()
                if int(quantity) > int(product.stock_count):
                    context = {
                        "current_lang": get_language(),
                        "dir": get_direction(),
                        "msg": "low quantity",
                        "count": CartOrderProduct.objects.filter(cart__user=user).count(),

                    }
                    return JsonResponse(context)
                    # return redirect('/')

                elif int(product.stock_count) == 0:
                    messages.warning(
                        request, _("product is in out of stock!")
                    )
                    # return redirect('/')
                    context = {
                        "current_lang": get_language(),
                        "dir": get_direction(),
                        "msg": "no stock",
                        "count": CartOrderProduct.objects.filter(cart__user=user).count(),

                    }
                    return JsonResponse(context)

                CartOrderProduct.objects.create(
                    cart=cart, product=product, qty=int(quantity)
                )
                context = {
                    "current_lang": get_language(),
                    "dir": get_direction(),
                    "msg": "added",
                    "count": CartOrderProduct.objects.filter(cart__user=user).count(),
                }
                return JsonResponse(context)
        else:
            cart = CartOrder.objects.create(user=user)
            CartOrderProduct.objects.create(
                cart=cart, product=product, qty=int(quantity)
            )
            context = {
                "current_lang": get_language(),
                "dir": get_direction(),
                "msg": "added",
                "count": CartOrderProduct.objects.filter(cart__user=user).count(),
            }
            return JsonResponse(context)
    else:
        return JsonResponse(
            {
                "msg": "login",
                "current_lang": get_language(),
                "dir": get_direction(),
                "count": CartOrderProduct.objects.filter(cart__user=user).count(),

            }
        )


@login_required
def add_to_cart(request, id):
    user = request.user
    product = Product.objects.get(id=id)
    carts = CartOrder.objects.filter(user=user)
    if carts.exists():
        if CartOrderProduct.objects.filter(cart__user=user, product=product).exists():
            messages.warning(
                request, _("product already exists in your cart! ")
            )
            return redirect("/")
        else:
            cart = CartOrder.objects.filter(user=user).first()
            CartOrderProduct.objects.create(cart=cart, product=product, qty=1)

    else:
        cart = CartOrder.objects.create(user=user)
        CartOrderProduct.objects.create(cart=cart, product=product, qty=1)
        messages.success(
            request, _("product added to your cart your cart! ")
        )
    return redirect("/")


@login_required
def cart_view(request):
    user = request.user
    if CartOrder.objects.filter(user=user).first():
        cart = CartOrder.objects.filter(user=user).first()

        items = cart.cart_products.all()
        if len(items) == 0:

            messages.warning(request, _("Your cart is empty"))
            return redirect("index")
        else:
            cart.price = cart.get_total_price()
            cart.save()
            context = {
                "current_lang": get_language(),
                "dir": get_direction(),
                "items": items,
                "cart": cart,
                "cart_price": cart.price,
            }
            return render(request, "core/cart.html", context)

    else:
        return redirect("index")


def delete_item_from_cart(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        product = CartOrderProduct.objects.get(id=item_id)
        product.delete()
        return redirect("cart")
    else:
        return redirect("cart")


@login_required
def update_cart(request):
    if request.method == "POST":
        quantity = request.POST.get("item_quantity")
        item_id = request.POST.get("item_id")
        product = CartOrderProduct.objects.get(id=item_id)
        product.qty = int(quantity)
        product.save()

        return redirect("cart")
    else:
        return redirect("cart")


def apply_coupon(request):
    if request.method == "POST":
        coupon = request.POST.get("coupon")
        cart_id = request.POST.get("cart")
        if Coupon.objects.filter(coupon=coupon, available=True).exists():
            coupon = Coupon.objects.filter(
                coupon=coupon, available=True
            ).first()
            cart = CartOrder.objects.get(id=cart_id)
            cart.coupon = coupon

            cart.save()
            return redirect("cart")
        else:
            messages.warning(request, _("Coupon Invalid or Expired!"))
            return redirect("cart")
    else:
        return redirect("cart")


def send_order_placed_email(email, username, products, invoice, link):
    subject = "You Placed An Order!"
    product_list = "\n".join([str(i.get("title")) for i in products])
    message = f"""
    Hi {username},
    
    You have placed your order with order id {invoice} for the following item(s):

    {product_list}

    To see more details, click the link below:

    {link}
    """
    recipient_list = [email]
    email_from = "gswithmak@email.com"

    send_mail(subject, message, email_from, recipient_list)


@login_required
def checkout_view(request):
    if request.method == "POST":
        cart_id = request.POST.get("cart_id")
        cart = CartOrder.objects.get(id=cart_id)
        totalcartitems = cart.cart_products.all()
        cart.price = cart.get_total_price()

        cart.save()

        updated_price = cart.price + Shipping.objects.all()[0].price
        try:
            active_address = Address.objects.get(
                user=request.user, status=True
            )
            return render(
                request,
                "core/checkout.html",
                {
                    "current_lang": get_language(),
                    "dir": get_direction(),
                    "cart": cart,
                    "cart_data": totalcartitems,
                    "totalcartitems": len(totalcartitems),
                    "cart_total_amount": cart.price,
                    "sub_total": updated_price,
                    "active_address": active_address,
                },
            )

        except:
            messages.warning(request, _("address should be activated."))
            active_address = None
            return render(
                request,
                "core/checkout.html",
                {
                    "current_lang": get_language(),
                    "dir": get_direction(),
                    "cart": cart,
                    "cart_data": totalcartitems,
                    "totalcartitems": len(totalcartitems),
                    "cart_total_amount": cart.price,
                    "sub_total": updated_price,
                    "active_address": active_address,
                },
            )

    else:
        return redirect("cart")


@login_required
def cod_checkout(request):
    if request.method == "POST":
        cart_id = request.POST.get("cart_id")
        cart = CartOrder.objects.get(id=cart_id)
        address = Address.objects.filter(
            user=request.user, status=True).first()
        updated_price = int(cart.get_total_price()) + int(
            Shipping.objects.all()[0].price
        )
        invoice = f"{cart_id}{random.randint(99, 9999)}"
        image = request.FILES.get("bank_invoice_pic")
        bank_invoice = ImageFile(image)
        order = Order.objects.create(
            user=request.user,
            address=address,
            price=updated_price,
            bank_invoice=bank_invoice,
            cod=True,
            payment_type="bank",
            invoice_id=invoice,
        )
        cart_products = cart.cart_products.all()
        for i in cart_products:
            OrderProduct.objects.create(
                order=order,
                product=i.product,
                qty=i.qty,
                price=i.price,
                total=i.total,
            )
        messages.success(request, _("Order Placed Successfully!"))
        url = reverse("payment_completed_by_cod") + f"?cart_id={cart_id}"
        return redirect(url)
    else:
        messages.warning(request, _("Order was not placed!"))
        return redirect("cart")


@login_required
def payment_completed_by_cod(request):
    user = request.user
    cart_id = request.GET.get("cart_id")
    cart = CartOrder.objects.get(id=cart_id)
    address = Address.objects.filter(user=user, status=True).first()
    updated_price = int(cart.get_total_price()) + int(
        Shipping.objects.all()[0].price
    )
    order = Order.objects.get(
        user=request.user,
        address=address,
        price=updated_price
    )
    invoice = order.invoice_id
    CartOrderProduct.objects.filter(cart=cart).delete()
    cart.delete()
    sub_total = order.price - int(Shipping.objects.all()[0].price)

    products = [{"title": i.product.title} for i in order.order_products.all()]
    link = f"https://luxeen.org/en/dashboard/order/{order.id}"
    send_order_placed_email(user.email, user.first_name,
                            products, invoice, link)

    return render(
        request,
        "core/payment-completed.html",
        {
            "cart_data": order,
            "sub_total": sub_total,
            "invoice": invoice,
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


@login_required
def become_pro(request, id):
    user_id = request.user
    cart = CartOrder.objects.get(id=id)
    price = cart.get_total_price() + Shipping.objects.all()[0].price
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": user_id.username,
                    },
                    "unit_amount": price * 100,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        metadata={"user_id": user_id, "cart_id": id},
        success_url=request.build_absolute_uri(reverse("payment-completed"))
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("payment-failed")),
    )

    context = {
        "current_lang": get_language(),
        "dir": get_direction(),
        "session_id": session.id,
    }
    return render(request, "core/stripe_checkout.html", context)


@login_required
def payment_completed_view(request):
    user = request.user
    # cart_id = request.GET.get('cart_id')
    # cart = CartOrder.objects.get(id=cart_id)
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)

    cart_id = session["metadata"]["cart_id"]
    cart = CartOrder.objects.get(id=cart_id)
    updated_price = int(cart.get_total_price()) + int(
        Shipping.objects.all()[0].price
    )

    invoice = f"{cart_id}{random.randint(99, 9999)}"
    address = Address.objects.filter(
        user=request.user, status=True).first()

    order = Order.objects.create(

        user=request.user,
        address=address,
        price=updated_price,
        paid_status=True,
        cod=False,
        payment_type="stripe",
        invoice_id=invoice,
    )
    cart_products = cart.cart_products.all()
    for i in cart_products:
        OrderProduct.objects.create(
            order=order,
            product=i.product,
            qty=i.qty,
            price=i.price,
            total=i.total,
        )
    CartOrderProduct.objects.filter(cart=cart).delete()
    cart.delete()
    sub_total = order.price - int(Shipping.objects.all()[0].price)
    invoice = order.invoice_id
    products = [{"title": i.product.title} for i in order.order_products.all()]
    link = f"https://luxeen.org/en/dashboard/order/{order.id}"
    send_order_placed_email(user.email, user.first_name,
                            products, invoice, link)

    return render(
        request,
        "core/payment-completed.html",
        {
            "invoice": invoice,
            "cart_data": order,
            "sub_total": sub_total,
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


@login_required
def payment_failed_view(request):
    return render(
        request,
        "core/payment-failed.html",
        {
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


@login_required
def add_address(request):
    if request.method == "POST":
        user = request.user
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        billing_address = request.POST.get("billing_address")
        if Address.objects.filter(user=user).exists():
            for address in Address.objects.filter(user=user):
                if address.status == True:
                    address.status = False
                    address.save()
        Address.objects.create(
            user=user, mobile=lname, address=billing_address, status=True
        )
        messages.success(request, _("Your address was added!"))
        return redirect("checkout")
    else:
        messages.warning(request, _("Your address was not added!"))
        return redirect("checkout")


@login_required
def customer_dashboard(request):
    orders_list = Order.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)

    orders = (
        Order.objects.annotate(month=ExtractMonth("order_date"))
        .values("month")
        .annotate(count=Count("id"))
        .values("month", "count")
    )
    month = []
    total_orders = []

    for i in orders:
        try:

            month.append(calendar.month_name[i["month"]])
            total_orders.append(i["count"])
        except:
            pass
    if request.method == "POST":
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")

        new_address = Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile,
        )
        messages.success(request, _("Address Added Successfully."))
        return redirect("dashboard")
    else:
        pass

    user_profile = User.objects.get(id=request.user.id)
    context = {
        "current_lang": get_language(),
        "dir": get_direction(),
        "user_profile": user_profile,
        "orders": orders,
        "orders_list": orders_list,
        "address": address,
        "month": month,
        "total_orders": total_orders,
    }
    return render(request, "core/dashboard.html", context)


def order_detail(request, id):
    order = Order.objects.get(id=id)
    invoice = order.invoice_id
    return render(
        request,
        "core/order-detail.html",
        {
            "invoice": invoice,
            "cart_data": order,
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


def make_address_default(request):
    id = request.GET["id"]
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse(
        {
            "boolean": True,
            "current_lang": get_language(),
            "dir": get_direction(),
        }
    )


@login_required
def wishlist_view(request):
    wishlist = WishList.objects.all()
    context = {
        "current_lang": get_language(),
        "dir": get_direction(),
        "w": wishlist,
    }
    return render(request, "core/wishlist.html", context)

    # w


# @login_required


def add_to_wishlist(request):
    if request.user.is_authenticated:
        product_id = request.GET["id"]
        product = Product.objects.get(id=product_id)
        context = {
            "current_lang": get_language(),
            "dir": get_direction(),
        }

        wishlist_count = WishList.objects.filter(
            product=product, user=request.user
        ).count()

        if wishlist_count > 0:
            context = {
                "current_lang": get_language(),
                "dir": get_direction(),
                "bool": False,
                "msg": "already added to wishlist",
            }
        else:
            new_wishlist = WishList.objects.create(
                user=request.user,
                product=product,
            )
            context = {
                "current_lang": get_language(),
                "dir": get_direction(),
                "bool": True,
                "count": WishList.objects.filter(user=request.user).count(),
            }

        return JsonResponse(context)
    else:
        context = {
            "current_lang": get_language(),
            "dir": get_direction(),
            "bool": False,
            "msg": "you need to login",
        }

        return JsonResponse(context)


# def remove_wishlist(request):
#     id = request.GET['id']
#     wishlist = WishList.objects.filter(user=request.user).values()

#     product = WishList.objects.get(id=id)
#     h = product.delete()

#     context = {
# "current_lang": get_language(),
# "dir": get_direction(),
#         "bool": True,
#         "wishlist":wishlist
#     }
#     t = render_to_string("core/async/wishlist-list.html", context)
#     return JsonResponse({"data": t, "w":wishlist})


def remove_wishlist(request):
    id = request.GET["id"]
    wishlist = WishList.objects.filter(user=request.user)
    wishlist_d = WishList.objects.get(id=id)
    delete_product = wishlist_d.delete()

    context = {
        "current_lang": get_language(),
        "dir": get_direction(),
        "bool": True,
        "w": wishlist,
    }
    wishlist_json = serializers.serialize("json", wishlist)
    t = render_to_string("core/wishlist-list.html", context)
    return JsonResponse({"data": t, "w": wishlist_json})


# Other Pages
def contact(request):
    return render(
        request,
        "core/contact.html",
        {
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


def ajax_contact_form(request):
    full_name = request.GET["full_name"]
    email = request.GET["email"]
    phone = request.GET["phone"]
    subject = request.GET["subject"]
    message = request.GET["message"]

    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )

    data = {"bool": True, "message": _("Message Sent Successfully")}

    return JsonResponse(
        {
            "data": data,
            "current_lang": get_language(),
            "dir": get_direction(),
        }
    )


def doctors(request):
    doctors = Doctor.objects.all()
    context = {
        "current_lang": get_language(),
        "dir": get_direction(),
        "doctors": doctors,
    }
    return render(request, "core/doctors_page.html", context)


@login_required
def prescriptions(request):
    preses = Prescription.objects.filter(user=request.user)
    return render(
        request,
        "core/prescriptions.html",
        {
            "preses": preses,
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


@login_required
def presform(request):

    return render(
        request,
        "core/presform.html",
        {
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


@login_required
def presinsurance(request):
    insurances = Insurance.objects.all()

    if request.method == "POST":
        form = InsuranceForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, _(
                "insurance order added successfully, we will view it within 15 minutes"))
    form = InsuranceForm()

    return render(
        request,
        "core/presinsurance.html",
        {
            "form": form,
            "insurances": insurances,
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


@login_required
def prescreate(request):
    user = request.user
    if request.method == "POST":

        subject = request.POST.get("subject")
        prescription = request.FILES.get("prescription")
        Prescription.objects.create(
            user=user,
            subject=subject,
            prescription=prescription,
        )
        messages.success(
            request,
            _("Your request is submitted you will soon get a verification email with the invoice"),
        )
        return redirect("prescriptions")
        # else:
        #     subject = request.POST.get("subject")
        #     image = request.FILES.get("img")
        #     Prescription.objects.create(
        #         user=user, subject=subject, image=image
        #     )
        #     messages.success(
        #         request,
        #         "Your request is submitted you will soon get a verification email with the invoice",
        #     )
        #     return redirect("prescribtions")
    else:
        messages.warning(request, _("Something Went Wrong"))

        return redirect("prescriptions")


def presdetails(request, id):
    pres = Prescription.objects.get(id=id)
    return render(
        request,
        "core/pres_details.html",
        {
            "pres": pres,
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


def advices(request):
    advices = Advices.objects.all()
    return render(
        request,
        "core/advices.html",
        {
            "advices": advices,
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


def advice(request, id):
    advice = Advices.objects.get(id=id)
    return render(
        request,
        "core/advice.html",
        {
            "advice": advice,
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


def location(request, id):
    location = Locations.objects.get(id=id)
    return render(
        request,
        "core/location.html",
        {
            "location": location,
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


def about_us(request):
    return render(
        request,
        "core/about_us.html",
        {
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


def purchase_guide(request):
    return render(
        request,
        "core/purchase_guide.html",
        {
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


def privacy_policy(request):
    return render(
        request,
        "core/privacy_policy.html",
        {
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


@login_required
def consultation(request, id):

    if request.method == "POST":
        form = ConsultationForm(
            data=request.POST or None, files=request.FILES
        )
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.doctor = Doctor.objects.get(id=id)
            form.save()
            messages.success(request, _(
                "your consultation is saved and will be viewed within 15 minutes"))
    form = ConsultationForm()
    return render(
        request,
        "core/consultation.html",
        {
            "form": form,
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )


@login_required
def consultation_payment(request, cid):
    consultation = Consultation.objects.filter(pk__exact=cid).first()
    if request.method == "POST":
        bank_invoice = request.FILES.get("bank_invoice_pic")
        consultation.bank_invoice = ImageFile(bank_invoice)
        consultation.save()
        messages.success(request, _(
            "your consultation is saved and will be viewed within 15 minutes"))

    return render(request, "con_pay.html", {"cons": consultation})


def terms_of_service(request):
    return render(
        request,
        "core/terms_of_service.html",
        {
            "current_lang": get_language(),
            "dir": get_direction(),
        },
    )
