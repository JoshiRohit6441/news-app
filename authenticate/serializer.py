from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def save(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data['first_name'],
            last_name=validated_data["last_name"],
            is_admin=False,
            is_active=False
        )

        password = validated_data['password']
        password2 = validated_data['password2']

        if password != password2:
            raise serializers.ValidationError("password did not match")

        user.set_password(password)
        user.save()
        user.verification_otp = generate_otp()
        return user


def generate_otp():
    return 123456


class UserUpdateserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "profile_pic")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
