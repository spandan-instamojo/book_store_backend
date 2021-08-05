from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import StoreUser, HintQuestion
from .helpers import JWTAuthenticationGenerator


class HintSerializer(serializers.ModelSerializer):
    class Meta:
        model = HintQuestion
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreUser
        exclude = ('is_authenticated', 'is_active', 'is_superuser', 'created', 'modified')

    def validate(self, attrs):
        username = attrs['username']
        email = attrs['email']
        home_phone = attrs['home_phone']
        if StoreUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists')
        if StoreUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Account with email already exists')

        attrs['readable_password'] = attrs['password']
        attrs['password'] = make_password(attrs['password'])

        return attrs

    def save(self, **kwargs):
        self.validated_data.pop('readable_password', None)
        return super(RegistrationSerializer, self).save(**kwargs)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(max_length=100, required=True, allow_null=False, allow_blank=False)

    def validate(self, attrs):
        username = attrs['username']
        if not StoreUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('Given username does not exist')
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, required=True, allow_null=False, allow_blank=False)
    hq_id = serializers.IntegerField(allow_null=False, required=True)
    hint_answer = serializers.CharField(max_length=30, required=True, allow_null=False, allow_blank=False)
    new_password = serializers.CharField(max_length=100, required=True, allow_null=False, allow_blank=False)

    def validate(self, attrs):
        username = attrs['username']
        hq_id = attrs['hq_id']
        hint_answer = attrs['hint_answer']
        try:
            user = StoreUser.objects.get(username=username)
        except StoreUser.DoesNotExist:
            raise serializers.ValidationError('Username does not exist')
        else:
            if user.hint_question.id == hq_id:
                if user.hint_answer != hint_answer:
                    raise serializers.ValidationError('Incorrect Answer')
                else:
                    attrs['readable_password'] = attrs['new_password']
                    attrs['password'] = make_password(attrs['new_password'])
            else:
                raise serializers.ValidationError('Invalid user/hint-question')

        return attrs
