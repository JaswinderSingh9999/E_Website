from django.contrib import admin
from .models import Register, Order, Product, Course, Teacher,FAQ,ContactInfo, ContactMessage
from .models import Newsletter, Footer, FooterContact
from django.utils.html import format_html
from django.urls import reverse


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'country')
    search_fields = ('username', 'email')
    list_filter = ('country',)
    ordering = ('-id',)
    list_per_page = 5


# COMMON DELETE BUTTON FUNCTION (reuse)
def get_delete_button(obj):
    url = reverse(
        'admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name),
        args=[obj.id]
    )
    return format_html(
        '<a style="background:red; color:white; padding:5px 10px; border-radius:5px;" href="{}">Delete</a>',
        url
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'pr_name', 'pr_price', 'delete_button')
    

    def delete_button(self, obj):
        return get_delete_button(obj)

    delete_button.short_description = "Delete"



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'co_title', 'co_details', 'delete_button')

    def delete_button(self, obj):
        return get_delete_button(obj)

    delete_button.short_description = "Delete"


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'designation', 'delete_button')

    def delete_button(self, obj):
        return get_delete_button(obj)

    delete_button.short_description = "Delete"

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'question',"answer",'delete_button')
    ordering = ('-id',)
    def delete_button(self, obj):
        return get_delete_button(obj)

    delete_button.short_description = "Delete"

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('id','email','phone','address',"delete_button")
    ordering = ('-id',)
    def delete_button(self,obj):
        return get_delete_button(obj)
    delete_button.short_description = "Delete"

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','message', 'email', 'created_at',"delete_button")
    def delete_button(self, obj):
        return get_delete_button(obj)

    delete_button.short_description = "Delete"

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'created_at',"delete_button")
    def delete_button(self, obj):
        return get_delete_button(obj)

    delete_button.short_description = "Delete"


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ('id',"delete_button")
    def delete_button(self, obj):
        return get_delete_button(obj)

    delete_button.short_description = "Delete"


@admin.register(FooterContact)
class FooterContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone',"delete_button")
    def delete_button(self, obj):
        return get_delete_button(obj)

    delete_button.short_description = "Delete"

from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# ✅ DELETE BUTTON FUNCTION
def get_delete_button(obj):
    return format_html(
        '<a class="button" style="color:red;" href="{}">Delete</a>',
        reverse('admin:{}_{}_delete'.format(obj._meta.app_label, obj._meta.model_name), args=[obj.id])
    )


# ✅ ORDER ITEM INLINE (Inside Order)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'price', 'quantity']


# ✅ ORDER ADMIN
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'customer_name',
        'total_amount',
        'created_at',
        'get_products',
        'delete_button'
    )

    search_fields = ('order_id', 'customer_name')
    list_filter = ('created_at',)
    inlines = [OrderItemInline]

    # ✅ Show product names + quantity
    def get_products(self, obj):
        return ", ".join([
            f"{item.product_name} ({item.quantity})"
            for item in obj.items.all()
        ])
    get_products.short_description = "Products"

    # ✅ Delete button
    def delete_button(self, obj):
        return get_delete_button(obj)
    delete_button.short_description = "Delete"
