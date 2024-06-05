from django.utils.deconstruct import deconstructible
from uuid import uuid4
import os
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models import Avg, Count
from django.utils import timezone
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from userauths.models import User

STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)


RATING = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        filename = "{}.{}".format(uuid4().hex, ext)
        return os.path.join(self.path, filename)


class Address(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="addresses"
    )
    mobile = models.CharField(max_length=300, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:

        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
        db_table = "addresses_db"

    def __str__(self):
        return self.address


class BigBanner(models.Model):
    image = models.ImageField(
        upload_to="big_banners", default="big_banners.jpg"
    )
    name = models.CharField(max_length=50, default="Skin Care")
    url = models.URLField(blank=True, null=True)
    user_catcher = models.CharField(max_length=50, default="Big discount")
    short_line = models.CharField(
        max_length=100, default="Save 80 percent on all products flat"
    )

    class Meta:

        verbose_name = _("Big Banner")
        verbose_name_plural = _("Big Banners")
        db_table = "big_bunners_db"

    def __str__(self):
        return self.name


class SideBanner(models.Model):
    image = models.ImageField(
        upload_to="side_banners", default="side_banners.jpg"
    )
    type = models.CharField(max_length=50, default="organic")
    url = models.URLField(blank=True, null=True)
    user_catcher = models.CharField(
        max_length=50, default="discounts no all products"
    )

    class Meta:

        verbose_name = _("Side Banner")
        verbose_name_plural = _("Side Banners")
        db_table = "side_bunners_db"

    def __str__(self):
        return self.type


class MainCategory(models.Model):
    title = models.CharField(max_length=100, default="")
    image = models.ImageField(
        upload_to="maincategory", default="category.jpg"
    )

    class Meta:

        verbose_name = _("Main Category")
        verbose_name_plural = _("Main Categories")
        db_table = "main_categories_db"

    def category_image(self):
        return mark_safe(
            '<img src="%s" width="50" height="50" />' % (self.image.url)
        )

    def product_count(self):
        # count the number of products for each category
        category_counts = Category.objects.filter(
            sub_cat__main_cat=self
        ).annotate(product_count=Count("products"))

        # sum up the product counts for all categories
        total_product_count = sum([c.product_count for c in category_counts])

        return total_product_count

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    main_cat = models.ForeignKey(
        MainCategory, on_delete=models.CASCADE, related_name="subcats"
    )
    title = models.CharField(max_length=100, default="")
    image = models.ImageField(upload_to="subcategory", default="category.jpg")

    class Meta:

        verbose_name = _("Sub Category")
        verbose_name_plural = _("Sub Categories")
        db_table = "sub_categories_db"

    def category_image(self):
        return mark_safe(
            '<img src="%s" width="50" height="50" />' % (self.image.url)
        )

    def __str__(self):
        return self.title


class Category(models.Model):
    sub_cat = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name="cats"
    )
    title = models.CharField(max_length=100, default="")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        db_table = "categories_db"

    def category_image(self):
        return mark_safe(
            '<img src="%s" width="50" height="50" />' % (self.image.url)
        )

    def __str__(self):
        return self.title


class ProductType(models.Model):
    title = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products",
    )
    medicine_type = models.ForeignKey(
        ProductType, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100, default="")
    image = models.ImageField(
        upload_to="ProductImages", default="product.jpg"
    )
    # description = models.TextField(null=True, blank=True, default="This is the product")
    description = RichTextUploadingField(
        null=True, blank=True, default="This is the product"
    )

    price = models.PositiveIntegerField()
    old_price = models.PositiveIntegerField(null=True, blank=True)

    specifications = RichTextUploadingField(null=True, blank=True)
    # specifications = models.TextField(null=True, blank=True)

    stock_count = models.IntegerField(
        default=100
    )

    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    is_prescription = models.BooleanField(default=False)

    views = models.PositiveIntegerField(default=0)

    date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    class Meta:

        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        db_table = "products_db"

    def product_image(self):
        return mark_safe(
            '<img src="%s" width="50" height="50" />' % (self.image.url)
        )

    def __str__(self):
        return self.title

    def get_precentage(self):
        if self.old_price is None or self.old_price == 0 or self.old_price <= self.price:
            return 0
        else:
            new_price = (1 - (int(self.price) / int(self.old_price))) * 100
            return new_price

    def average_rating(self):
        try:
            return {"rating_value": self.reviews.aggregate(Avg("rating"))["rating__avg"], "rating_percentage": 100 * (float(self.reviews.aggregate(Avg("rating"))["rating__avg"])/5)}
        except:
            return {"rating_value": 0, "rating_percentage": 0}


