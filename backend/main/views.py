from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm 


from .models import Task, Sprint, CustomUser  
from .serializers import TaskSerializer, SprintSerializer
from .forms import CustomUserCreationForm

from django.contrib.auth.forms import AuthenticationForm 

#для REST
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

# для REST API, React 
from rest_framework import viewsets
from .models import Sprint, Task
from .serializers import SprintSerializer, TaskSerializer

class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer

    permission_classes = [permissions.IsAuthenticated] #для проверки прав доступа

    def get_queryset(self):
        return Sprint.objects.filter(user=self.request.user) # для вывода спринта по конкретному пользователю

    def perform_create(self, serializer): # чтобы поле user устанавливается как текущий пользователь
            serializer.save(user=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    # Только для родительских задач может не быть задана родительская задача
    queryset = Task.objects.filter(parent_task__isnull=True)  
    serializer_class = TaskSerializer

    permission_classes = [permissions.IsAuthenticated] #для проверки прав доступа

    def get_queryset(self):
        # Фильтрация задач по пользователю и спринту
        queryset = Task.objects.filter(
            user=self.request.user,
            parent_task__isnull=True
        )
        sprint_id = self.request.query_params.get('sprint')
        if sprint_id:
            queryset = queryset.filter(sprint_id=sprint_id)
        return queryset

    def perform_create(self, serializer):
        # Автоматически привязывает задачу к текущему пользователю
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # Запрет изменения владельца задачи
        
        if 'user' in serializer.validated_data:
            raise PermissionDenied("Нельзя изменять владельца задачи")
        serializer.save()


