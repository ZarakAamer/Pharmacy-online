from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import (
    Address,
    Advices,
    Bank,
    BigBanner,
    CartOrder,
    CartOrderProduct,
    Category,
    Consultation,
    Coupon,
    Doctor,
    Insurance,
    Locations,
    MainCategory,
    Order,
    OrderProduct,
    Prescription,
    Product,
    ProductImage,
    ProductReview,
    Shipping,
    SpecialTimeOffer,
    SubCategory,
    WishList,
    AboutUs,
    ProductType
)


# import random
# from import_export import resources, fields
# from import_export.widgets import ForeignKeyWidget
# from .models import Product, Category


# def create_en_title():
#     random_number = str(random.randint(0, 9999999))
#     name = "Title" + random_number
#     return name


# arabic_start = 0x0600
# arabic_end = 0x06FF


# def generate_random_arabic_char():
#     """Generate a random Arabic character."""
#     return chr(random.randint(arabic_start, arabic_end))


# def generate_random_arabic_word(length):
#     """Generate a random Arabic word of a given length."""
#     word = ''.join(generate_random_arabic_char() for _ in range(length))
#     return word


# create_ar_title = generate_random_arabic_word(15)


# class MyModelResource(resources.ModelResource):
#     category = fields.Field(
#         column_name='category',
#         attribute='category',
#         widget=ForeignKeyWidget(Category, 'title')
#     )

#     title_ar = fields.Field(
#         column_name='title_ar',
#         attribute='title_ar'
#     )

#     title_fr = fields.Field(
#         column_name='title_fr',
#         attribute='title_fr'
#     )

#     description_ar = fields.Field(
#         column_name='description_ar',
#         attribute='description_ar'
#     )

#     description_fr = fields.Field(
#         column_name='description_fr',
#         attribute='description_fr'
#     )

#     specifications_ar = fields.Field(
#         column_name='specifications_ar',
#         attribute='specifications_ar'
#     )

#     specifications_fr = fields.Field(
#         column_name='specifications_fr',
#         attribute='specifications_fr'
#     )

#     class Meta:
#         model = Product
#         fields = ('category', 'title', 'title_ar', 'title_fr', 'image', 'description', 'description_ar', 'description_fr', 'specifications', 'specifications_ar', 'specifications_fr', 'price', 'old_price',
#                   'stock_count', 'in_stock', 'featured', 'is_prescription', 'expiry_date')
#         export_order = fields
#         import_id_fields = ('title',)  # Use a unique field to identify records

#     def dehydrate_category(self, product):
#         return product.category.title if product.category else ''

#     def before_import_row(self, row, row_number=None, **kwargs):
#         if 'category' in row:
#             category_title = str(row['category']).strip()
#             print(f"Processing row {row_number}: {category_title}")
#             try:
#                 category = Category.objects.get(title=category_title)
#                 print(f"Found existing category: {category.title}")
#             except Category.DoesNotExist:
#                 print(
#                     f"Category does not exist, creating new category: {category_title}")
#                 category = Category.objects.get(title="General")

#             row['category'] = category.title
#             print(f"Updated row {row_number} with category ID: {category.id}")

#     # def skip_row(self, instance, original):
#     #     # Ignore the 'id' field during import
#     #     return 'id' in original
#         # Define default values for all fields
#             default_values = {
#                 'title_ar': generate_random_arabic_word(15),
#                 'description_ar': generate_random_arabic_word(25),
#                 'description_fr': 'Description par défaut',
#                 'specifications_ar': generate_random_arabic_word(25),
#                 'specifications_fr': 'Spécifications par défaut',
#                 'title': create_en_title(),
#                 # Assuming you want a default image
#                 'image': 'https://www.flaticon.com/free-icons/medicine',
#                 'description': 'Default Description',
#                 'specifications': 'Default Specifications',
#                 'price': 0.0,
#                 'old_price': 0.0,
#                 'stock_count': 0,
#                 'in_stock': True,
#                 'featured': False,
#                 'is_prescription': False,
#                 'expiry_date': '4/21/2040 21:47'  # Future date as default
#             }

#             for field, default_value in default_values.items():
#                 if not row.get(field):
#                     row[field] = default_value


# class MyModelAdmin(ImportExportModelAdmin):
#     resource_class = MyModelResource

#     def get_import_formats(self):
#         # Ensure the file is read as UTF-8
#         import_formats = super().get_import_formats()
#         for format in import_formats:
#             if hasattr(format, 'get_read_mode'):
#                 format.get_read_mode = lambda: ('rt', {'encoding': 'utf-8'})
#         return import_formats


# class MyModelAdmin(ImportExportModelAdmin):
#     resource_class = MyModelResource


# admin.site.register(Product, MyModelAdmin)

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    ...


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    search_fields = ["title"]
    list_filter = ["featured", "category"]
    list_editable = [
        "price",
        "featured",
    ]
    list_display = [
        "title",
        "product_image",
        "price",
        "stock_count",
        "category",
        "featured",
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "category_image"]
    search_fields = ["title"]


class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "category_image"]
    search_fields = ["title"]


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "category_image"]
    search_fields = ["title"]


class OrdersProductsAdmin(admin.TabularInline):
    model = OrderProduct


class OrderAdmin(admin.ModelAdmin):
    list_filter = ["paid_status", "cod"]
    list_editable = [
        "paid_status",
    ]
    list_display = ["user", "price", "paid_status", "cod", "order_date"]
    inlines = [OrdersProductsAdmin]


class OrderProductsAdmin(admin.ModelAdmin):
    list_display = ["order", "qty", "price", "total"]


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "review", "rating"]


class wishlistAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "date"]


class AddressAdmin(admin.ModelAdmin):
    list_editable = ["address", "status"]
    list_display = ["user", "address", "status"]


class CouponAdmin(admin.ModelAdmin):
    list_editable = ["available"]
    list_display = ["coupon", "percentage", "available"]


class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ["user", "subject"]


class CartOrderProductsAdmin(admin.ModelAdmin):
    ...


admin.site.register(Product, ProductAdmin)
admin.site.register(MainCategory, MainCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderProduct, CartOrderProductsAdmin)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductsAdmin)

admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(WishList, wishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(BigBanner)
admin.site.register(Insurance)
admin.site.register(Advices)
admin.site.register(Doctor)
admin.site.register(Locations)
admin.site.register(SpecialTimeOffer)
admin.site.register(CartOrder)
admin.site.register(Shipping)
admin.site.register(Bank)
admin.site.register(AboutUs)
admin.site.register(ProductType)
