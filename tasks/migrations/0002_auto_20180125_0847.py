# Generated by Django 2.0.1 on 2018-01-25 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_description',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_due_date',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_title',
            field=models.CharField(max_length=100),
        ),
    ]