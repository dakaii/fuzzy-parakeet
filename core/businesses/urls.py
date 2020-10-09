from core.businesses.views import (BusinessOrganizationView,
                                   BusinessProductViewSet,
                                   FavoriteOrganizationView,
                                   OrganizationDetailView,
                                   OrganizationFilterView,
                                   OrgBrowsingHstryListView,
                                   OrganizationImageView, OrganizationListView,
                                   OrganizationProductsListView,
                                   ProductDetailView, ProductListView,
                                   RateOrganizationView, ReviewDetailView,
                                   ReviewListView)
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('business/products', BusinessProductViewSet,
                basename='business-product')
urlpatterns = router.urls


urlpatterns += [
    path('favorite/organizations/', FavoriteOrganizationView.as_view(),
         name='favorite-organizations'),
    path('histories/organization/', OrgBrowsingHstryListView.as_view(),
         name='org-history-list'),
    path('business/organizations/', BusinessOrganizationView.as_view(),
         name='business-organizations'),
    path('filter/organizations/', OrganizationFilterView.as_view(),
         name='organization-filter'),
    path('organization/image/', OrganizationImageView.as_view(),
         name='organization-image-list'),
    path('organizations/', OrganizationListView.as_view(),
         name='organization-list'),
    path('organizations/<int:pk>/', OrganizationDetailView.as_view(),
         name='organization-details'),
    path('organization/products/<int:pk>/',
         OrganizationProductsListView.as_view(), name='org-products-list'),
    path('products/', ProductListView.as_view(),
         name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(),
         name='product-details'),
    path('rate/organizations/', RateOrganizationView.as_view(),
         name='rate-organizations'),
    path('reviews/', ReviewListView.as_view(),
         name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(),
         name='review-details'),
]
