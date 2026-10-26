from django.db import migrations, models


def years_to_dates(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SELECT id, year FROM cars_car")
        rows = cursor.fetchall()
        for car_id, year in rows:
            if isinstance(year, int):
                if 0 < year < 100:
                    year += 2000
                cursor.execute(
                    "UPDATE cars_car SET year = %s WHERE id = %s",
                    [f"{year:04d}-01-01", car_id],
                )


def dates_to_years(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SELECT id, year FROM cars_car")
        rows = cursor.fetchall()
        for car_id, year in rows:
            if isinstance(year, str):
                cursor.execute(
                    "UPDATE cars_car SET year = %s WHERE id = %s",
                    [int(year[:4]), car_id],
                )


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0003_category_car_category"),
    ]

    operations = [
        migrations.RunPython(years_to_dates, dates_to_years),
        migrations.AlterField(
            model_name="car",
            name="year",
            field=models.DateField(),
        ),
    ]
