from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField



LABEL_CHOICE = (
    ('p','primary'),
    ('s','secondary'),
    ('d','danger'),
)
ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse("core:category",kwargs={
            'slug':self.slug
        })

    def __str__(self):
        return self.title

class Brand(models.Model):
    brand_name = models.CharField(max_length=200)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse("core:category", kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return self.brand_name

class Item(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True,blank=True)
    label = models.CharField(choices=LABEL_CHOICE,max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product",kwargs={
            'slug':self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_increase_to_cart_url(self):
        return reverse("core:increase_the_cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class Variation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  # size

    class Meta:
        unique_together = (
            ('item', 'name')
        )

    def __str__(self):
        return self.name

class ItemVariation(models.Model):
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)  # S, M, L
    attachment = models.ImageField(blank=True)

    class Meta:
        unique_together = (
            ('variation', 'value')
        )

    def __str__(self):
        return self.value

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    item_variations = models.ManyToManyField(ItemVariation)

    def __str__(self):
        return f"{self.qty} of {self.item.title}"

    def get_total_price(self):
        return self.qty * self.item.price

    def get_total_discount_price(self):
        return self.qty * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_price() - self.get_total_discount_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        else:
            return self.get_total_price()

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=200)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    shipping_address = models.ForeignKey('Address',related_name="shipping_address",on_delete=models.SET_NULL,blank=True,null=True)
    billing_address = models.ForeignKey('Address',related_name="billing_address",on_delete=models.SET_NULL,blank=True,null=True)
    payment = models.ForeignKey('Payment',on_delete=models.SET_NULL,blank=True,null=True)
    ordered = models.BooleanField(default=False)
    coupon = models.ForeignKey('Coupon',on_delete=models.SET_NULL,blank=True,null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1,choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    txn_id = models.CharField(max_length=400)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,blank=True,null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code = models.CharField(max_length=20)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    reason= models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    def __str__(self):
        return f"{self.pk}"

