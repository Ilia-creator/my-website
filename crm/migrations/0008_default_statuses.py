from django.db import migrations


STATUSES = ['Новый', 'В работе', 'Выполнен', 'Отклонён']


def create_statuses(apps, schema_editor):
    StatusCrm = apps.get_model('crm', 'StatusCrm')
    for name in STATUSES:
        StatusCrm.objects.get_or_create(status_name=name)


def remove_statuses(apps, schema_editor):
    StatusCrm = apps.get_model('crm', 'StatusCrm')
    StatusCrm.objects.filter(status_name__in=STATUSES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_order_order_package'),
    ]

    operations = [
        migrations.RunPython(create_statuses, remove_statuses),
    ]
