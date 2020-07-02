from core.accounts.permissions import IsBusinessOwner, IsGeneralUser
from core.businesses.models import Organization, Picture, Product, Review
from core.businesses.serializers import (OrganizationDetailSerializer,
                                         PictureSerializer, ProductSerializer,
                                         ReviewSerializer)
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .serializers import OrganizationSerializer

# class BusinessOrganizationViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsBusinessOwner]
#     serializer_class = OrganizationSerializer

#     def get_queryset(self):
#         user = self.request.user
#         try:
#             return [user.organization]
#         except Organization.DoesNotExist as e:
#             raise NotFound(detail={'message': str(e)})


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


class OrganizationListView(generics.ListAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsGeneralUser]


class OrganizationDetailView(generics.RetrieveAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationDetailSerializer
    permission_classes = [IsGeneralUser]


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
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsGeneralUser]


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsGeneralUser]


class BusinessPictureViewSet(viewsets.ModelViewSet):
    permission_classes = [IsBusinessOwner]
    serializer_class = PictureSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            organization = user.organization
        except Organization.DoesNotExist as e:
            raise NotFound(detail={'message': str(e)})

        product_id_list = organization.products.values_list('pk', flat=True)
        return Picture.objects.filter(product_id__in=product_id_list)

    def create(self, request):
        # TODO uploda the incoming pics to the could here.
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PictureListView(generics.ListAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    permission_classes = [IsGeneralUser]


class PictureDetailView(generics.RetrieveAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    permission_classes = [IsGeneralUser]


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
