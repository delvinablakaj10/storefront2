from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from . import views
from .models import Product, Collection, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from rest_framework import status
from django.db.models import Count
from pprint import pprint


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['collection_id']
    # pagination_class = PageNumberPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']


    def get_serializer_context(self):
        return {"request": self.request}

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response(
                {
                    "error": "Product cannot be deleted because it is associated with an order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # def get_queryset(self):
#     #     return Product.objects.select_related('collection').all()

#     # def get_serializer_class(self):
#     #     return ProductSerializer

#     def get_serializer_context(self):
#         return {'request': self.request}
#     # def get(self, request):
#     #     queryset = Product.objects.select_related('collection').all()
#     #     serializer = ProductSerializer(queryset, many=True, context={'request': request})
#     #     return Response(serializer.data)

#     # def post(self, request):
#     #     serializer = ProductSerializer(data = request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# class ProductDetail(APIView):
#     # def get(self, request, id):
#     #     queryset = get_object_or_404(Product, pk=id)
#     #     serializer_class = ProductSerializer(queryset)
#     #     return Response(serializer_.data)

#     def post(self, request, id):
#         serializer = ProductSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetail(RetrieveUpdateDestroyAPIView):

    # lookup_field = 'id'

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response(
                {
                    "error": "Product cannot be deleted because it is associated with an order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()  # This line saves the model instance with updated data
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        if product.orderitems.count() > 0:
            return Response(
                {
                    "error": "Product cannot be deleted because it is associated with an order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view()
# def collection_detail(request, pk):
#     return Response('ok')
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {"request": self.request}


# @api_view(['GET', 'POST'])
# def collection_list(request):

#     if request.method == 'GET':
#         collections = Collection.objects.annotate(products_count=Count('products')).all()
#         serializer = CollectionSerializer(collections, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count("products"))
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response(
                {
                    "error": "Collection cannot be deleted because it is associated with an order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "PUT", "DELETE"])
def collection_detail(request, id):
    collection = get_object_or_404(Collection, pk=id)
    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CollectionSerializer(collection, data=request.data)
        if serializer.is_valid():
            serializer.save()  # This line saves the model instance with updated data
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        if collection.products.count() > 0:
            return Response(
                {
                    "error": "Collection cannot be deleted because it is associated with an order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()

    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response(
                {
                    "error": "Collection cannot be deleted because it is associated with an order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}
