from django.contrib import admin

# Register your models here.
from .models import *

def make_refund_accepted(modelAdmin,request,queryset):
    queryset.update(refund_requested=False,refund_granted=True)


make_refund_accepted.short_description = "Update Order to Refund Granted"

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','ordered','being_delivered','received','refund_requested','refund_granted','user','shipping_address','billing_address','payment','coupon']
    list_display_links = ['user','billing_address','shipping_address','payment','coupon']
    list_filter = ['ordered','being_delivered','received','refund_requested','refund_granted']

    search_fields = ['user__username','ref_code']
    actions = [make_refund_accepted]

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','street_address','apartment_address','country','zip','address_type','default']

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address,AddressAdmin)
admin.site.register(Order,OrderAdmin)