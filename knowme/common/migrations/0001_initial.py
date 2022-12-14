# Generated by Django 3.2.16 on 2022-12-14 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('publish_date', models.DateTimeField(auto_now=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
                ('to_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
            options={
                'ordering': ['-publish_date'],
            },
        ),
        migrations.CreateModel(
            name='SavePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('save_date', models.DateField(auto_now=True)),
                ('to_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
                ('to_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
            ],
            options={
                'ordering': ['-save_date'],
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_date', models.DateTimeField(auto_now=True)),
                ('to_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
                ('to_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
            ],
            options={
                'ordering': ['-publish_date'],
            },
        ),
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follow_date', models.DateField(auto_now=True)),
                ('following_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='accounts.profile')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='accounts.profile')),
            ],
            options={
                'ordering': ['-follow_date'],
            },
        ),
        migrations.CreateModel(
            name='CommentReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=300)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
                ('to_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.comment')),
            ],
        ),
        migrations.AddConstraint(
            model_name='followers',
            constraint=models.UniqueConstraint(fields=('profile_id', 'following_profile_id'), name='unique_followers'),
        ),
    ]
