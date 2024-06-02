from django.shortcuts import render, redirect
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.hashers import check_password


from .models import Order, OrderProduct, Product, Category, ProductReview
from userauths.models import Profile, User
from .forms import AddProductForm
from .decorators import admin_required

import datetime


@admin_required
def dashboard(request):
    revenue = Order.objects.aggregate(price=Sum("price"))
    total_orders_count = Order.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by("-id")[:6]
    latest_orders = total_orders_count.order_by("-id")

    this_month = datetime.datetime.now().month
    monthly_revenue = Order.objects.filter(
        order_date__month=this_month).aggregate(price=Sum("price"))

    context = {
        "monthly_revenue": monthly_revenue,
        "revenue": revenue,
        "all_products": all_products,
        "all_categories": all_categories,
        "new_customers": new_customers,
        "latest_orders": latest_orders,
        "total_orders_count": total_orders_count,
    }
    return render(request, "useradmin/dashboard.html", context)


@admin_required
def products(request):
    all_products = Product.objects.all()
    all_categories = Category.objects.all()

    context = {
        "all_products": all_products,
        "all_categories": all_categories,
    }
    return render(request, "useradmin/products.html", context)


@admin_required
def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            return redirect("sub_admin_dashboard-products")
    else:
        form = AddProductForm()
    context = {
        'form': form
    }
    return render(request, "useradmin/add-products.html", context)


@admin_required
def edit_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.save()
            form.save_m2m()
            return redirect("sub_admin_dashboard-products")
    else:
        form = AddProductForm(instance=product)
    context = {
        'form': form,
        'product': product,
    }
    return render(request, "useradmin/edit-products.html", context)


@admin_required
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect("sub_admin_dashboard-products")


@admin_required
def orders(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
    }
    return render(request, "useradmin/orders.html", context)


@admin_required
def order_detail(request, id):
    order = Order.objects.get(id=id)
    order_items = OrderProduct.objects.filter(order=order)
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, "useradmin/order_detail.html", context)


@admin_required
@csrf_exempt
def change_order_status(request, id):
    order = Order.objects.get(id=id)
    if request.method == "POST":
        status = request.POST.get("status")
        print("status =======", status)
        messages.success(request, f"Order status changed to {status}")
        order.product_status = status
        order.save()

    return redirect("sub_admin_order_detail", order.id)


@admin_required
def shop_page(request):
    products = Product.objects.filter(user=request.user)
    revenue = Order.objects.filter(
        paid_status=True).aggregate(price=Sum("price"))
    total_sales = OrderProduct.objects.filter(
        order__paid_status=True).aggregate(qty=Sum("qty"))

    context = {
        'products': products,
        'revenue': revenue,
        'total_sales': total_sales,
    }
    return render(request, "useradmin/shop_page.html", context)


@admin_required
def reviews(request):
    reviews = ProductReview.objects.all()
    context = {
        'reviews': reviews,
    }
    return render(request, "useradmin/reviews.html", context)


@admin_required
def settings(request):
    user = request.user
    if not Profile.objects.filter(user=request.user).exists():
        profile = Profile.objects.create(
            user=user, full_name=user.first_name, phone=user.phone)
    else:
        profile = Profile.objects.get(user=user)

    if request.method == "POST":
        image = request.FILES.get("image")
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        bio = request.POST.get("bio")
        address = request.POST.get("address")
        country = request.POST.get("country")
        print("image ===========", image)

        if image != None:
            profile.image = image
        profile.full_name = full_name
        profile.phone = phone
        profile.bio = bio
        profile.address = address
        profile.country = country

        profile.save()
        messages.success(request, "Profile Updated Successfully")
        return redirect("sub_admin_settings")

    context = {
        'profile': profile,
    }
    return render(request, "useradmin/settings.html", context)


@admin_required
def change_password(request):
    user = request.user
    if not Profile.objects.filter(user=request.user).exists():
        profile = Profile.objects.create(
            user=user, full_name=user.first_name, phone=user.phone)
    else:
        profile = Profile.objects.get(user=user)
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")

        if confirm_new_password != new_password:
            messages.error(
                request, "Confirm Password and New Password Does Not Match")
            return redirect("sub_admin_change_password")

        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password Changed Successfully")
            return redirect("sub_admin_change_password")
        else:
            messages.error(request, "Old password is not correct")
            return redirect("sub_admin_change_password")

    return render(request, "useradmin/change_password.html")
