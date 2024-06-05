from django.urls import path, include  # Import include module
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("collections", views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

urlpatterns = [
    path("", include(router.urls)),  # Include router URLs
    path("", include(products_router.urls)),  # Include products_router URLs
]
