# Generated by Django 5.0.2 on 2024-02-22 14:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0002_tbl_collegecandidate'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_semmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sem1', models.IntegerField()),
                ('sem2', models.IntegerField()),
                ('sem3', models.IntegerField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.tbl_collegecandidate')),
            ],
        ),
    ]
