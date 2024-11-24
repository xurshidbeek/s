from django.views.generic import ListView, DeleteView, TemplateView, DetailView, UpdateView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages


from .models import Category, Product,Cart
User = get_user_model()


class CustomRangeForPagination:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        page_obj = context['page_obj']
        left_index = page_obj.number - 1
        right_index = page_obj.number + 1

        if left_index < 1:
            left_index = 1

        if right_index > page_obj.paginator.num_pages:
            right_index = page_obj.paginator.num_pages

        custom_range = range(left_index, right_index + 1)
        context['custom_range'] = custom_range
        return context


class AccountView(TemplateView):
    model = User
    template_name = 'app_main/user_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = kwargs.get('user_id')
        context['user'] = User.objects.get(id=user_id)
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'app_main/category.html'
    context_object_name = 'categories'

class ProductListView(ListView):
    model = Product
    template_name = 'app_main/home.html'
    context_object_name = 'products'
    paginate_by = 6
    extra_context = {"is_home": True}

    def get_queryset(self):
        search_term = self.request.GET.get("search", "")
        if search_term:
            return Product.objects.filter(
                title__icontains=search_term
            ).order_by("-id")
        else:
            return Product.objects.all().order_by("-id")

class CategoryDetailView(ListView):
    model = Product
    template_name = "app_main/category_detail.html"
    context_object_name = "products"
    def get_queryset(self):
        category_id = self.kwargs.get("id")
        category = get_object_or_404(Category, id=category_id)
        return Product.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("id")
        category = get_object_or_404(Category, id=category_id)
        context["category"] = category
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "app_main/product.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        product_id = self.kwargs.get("id")
        return get_object_or_404(Product, id=product_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.exclude(id=self.object.id)[:4]
        return context


class CartListView(ListView):
    model = Cart
    template_name = 'app_main/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        # Get all the cart items for the logged-in user
        return Cart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = sum(cart_item.total_price for cart_item in context['cart_items'])  # Calculate total price
        context['total_price'] = total
        return context


class AddToCartView(LoginRequiredMixin, View):
    login_url = "login"

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get("quantity", 1))

        # Check product stock
        if product.stock < quantity:
            messages.error(request, f"{product.name} Tugadi!")
            return redirect(request.META.get("HTTP_REFERER", "home"))

        try:
            # Add product to cart
            cart_item, created = Cart.objects.get_or_create(
                user=request.user, product=product, defaults={"quantity": quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            messages.success(request, f"{product.name}  Added cart")
        except Exception as e:
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")

        return redirect(request.META.get("HTTP_REFERER", "home"))




class CartProductDelete(LoginRequiredMixin, DeleteView):
    model = Cart
    success_url = reverse_lazy("cart")
    pk_url_kwarg = "cart_product_id"


class IncrementView(LoginRequiredMixin, View):
    def post(self, request, cart_id):
        cart = get_object_or_404(Cart, id=cart_id)

        # Check if the desired quantity exceeds stock
        if cart.quantity + 1 > cart.product.stock:
            messages.error(request, "Not enough stock available.")
            return redirect("cart")

        # If stock is sufficient, increment the quantity
        cart.quantity += 1
        cart.save()

        return redirect("cart")

class DecrementView(LoginRequiredMixin, View):
    def post(self, request, cart_id):
        cart = get_object_or_404(Cart, id=cart_id)
        if cart.quantity > 1:
            cart.quantity -= 1
        cart.save()
        return redirect("cart")
