from rest_framework import serializers
from .models import CustomUser, Sprint, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'display_name', 'first_name', 'last_name']

class SprintSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Sprint
        fields = ['id', 'title', 'user']
        read_only_fields = ['user']
        
    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to create sprints")
        validated_data['user'] = user
        return super().create(validated_data)

class TaskSerializer(serializers.ModelSerializer):
    subtasks = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)  

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('user',)  # user нельзя будет менять через API 

    def get_subtasks(self, obj):
        subtasks = obj.subtasks.all()
        return TaskSerializer(subtasks, many=True).data

    def create(self, validated_data):
        user = self.context['request'].user # достаем пользователя из контекста запроса
        
        # Проверяем, что пользователь аутентифицирован
        if not user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to create tasks")
        
        validated_data['user'] = user
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Запрет изменения пользователя при обновлении
        if 'user' in validated_data:
            del validated_data['user']
        return super().update(instance, validated_data)


#==== Для сохранения Фамилии и имени при регистрации ====================================
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    display_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'display_name': self.validated_data.get('display_name', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', '')
        })
        return data

    def save(self, request):
        user = super().save(request)
        user.display_name = self.validated_data.get('display_name', '')
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save()
        return user

#================================================================================