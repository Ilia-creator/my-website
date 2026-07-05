from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_default_statuses'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_contact_method',
            field=models.CharField(
                choices=[('telegram', 'Telegram'), ('whatsapp', 'WhatsApp')],
                default='telegram',
                max_length=20,
                verbose_name='Contact method',
            ),
        ),
    ]
