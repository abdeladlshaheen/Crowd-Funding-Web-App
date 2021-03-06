# Generated by Django 4.0.4 on 2022-05-08 18:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrateproject',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projectreport',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
        migrations.AddField(
            model_name='projectreport',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projectdonation',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.project'),
        ),
        migrations.AddField(
            model_name='projectdonation',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.category'),
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(to='projects.tag'),
        ),
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='picture',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
        migrations.AddField(
            model_name='commentreport',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.comment'),
        ),
        migrations.AddField(
            model_name='commentreport',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