class ProductImage(models.Model):
    image = models.ImageField(
        upload_to="product-images", default="product.jpg"
    )
    product = models.ForeignKey(
        Product,
        related_name="p_images",
        on_delete=models.SET_NULL,
        null=True,
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        db_table = "product_images_db"


class SpecialTimeOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    end_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:

        verbose_name = _("Special Time Offer")
        verbose_name_plural = _("Special Time Offers")
        db_table = "special_time_offers_db"

    def ending(self):
        date_time = self.end_at.strftime("%Y-%m-%d %H:%M:%S")
        return date_time


class Coupon(models.Model):
    coupon = models.CharField(max_length=20)
    percentage = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")
        ordering = ["coupon"]
        db_table = "coupons_db"

    def __str__(self):
        return f"{self.coupon}:  {self.percentage}%"


class Shipping(models.Model):
    price = models.IntegerField(default=500)

    class Meta:
        verbose_name = _("Shipping Price")
        verbose_name_plural = _("Shipping Prices")
        db_table = "shipping_prices_db"

    def __str__(self):
        return f"{self.price}"


class CartOrder(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="carts"
    )
    price = models.PositiveIntegerField(blank=True, null=True)
    order_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True)

    class Meta:

        verbose_name = _("Cart Order")
        verbose_name_plural = _("Cart Orders")
        db_table = "cart_orders_db"

    def get_total_price(self):

        total_price = 0
        for item in self.cart_products.all():
            total_price += item.qty * item.price
        self.price = total_price
        if self.coupon != None:
            discounts = self.price * (self.coupon.percentage / 100)
            self.price = total_price - discounts
            return self.price
        else:
            return self.price

    def get_all_cart_items(self):

        number = self.cart_products.all().count()
        return number


class CartOrderProduct(models.Model):
    cart = models.ForeignKey(
        CartOrder, on_delete=models.CASCADE, related_name="cart_products"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="in_cart_products",
        blank=True,
        null=True,
    )
    qty = models.IntegerField(default=0)
    price = models.PositiveIntegerField(blank=True, null=True)
    total = models.PositiveIntegerField(blank=True, null=True)

    class Meta:

        verbose_name = _("Cart Order Item")
        verbose_name_plural = _("Cart Order Items")
        db_table = "cart_order_items_db"

    def __str__(self):
        return self.product.title

    def order_img(self):
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" />' % (self.image)
        )

    def save(self, *args, **kwargs):
        # Get the price of the related Product instance
        product_price = self.product.price

        # Set the price and calculate the total based on the quantity
        self.price = product_price
        self.total = self.qty * product_price

        # Call the parent save method to save the model instance
        super(CartOrderProduct, self).save(*args, **kwargs)


############################################## Product Revew, wishlists, Address ##################################


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders"
    )
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True
    )

    price = models.PositiveIntegerField(blank=True, null=True)
    paid_status = models.BooleanField(default=False, null=True, blank=True)
    cod = models.BooleanField(default=False, null=True, blank=True)
    payment_type = models.CharField(max_length=50,)
    order_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )
    bank_invoice = models.ImageField(
        upload_to=PathAndRename("bank_invoices/"), blank=True)
    product_status = models.CharField(
        choices=STATUS_CHOICE, max_length=30, default="processing"
    )
    invoice_id = models.CharField(max_length=20, default="")

    class Meta:

        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        db_table = "orders"

    def get_total_price(self):
        return self.price


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_products"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="in_order_products",
        blank=True,
        null=True,
    )
    qty = models.IntegerField(default=0)
    price = models.PositiveIntegerField(blank=True, null=True)
    total = models.PositiveIntegerField(blank=True, null=True)

    class Meta:

        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
        db_table = "order_items_db"

    def __str__(self):
        return self.product.title

    def order_img(self):
        return mark_safe(
            '<img src="/media/%s" width="50" height="50" />' % (self.image)
        )

    def save(self, *args, **kwargs):
        # Get the price of the related Product instance
        product_price = self.product.price

        # Set the price and calculate the total based on the quantity
        self.price = product_price
        self.total = self.qty * product_price

        # Call the parent save method to save the model instance
        super(OrderProduct, self).save(*args, **kwargs)


