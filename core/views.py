from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.db.models import Q
from django.utils import timezone
from .forms import *
import random
import string


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'home.html'


class CategoryView(ListView):
    def get(self, *args, **kwargs):
        try:
            order = Item.objects.all()
            context = {"object":order}
        except ObjectDoesNotExist:
            messages.warning(self.request,"you do not have an active order")
            return redirect("/")
    paginate_by = 10
    template_name = 'home.html'



class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            context = {"object":order}
        except ObjectDoesNotExist:
            messages.warning(self.request,"you do not have an active order")
            return redirect("/")

        return render(self.request, 'order_summary.html',context)

    model = Order
    template_name = 'order_summary.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super(ItemDetailView, self).get_context_data(*args, **kwargs)
        context['item'] = Item.objects.exclude(slug=self.kwargs['slug'])
        return context


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True,
                'address': Address.objects.filter(user=self.request.user)
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )

            if shipping_address_qs.exists():
                context.update({'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            if self.request.method == "POST":
                save_address = self.request.POST.get("save_address",None)

                if save_address == None:
                    selected_addres = Address.objects.get(id=save_address)
                    order.address = selected_addres
                    order.save()
                    redirect("core:payment","cod")
                else:
                    if form.is_valid():
                        data = form.save(commit=False)
                        data.user = self.request.user
                        data.address_type = "S"
                        data.default = True
                        data.save()
                        order.address = data
                        order.save()
                        return redirect('core:payment',"cod")
                    else:
                        return redirect("core:checkout")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")

class PaymentView(View):
    def get(self,*args,**kwargs):
        order = Order.objects.get(user=self.request.user,ordered=False)
        if order.billing_address:
            return render(self.request,"payment.html",{
                "order": order,
                "DISPLAY_COUPON_FORM":False
            })
        else:
            messages.warning(self.request,"you have not added a billing address")
            return redirect("core:checkout")

    def post(self,*args,**kwargs):
        order = Order.objects.get(user=self.request.user,ordered=False)

        # create the payment
        payment = Payment()
        payment.txn_id = "12112212121"
        payment.user = self.request.user
        payment.amount = order.get_total()
        payment.save()

        #assign the payment to the order
        order_items = order.items.all()
        order_items.update(ordered=True)
        for item in order_items:
            item.save()

        order.ordered = True
        order.payment = payment

        #todo : assign ref code

        order.ref_code = create_ref_code()

        order.save()

        return redirect('core:homepage')


class AddToCartView(LoginRequiredMixin,View):
    def get(self,request, slug,*args,**kwargs):
        item = get_object_or_404(Item,slug=slug)

        # var is variant list
        var = []

        variant = Variation.objects.filter(item=item)
        for v in variant:
            var.append(request.GET.get(v.name,None))

        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False,
        )
        order_qs = Order.objects.filter(user=request.user,ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item.qty += 1
                order_item.save()
                messages.info(request,"this item was updated to your cart")
                return redirect("core:order-summary")
            else:
                order.items.add(order_item)
                for v in var:
                    a = ItemVariation.objects.get(value=v,variation__item__slug=item.slug)
                    order_item.item_variations.add(a)


                messages.info(request,"this item was added to your cart")
                return redirect("core:order-summary")
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user,ordered_date=ordered_date)
            order.items.add(order_item)
            messages.info(request,"this item was added to your cart")
            return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.qty > 1:
                order_item.qty -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


def get_coupon(request,code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request,"this coupon does not exist")
        return redirect("core:checkout")

def check_coupon(request,code):
    try:
        coupon = Coupon.objects.get(code=code)
        return True
    except ObjectDoesNotExist:
        return False


class AddCouponView(View):
    def post(self,*args,**kwargs):
        if self.request.method == "POST":
            form = CouponForm(self.request.POST or None)
            if form.is_valid():
                try:
                    code = form.cleaned_data.get("code")
                    if check_coupon(self.request,code):
                        order = Order.objects.get(user=self.request.user, ordered=False)
                        order.coupon = get_coupon(self.request,code)
                        order.save()
                        messages.success(self.request, "Successfully added coupon")
                        return redirect("core:checkout")
                    else:
                        messages.success(self.request, "Invalid coupon Try Again")
                        return redirect("core:checkout")

                except ObjectDoesNotExist:
                    messages.info(self.request,"you do not have an active order")
                    return redirect("core:checkout")



class RequestFundView(View):
    def get(self,*args,**kwargs):
        form = RefundForm()
        context = {
            "form":form
        }
        return render(self.request,"request_refund.html",context)

    def post(self,*args,**kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                #edit the order
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "this Request was recieved ")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request,"this order don't exist")
                return redirect("core:request-refund")

