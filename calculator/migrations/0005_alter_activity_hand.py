# Generated by Django 5.2.2 on 2025-07-10 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0004_alter_activity_description_source_measuring"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activity",
            name="hand",
            field=models.CharField(
                choices=[("left", "Lewa ręka"), ("right", "Prawa ręka")],
                max_length=50,
                verbose_name="Miejsce, orientacja osi oraz metoda mocowania przetwornika",
            ),
        ),
    ]
