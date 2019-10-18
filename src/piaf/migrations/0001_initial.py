# Generated by Django 2.1 on 2019-10-17 22:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('index', models.IntegerField()),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('theme', models.CharField(choices=[('Religion', 'Religion'), ('Géographie', 'Géographie'), ('Histoire', 'Histoire'), ('Sport', 'Sport'), ('Arts', 'Arts'), ('Société', 'Société'), ('Sciences', 'Sciences')], max_length=20)),
                ('reference', models.CharField(max_length=10)),
                ('audience', models.CharField(choices=[('restricted', 'restricted'), ('all', 'all')], default='all', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'pending'), ('progress', 'progress'), ('completed', 'completed')], default='pending', max_length=10)),
                ('article', models.ForeignKey(on_delete='cascade', related_name='paragraphs', to='piaf.Article')),
            ],
        ),
        migrations.CreateModel(
            name='ParagraphBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participated_at', models.DateField(auto_now=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('progress', 'progress'), ('completed', 'completed')], default='pending', max_length=10)),
                ('user', models.ForeignKey(null=True, on_delete='null', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('paragraph', models.ForeignKey(on_delete='cascade', related_name='questions', to='piaf.Paragraph')),
            ],
        ),
        migrations.AddField(
            model_name='paragraph',
            name='batch',
            field=models.ForeignKey(on_delete='cascade', related_name='paragraphs', to='piaf.ParagraphBatch'),
        ),
        migrations.AddField(
            model_name='paragraph',
            name='user',
            field=models.ForeignKey(null=True, on_delete='null', related_name='paragraphs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete='cascade', related_name='answers', to='piaf.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(null=True, on_delete='null', related_name='answers', to=settings.AUTH_USER_MODEL),
        ),
    ]