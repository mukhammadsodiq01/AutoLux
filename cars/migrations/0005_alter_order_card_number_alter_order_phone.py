from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0004_alter_car_year"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="card_number",
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name="order",
            name="phone",
            field=models.CharField(max_length=13),
        ),
    ]
