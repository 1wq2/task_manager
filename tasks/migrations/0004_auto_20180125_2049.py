# Generated by Django 2.0.1 on 2018-01-25 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20180125_0850'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(choices=[('Manager', 'Manager'), ('Developer', 'Developer')], default='Developer', max_length=15)),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='user',
        ),
        migrations.AddField(
            model_name='project',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='tasks.Project'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.UserRole'),
        ),
    ]
