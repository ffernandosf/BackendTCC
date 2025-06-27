from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para ler e atualizar dados de usuários.
    A senha é opcional na atualização (write_only).
    """
    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        """
        Atualiza o usuário, tratando a senha separadamente se ela for fornecida.
        """
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer usado especificamente para criar novos usuários.
    Garante que o campo de senha seja obrigatório e tratado corretamente.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
    
    def create(self, validated_data):
        """
        Cria um novo usuário usando o método create_user para hashear a senha.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
