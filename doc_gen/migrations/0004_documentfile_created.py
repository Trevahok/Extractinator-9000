# Generated by Django 2.1.7 on 2019-03-16 20:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('doc_gen', '0003_template_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentfile',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created at:'),
            preserve_default=False,
        ),
    ]
