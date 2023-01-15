from django.contrib.auth import get_user_model
from rest_framework import permissions, status, views, generics
from rest_framework.response import Response

from core.accounts.serializers.account_owners import AccountOwnerSerializer, UserDetailSerializer, UserListSerializer

User = get_user_model()


class AccountOwnerView(views.APIView):

    serializer_class = AccountOwnerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.request.query_params.get("username")
        users = User.objects.filter(username__icontains=username)
        return users


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]