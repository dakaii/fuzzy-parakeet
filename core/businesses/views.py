from core.accounts.permissions import IsBusinessOwner, IsGeneralUser
from core.businesses.models import (Organization, OrgBrowsingHstry,
                                    Product, Rating, Review)
from core.businesses.serializers import (FavoriteListSerializer,
                                         FavoriteSerializer,
                                         OrgBrowsingHstrySerializer,
                                         OrganizationDetailSerializer,
                                         OrganizationImageSerializer,
                                         OrganizationSerializer,
                                         ProductSerializer,
                                         RatingListSerializer,
                                         RatingSerializer, ReviewSerializer)
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response


class FavoriteOrganizationView(views.APIView):
    permission_classes = [IsGeneralUser]

    def post(self, request, *args, **kwargs):
        serializer = FavoriteSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        serializer = FavoriteListSerializer(request.user)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        org_pk = self.request.data['organization_id']
        try:
            user.favorites.remove(org_pk)
        except Organization.DoesNotExist as e:
            raise NotFound(detail={'message': str(e)})
        return Response(
            data={
                'message': f'org: {org_pk} was removed from the favorite list'
            }, status=status.HTTP_204_NO_CONTENT)


class BusinessOrganizationView(views.APIView):
    permission_classes = [IsBusinessOwner]
    serializer_class = OrganizationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        instance = self._get_org(request.user)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self._get_org(request.user)
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):
        instance = self._get_org(request.user)
        instance.delete()
        return Response(
            data={'message': 'deleted'}, status=status.HTTP_204_NO_CONTENT)

    def _get_org(self, user):
        try:
            return user.organization
        except Organization.DoesNotExist as e:
            raise NotFound(detail={'message': str(e)})


class OrganizationFilterView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        keyword = self.request.GET.get('keyword', '')
        if keyword:
            return Organization.objects.filter(
                Q(name__icontains=keyword) |
                Q(location__state__icontains=keyword) |
                Q(location__city__icontains=keyword))
        return Organization.objects.all()


class OrganizationListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class OrganizationDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Organization.objects.all()
    serializer_class = OrganizationDetailSerializer


class BusinessProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsBusinessOwner]
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            organization = user.organization
        except Organization.DoesNotExist as e:
            raise NotFound(detail={'message': str(e)})
        return organization.products.all()

    def list(self, request):
        # TODO delete this. this is unnecessary.
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            request.data['organization'] = request.user.organization.pk
        except Organization.DoesNotExist as e:
            raise NotFound(detail={'message': str(e)})
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        # TODO delete this. this is unnecessary.
        queryset = self.get_queryset()
        product = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(product)
        return Response(serializer.data)


class ProductListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrganizationProductsListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self, pk):
        try:
            organization = Organization.objects.get(pk=pk)
        except Organization.DoesNotExist as e:
            raise NotFound(detail={'message': str(e)})
        return organization.products.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset(kwargs['pk'])
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class RateOrganizationView(views.APIView):
    permission_classes = [IsGeneralUser]
    serializer_class = RatingSerializer

    def get_queryset(self):
        return Rating.objects.filter(person=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = RatingSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        serializer = RatingListSerializer(
            request.user, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        org_pk = self.request.data['organization_id']
        try:
            user.rated_organizations.remove(org_pk)
        except Organization.DoesNotExist as e:
            raise NotFound(detail={'message': str(e)})
        return Response(
            data={
                'message': f'org: {org_pk} was removed from the rate list'
            }, status=status.HTTP_204_NO_CONTENT)


class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsGeneralUser]

    def get_queryset(self):
        user = self.request.user
        return user.reviews.all()

    def create(self, request):
        request.data['author'] = request.user.pk
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsGeneralUser]

    def get_queryset(self):
        user = self.request.user
        return user.reviews.all()


class OrgBrowsingHstryListView(generics.ListCreateAPIView):
    queryset = OrgBrowsingHstry.objects.all()
    serializer_class = OrgBrowsingHstrySerializer
    permission_classes = [IsGeneralUser]

    def get_queryset(self):
        user = self.request.user
        return user.org_browsing_hstry.order_by('-created_at')

    def create(self, request):
        request.data['user'] = request.user.pk
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrganizationImageView(generics.ListCreateAPIView):
    serializer_class = OrganizationImageSerializer
    permission_classes = [IsBusinessOwner]

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
