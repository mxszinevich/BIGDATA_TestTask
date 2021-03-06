import datetime

import pytest
from django.core.files.base import ContentFile
from django.urls import reverse
from rest_framework import status

from tasks.models import Task
from tests.tests_tasks.factories import TaskFactory, TaskFileFactory
from tests.tests_users.user_factory import UserFactory


class TestTaskViewSet:
    """
    Тестирование API задач
    """

    @pytest.mark.django_db
    def test_action_create_without_file(self, api_client):
        """
        Тестирование создания задачи без файла
        """

        user = UserFactory()
        task_data = {
            "title": "Задача",
            "description": "Описание задачи",
            "completion_date": datetime.datetime.now().date().isoformat(),
            "user": user.id,
        }

        url = reverse("tasks-list")
        response = api_client.post(url, data=task_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        api_client.force_authenticate(user=user)
        response = api_client.post(url, data=task_data)
        assert response.status_code == status.HTTP_201_CREATED
        task = Task.objects.first()
        assert task.title == task_data["title"]
        assert task.description == task_data["description"]
        assert task.completion_date == datetime.datetime.now().date()
        assert task.user == user
        assert task.files.count() == 0

    @pytest.mark.django_db
    def test_action_create_one_file(self, api_client):
        """
        Тестирование создания задачи с 1 файлом
        """

        user = UserFactory()
        task_data = {
            "title": "Задача",
            "description": "Описание задачи",
            "completion_date": datetime.datetime.now().date().isoformat(),
            "user": user.id,
            "files": ContentFile("content_file", "test.png"),
        }

        api_client.force_authenticate(user=user)
        url = reverse("tasks-list")
        response = api_client.post(url, data=task_data)
        assert response.status_code == status.HTTP_201_CREATED
        task = Task.objects.first()
        assert task.title == task_data["title"]
        assert task.description == task_data["description"]
        assert task.completion_date == datetime.datetime.now().date()
        assert task.user == user
        assert task.files.count() == 1

    @pytest.mark.django_db
    def test_action_create_multiple_file(self, api_client):
        """
        Тестирование создания задачи с несколькими файлами
        """

        user = UserFactory()
        count_files = 5
        task_data = {
            "title": "Задача",
            "description": "Описание задачи",
            "completion_date": datetime.datetime.now().date().isoformat(),
            "user": user.id,
            "files": [
                ContentFile("content_file", f"test{i}.png") for i in range(count_files)
            ],
        }

        api_client.force_authenticate(user=user)
        url = reverse("tasks-list")
        response = api_client.post(url, data=task_data)
        assert response.status_code == status.HTTP_201_CREATED
        task = Task.objects.first()
        assert task.title == task_data["title"]
        assert task.description == task_data["description"]
        assert task.completion_date == datetime.datetime.now().date()
        assert task.user == user
        assert task.files.count() == count_files

    @pytest.mark.django_db
    def test_action_task_list(self, api_client, django_assert_num_queries):
        """
        Тестирование просмотра задач
        """

        user1 = UserFactory()
        user2 = UserFactory()
        count_related_objects_user1 = 3
        count_related_objects_user2 = 1
        taks_user_1 = []

        for i in range(count_related_objects_user1):
            task1 = TaskFactory(user=user1)
            taks_user_1.append(task1)
            task_file = TaskFileFactory(task=task1)

        taks_user_2 = []
        for i in range(count_related_objects_user2):
            task2 = TaskFactory(user=user2)
            taks_user_2.append(task2)
            task_file = TaskFileFactory(task=task2)

        api_client.force_authenticate(user=user1)
        url = reverse("tasks-list")
        with django_assert_num_queries(3):
            response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        res_json = response.json()
        assert res_json["count"] == count_related_objects_user1
        assert res_json["results"][0]["id"] == taks_user_1[0].id
        assert res_json["results"][0]["title"] == taks_user_1[0].title
        assert res_json["results"][0]["description"] == taks_user_1[0].description
        for task in res_json["results"]:
            assert task["user"] == user1.id

        api_client.force_authenticate(user=user2)
        with django_assert_num_queries(3):
            response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        res_json = response.json()
        assert res_json["count"] == count_related_objects_user2
        assert res_json["results"][0]["id"] == taks_user_2[0].id
        assert res_json["results"][0]["title"] == taks_user_2[0].title
        assert res_json["results"][0]["description"] == taks_user_2[0].description
        assert res_json["results"][0]["description"] == taks_user_2[0].description
        for task in res_json["results"]:
            assert task["user"] == user2.id

    @pytest.mark.django_db
    def test_action_detail(self, api_client, django_assert_num_queries):
        """
        Тестирование получения детальной информации о задаче
        """

        user1 = UserFactory()
        user2 = UserFactory()
        task = TaskFactory(user=user1)
        count_task_files = 5
        task_files = [TaskFileFactory(task=task) for _ in range(count_task_files)]

        api_client.force_authenticate(user=user1)
        url = reverse("tasks-detail", kwargs={"pk": task.id})
        with django_assert_num_queries(2):
            response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        res_json = response.json()
        assert res_json["title"] == task.title
        assert res_json["description"] == task.description
        assert res_json["completion_date"] == task.completion_date.isoformat()
        assert res_json["active"] == task.active

        api_client.force_authenticate(user=user2)
        url = reverse("tasks-detail", kwargs={"pk": task.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_action_update(self, api_client, django_assert_num_queries):
        """
        Тестирование обновления задачи
        """

        user = UserFactory()
        task = TaskFactory(user=user)
        old_task_title = task.title
        old_task_description = task.description
        task_update_data = {
            "title": "Update_title",
            "description": "Update description",
        }

        api_client.force_authenticate(user=user)
        url = reverse("tasks-detail", kwargs={"pk": task.id})
        with django_assert_num_queries(4):
            response = api_client.put(url, data=task_update_data)
        assert response.status_code == status.HTTP_200_OK
        task: Task = Task.objects.first()
        assert task.title == task_update_data["title"]
        assert task.description == task_update_data["description"]
        assert task.title != old_task_title
        assert task.description != old_task_description

        user2 = UserFactory()
        api_client.force_authenticate(user=user2)
        url = reverse("tasks-detail", kwargs={"pk": task.id})
        response = api_client.put(url, data=task_update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_action_delete(self, api_client, django_assert_num_queries):
        """
        Тестирование удаления задачи
        """

        user = UserFactory()
        task = TaskFactory(user=user)

        api_client.force_authenticate(user=user)
        url = reverse("tasks-detail", kwargs={"pk": task.id})
        with django_assert_num_queries(4):
            response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Task.objects.count() == 0

        user2 = UserFactory()
        task = TaskFactory(user=user2)

        api_client.force_authenticate(user=user)
        url = reverse("tasks-detail", kwargs={"pk": task.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
