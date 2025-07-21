from rest_framework import viewsets
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('ordering')
    serializer_class = CategorySerializer
    filterset_fields = ['is_homepage', 'status', 'layout']  # tương đương list_filter
    search_fields = ['name']  # tương đương search_fields

    # class Media:
    #     js = ('my_admin/js/jquery-3.6.0.min.js', 'my_admin/js/slugify.min.js', 'my_admin/js/general.js')