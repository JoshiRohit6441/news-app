# Generated by Django 5.0.2 on 2024-02-28 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsEditor', '0004_alter_news_long_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='card_title',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
