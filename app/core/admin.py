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
