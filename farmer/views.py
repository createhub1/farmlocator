from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from farmer.models import Product, FarmerDetails
from myapp.models import UserProfile
from consumer.models import Reviews, Cart

class FarmerDashboardView(LoginRequiredMixin, View):
    template_name = "farmer/farmer_dashboard.html"

    def get(self, request):
        products = Product.objects.filter(user=request.user)
        context = {
            "products": products
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        product_name = request.POST.get("product_name")
        price = request.POST.get("price")
        category = request.POST.get("category")
        description = request.POST.get("description")
        product_image = request.FILES.get("product_image")
        certification = request.FILES.get("certification")
        quantity = request.POST.get("quantity")
        unit = request.POST.get("unit")
        
        Product.objects.create(
            user=user,
            product_name=product_name,
            price=price,
            category=category,
            description=description,
            product_image=product_image,
            certification=certification,
            quantity=quantity,
            unit=unit,
        )
        
        return redirect('farmer_dashboard')

@method_decorator(csrf_exempt, name='dispatch')
class UpdateProductView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id, user=request.user)
            product.product_name = request.POST.get("product_name")
            product.price = request.POST.get("price")
            product.category = request.POST.get("category")
            product.description = request.POST.get("description")
            product.quantity = request.POST.get("quantity")
            
            if 'product_image' in request.FILES:
                product.product_image = request.FILES['product_image']
            if 'certification' in request.FILES:
                product.certification = request.FILES['certification']
                
            product.save()
            return JsonResponse({'status': 'success'})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
        
class ProductListView(LoginRequiredMixin, View):
    template_name = "farmer/products.html"
    
    def get(self, request):
        products = Product.objects.filter(user=request.user).select_related('user')
        product_data = []
        for product in products:
            try:
                profile = product.user.userprofile
                product_data.append({
                    "name": product.product_name,
                    "image": product.product_image,
                    "price": product.price,
                    "category": product.category,
                    "unit": product.unit,
                    "quantity": product.quantity,
                    "latitude": profile.latitude,
                    "longitude": profile.longitude
                })
            except UserProfile.DoesNotExist:
                continue  
        
        return render(request, self.template_name, {"products": product_data})
    
class DeleteProductView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, user=request.user)
        product.delete()
        return JsonResponse({'status': 'success'})
    
class SettingsView(LoginRequiredMixin, View):
    template_name = "farmer/settings.html"
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        user = request.user
        profile_img = request.FILES.get('profile_img')
        farm_name = request.POST.get('farm_name') 

        farmer, created = FarmerDetails.objects.get_or_create(user=user)
        if profile_img:
            farmer.profile_img = profile_img
            
        if farm_name:
            farmer.farm_name = farm_name
            
        farmer.save()
            
        return render(request, self.template_name)

class ShowReviewView(LoginRequiredMixin, View):
    template_name = "farmer/show-review.html"
    
    def get(self, request):
        
        reviews = Reviews.objects.filter(
            product__user=request.user
        ).select_related(
            'product',
            'user'
        ) 

        context = {
            'reviews': reviews
        }
        return render(request, self.template_name, context)
    
class OrderView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Cart.objects.filter(
            product__user=request.user,
            address__isnull=False,
            number__isnull=False
        ).select_related('product', 'user')
        
        return render(request, 'farmer/orders.html', {'orders': orders})