class ProductReview(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reviews",
    )
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = _("Product Review")
        verbose_name_plural = _("Product Reviews")
        db_table = "product_reviews_db"

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating


class WishList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="wishes",
    )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = _("Whishlist")
        verbose_name_plural = _("Whishlists")
        db_table = "wishlists_db"

    def __str__(self):
        return self.product.title


class PrescriptionAbstract(models.Model):
    subject = models.CharField(max_length=200)
    prescription = models.ImageField(
        upload_to=PathAndRename("prescriptions/")
    )

    class Meta:
        abstract = True
        db_table = "prescription_abstract_db"


class Insurance(PrescriptionAbstract):
    CHOICES = (
        ("1", "الشركة التعاونية للتأمين"),
    )
    company = models.CharField(max_length=200, choices=CHOICES)
    insurance_card = models.ImageField(upload_to=PathAndRename("insurances"))
    done = models.BooleanField(
        _("done"), default=False
    )

    class Meta:

        verbose_name = _("Insurance")
        verbose_name_plural = _("Insurances")
        db_table = "insurances_db"

    def __str__(self):
        return self.company


class Prescription(PrescriptionAbstract):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="prescriptions"
    )

    class Meta:
        verbose_name = _("Prescription")
        verbose_name_plural = _("Prescriptions")
        db_table = "prescriptions_db"

    def __str__(self):
        return self.user.username


class Doctor(models.Model):
    name = models.CharField(max_length=70)
    details = models.TextField(null=True, blank=True)
    specialty = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    image = models.ImageField(upload_to="Doctors")
    timing = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:

        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")
        db_table = "doctors_db"

    def __str__(self):
        return self.name


class Consultation(PrescriptionAbstract):
    user = models.ForeignKey(
        User, models.CASCADE, related_name="consultations"
    )
    doctor = models.ForeignKey(
        Doctor, models.CASCADE, related_name="consultations"
    )
    content = models.TextField()
    bank_invoice = models.ImageField(
        upload_to=PathAndRename("bank_invoices/"), blank=True)

    class Meta:
        verbose_name = _("Consultation")
        verbose_name_plural = _("Consultations")
        db_table = "consultations_db"


class Advices(models.Model):
    image = models.ImageField(upload_to="advices")
    title = models.CharField(max_length=1000, blank=True, null=True)
    description = models.TextField()
    advice = RichTextUploadingField(null=True, blank=True)

    class Meta:

        verbose_name = _("Advice")
        verbose_name_plural = _("Advices")
        db_table = "advices_db"

    def __str__(self):
        return self.title


class Locations(models.Model):
    city_name = models.CharField(max_length=300, null=True, blank=True)
    map_iframe = models.CharField(max_length=2000)
    details = RichTextUploadingField(null=True, blank=True)

    class Meta:

        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        db_table = "locations_db"

    def __str__(self):
        return self.city_name


class Bank(models.Model):
    instructions = RichTextUploadingField()
    account_info = RichTextUploadingField()

    class Meta:

        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")
        db_table = "banks_db"

    def __str__(self):
        return f"Account id={self.id}"


class AboutUs(models.Model):
    pass
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    description = RichTextUploadingField()

    class Meta:

        verbose_name = _("Aboutus")
        verbose_name_plural = _("About Us")
        db_table = "about_us_db"
