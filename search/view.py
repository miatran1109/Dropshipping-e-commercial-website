from django.views.generic import ListView
from django.db.models import Q


class SearchResultsView(ListView):
    model = Product
    template_name = 'mainpage/search-product.html'
     context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('search')
        products=Product.objects.filter(Q(name__icontains=query))
        return products