from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'is_staff', 'is_superuser', 'first_name', 'last_name')
        read_only_fields = ('id', 'is_staff', 'is_superuser')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = self.validated_data.pop('password')

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user