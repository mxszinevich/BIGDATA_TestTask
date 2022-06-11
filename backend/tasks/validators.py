from datetime import datetime

from rest_framework import serializers


def validate_completion_date(value: str) -> str:
    """
    Валидация даты окончания задачи
    """

    try:
        completion_date = datetime.fromisoformat(value)
    except ValueError:
        raise serializers.ValidationError("Неверный формат даты (YYYY-MM-DD)")

    if datetime.now().date() > completion_date.date():
        raise serializers.ValidationError(
            "Дата завершения задачи превышает текущую дату"
        )

    return value
