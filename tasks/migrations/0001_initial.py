# Generated by Django 2.0.1 on 2018-01-22 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_title', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_title', models.FileField(upload_to='')),
                ('task_description', models.FileField(upload_to='')),
                ('task_due_date', models.FileField(upload_to='')),
                ('project', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tasks.Project')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tasks.User'),
        ),
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tasks.User'),
        ),
    ]
