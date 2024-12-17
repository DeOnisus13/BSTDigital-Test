from django.db.models.signals import post_save


def bulk_create_with_signals(model_class, objects):
    """
    Функция для замещения метода bulk_create.
    Этот метод удобен, когда нужно добавить сразу много записей в БД, но с ним не работают сигналы.
    В данной функции для всех создаваемых объектов принудительно вызывается срабатывание сигнала.
    """
    # Сначала делаем заполнение БД через bulk_create
    created_objects = model_class.objects.bulk_create(objects)

    # Затем вызываем сигнал post_save вручную для каждого объекта
    for obj in created_objects:
        post_save.send(sender=model_class, instance=obj, created=True)

    return created_objects
