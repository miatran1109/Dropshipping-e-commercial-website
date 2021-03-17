from .views import SearchResultsView

urlpatterns = [ 
    path('search', SearchResultsView.as_view(), name='search_results'),
]