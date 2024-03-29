# Generated by Django 5.0.2 on 2024-02-24 07:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0001_initial'),
        ('Student', '0009_delete_tbl_collegepolling'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_collegepolling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polling_datetime', models.DateField(auto_now_add=True)),
                ('polling_status', models.IntegerField(default=0)),
                ('arts_candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arts', to='Student.tbl_collegecandidate')),
                ('chairperson_candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chairperson', to='Student.tbl_collegecandidate')),
                ('editor_candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='editor', to='Student.tbl_collegecandidate')),
                ('first_candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='first', to='Student.tbl_collegecandidate')),
                ('general_candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='general', to='Student.tbl_collegecandidate')),
                ('lady_candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lady', to='Student.tbl_collegecandidate')),
                ('polling_student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='Guest.tbl_newstudent')),
                ('sec_candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sec', to='Student.tbl_collegecandidate')),
                ('third_candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='third', to='Student.tbl_collegecandidate')),
                ('union_candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='union', to='Student.tbl_collegecandidate')),
                ('vchairperson_candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vchairperson', to='Student.tbl_collegecandidate')),
            ],
        ),
    ]
