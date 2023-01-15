from rest_framework import serializers

from core.accounts.models.account_owners import AccountOwner


class GoogleSignUpSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=100, min_length=6)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = AccountOwner
        fields = ('id', 'username', 'email', 'password', 'is_staff',
                  'is_active', 'created_at')

    def validate_email(self, value):
        if AccountOwner.objects.filter(email=value).exists():
            raise serializers.ValidationError('The email is already taken.')
        return value

    def create(self, validated_data):
        return AccountOwner.objects.create_user(**validated_data)


class AccountOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountOwner
        fields = ('id', 'username', 'email', 'is_staff', 'is_active',
                  'created_at')


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountOwner
        fields = ('id', 'username', 'email', 'is_staff', 'is_active',
                  'created_at')


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountOwner
        fields = ('id', 'username', 'email', 'is_staff', 'is_active',
                  'created_at')