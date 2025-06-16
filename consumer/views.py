from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from farmer.models import Product, FarmerDetails
from django.http import JsonResponse
from django.template.loader import render_to_string
from consumer.models import Cart, Reviews
from django.db.models import Q
from django.views.generic import View
from django.urls import reverse
from django.http import HttpResponseBadRequest

class ConsumerDashboardView(LoginRequiredMixin, View):
    template_name = 'consumer/consumer_dashboard.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_home'] = True 
        return context
    
    def post(self, request):
        query = request.POST.get('query')
        results = Product.objects.filter(Q(product_name__icontains=query) | Q(category__icontains=query))
        context = {
            "results": results,
        }
        return render(request, self.template_name, context)
    
class ProductComparisonView(LoginRequiredMixin, View):
    template_name = 'consumer/comparison_table.html'
    partial_template = 'consumer/comparison_table_partial.html'

    def get_queryset(self):
        products = Product.objects.select_related('user')
        category_filter = self.request.GET.get('category')
        sort_by = self.request.GET.get('sort')

        if category_filter:
            products = products.filter(category__iexact=category_filter)

        if sort_by == 'price_low_high':
            products = products.order_by('price')
        elif sort_by == 'price_high_low':
            products = products.order_by('-price')

        return products
    
    def get_context_data(self, products):
        farmers = FarmerDetails.objects.filter(
            user_id__in=products.values('user_id')
        ).select_related('user')

        farm_map = {farmer.user_id: farmer.farm_name for farmer in farmers}

        for product in products:
            product.farm_name = farm_map.get(product.user_id, 'Unknown Farm')

        return {
            'products': products,
            'categories': Product.objects.values_list('category', flat=True)
                                    .distinct()
                                    .order_by('category'),
            'selected_category': self.request.GET.get('category'),
            'selected_sort': self.request.GET.get('sort'),
        }

    def get(self, request):
        products = self.get_queryset()
        context = self.get_context_data(products)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string(self.partial_template, context, request)
            return JsonResponse({'table_html': html})

        return render(request, self.template_name, context)

class CategoryProductsView(LoginRequiredMixin, View):
    template_name = 'consumer/category_products.html'
    
    def get(self, request, category):
        products = Product.objects.filter(category__iexact=category)
        product_data = []
        
        for product in products:
            reviews = [
                {
                    'user': review.user.username,
                    'review': review.review,
                }
                for review in product.reviews_set.all()
            ]
            user = product.user
            
        for product in products:
            product_data.append({
                "id": product.id,
                "product_name": product.product_name,
                "posted_by": user.username,
                "description": product.description,
                "price": product.price,
                "image": product.product_image.url if product.product_image else None,
                "certification_image": product.certification.url if product.certification else None,
                "farm_name": product.user.farmerdetails.farm_name if hasattr(product.user, 'farmerdetails') else "Unknown Farm",
                "latitude": product.user.userprofile.latitude if hasattr(product.user, 'userprofile') and product.user.userprofile.latitude else None,
                "longitude": product.user.userprofile.longitude if hasattr(product.user, 'userprofile') and product.user.userprofile.longitude else None,
                "reviews": reviews,
            })


        context = {
            'category': category,
            'products': product_data,
        }
        return render(request, self.template_name, context)
    
class AddToCartView(LoginRequiredMixin, View):

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        Cart.objects.get_or_create(user=request.user, product=product, defaults={'address': None, 'number': None})
        return redirect(request.POST.get('next', 'consumer_dashboard'))

class UpdateQuantityView(LoginRequiredMixin, View):     
    def post(self, request, cart_id):
        cart = get_object_or_404(Cart, id=cart_id, user=request.user)

        if 'increment' in request.POST:
            cart.quantity += 1
        elif 'decrement' in request.POST:
            if cart.quantity > 1:
                cart.quantity -= 1
            else:
                return HttpResponseBadRequest("Quantity cannot be less than 1.")
        else:
            return HttpResponseBadRequest("Invalid action.")

        cart.save()
        return redirect('show-cart')
            
class UpdateCartAddressView(LoginRequiredMixin, View):
    def post(self, request):
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')

        Cart.objects.filter(user=request.user).update(
            address=address,
            number=phone_number
        )

        return redirect('consumer_dashboard')
    
class ShowCartView(LoginRequiredMixin, View):
    template_name = 'consumer/show_cart.html'
    
    def get(self, request):
        cart_items = Cart.objects.filter(
            user=request.user,
            address__isnull=True,
            number__isnull=True
        ).select_related('product')
        
        total = sum(item.product.price * item.quantity for item in cart_items)
        remaining_amount = max(25 - total, 0)
        
        context = {
            'cart_items': cart_items,
            'total': total,
            'remaining_amount': remaining_amount,
        }
        return render(request, self.template_name, context)
    
# class ShowCartView(LoginRequiredMixin, View):
#     template_name = 'consumer/show_cart.html'
    
#     def get(self, request):
#         cart_items = Cart.objects.filter(user=request.user).select_related('product')
#         total = sum(item.product.price for item in cart_items)
#         remaining_amount = max(25 - total, 0)
        
#         context = {
#             'cart_items': cart_items,
#             'total': total,
#             'remaining_amount': remaining_amount,
#         }
#         return render(request, self.template_name, context)
    
class RemoveProductView(LoginRequiredMixin, View):
    
    def get(self, request):
        return render(request, 'show_cart.html')
    
    def post(self, request, cart_item_id): 
        cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
        cart_item.delete()
        return redirect('show-cart')
    
class ReviewsViews(LoginRequiredMixin, View):
    
    def post(self, request, product_id):
        user = request.user
        product = get_object_or_404(Product, id=product_id)
        review = request.POST.get('review')
        
        Reviews.objects.create(
            user = user,
            product = product,
            review = review,
        )

        return redirect(request.POST.get('next', reverse('category-products', args=[product.category])))
        