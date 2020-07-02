
from core.businesses.views import (BusinessOrganizationView,
                                   BusinessPictureViewSet,
                                   BusinessProductViewSet,
                                   OrganizationDetailView,
                                   OrganizationListView, ProductDetailView,
                                   ProductListView, ReviewDetailView,
                                   ReviewListView)
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('business/organizations', BusinessOrganizationViewSet,
#                 basename='business-organization')
router.register('business/products', BusinessProductViewSet,
                basename='business-product')
router.register('business/pictures', BusinessPictureViewSet,
                basename='business-picture')
urlpatterns = router.urls


urlpatterns += [
    path('business/organizations/', BusinessOrganizationView.as_view(),
         name='business-organizations'),
    path('organizations/', OrganizationListView.as_view(),
         name='organization-list'),
    path('organizations/<int:pk>/', OrganizationDetailView.as_view(),
         name='organization-details'),
    path('products/', ProductListView.as_view(),
         name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(),
         name='product-details'),
    path('reviews/', ReviewListView.as_view(),
         name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(),
         name='review-details'),
]
