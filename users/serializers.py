from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User

class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'telefono', 'is_active', 'is_staff']
        read_only_fields = fields

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, trim_whitespace=False, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'telefono', 'password', 'is_active', 'is_staff']
        read_only_fields = ['id']

    def validate_email(self, value):
        value = value.strip().lower()
        others = User.objects.filter(email__iexact=value)
        if self.instance:
            others = others.exclude(pk=self.instance.pk)
        if others.exists():
            raise serializers.ValidationError('Este correo ya esta registrado.')
        return value

    def validate(self, attrs):
        if self.instance is None and 'password' not in attrs:
            raise serializers.ValidationError({'password': 'La contrasena es obligatoria al crear.'})
        if 'password' in attrs:
            candidate = User(username=attrs.get('username', getattr(self.instance, 'username', '')),
                             email=attrs.get('email', getattr(self.instance, 'email', '')))
            try:
                validate_password(attrs['password'], candidate)
            except ValidationError as error:
                raise serializers.ValidationError({'password': error.messages})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        # Si no se envia password, el hash original permanece intacto.
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
