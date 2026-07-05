from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0003_pricecardimage'),
        ('crm', '0006_remove_statuscrm_status_name_alter_comentcrm_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='price.pricecard', verbose_name='Услуга'),
        ),
    ]
