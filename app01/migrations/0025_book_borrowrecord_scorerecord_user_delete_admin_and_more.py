# Generated by Django 5.0 on 2024-06-21 20:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0024_alter_admin_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False, verbose_name='图书ID')),
                ('book_name', models.CharField(max_length=64, verbose_name='图书名')),
                ('author', models.CharField(max_length=64, verbose_name='作者')),
                ('publisher', models.CharField(max_length=64, verbose_name='出版社')),
                ('category', models.CharField(max_length=32, verbose_name='分类')),
                ('stock_quantity', models.IntegerField(verbose_name='库存数量')),
                ('borrow_count', models.IntegerField(default=0, verbose_name='借阅次数')),
                ('score', models.DecimalField(decimal_places=2, default=0.0, max_digits=3, verbose_name='评分')),
            ],
        ),
        migrations.CreateModel(
            name='BorrowRecord',
            fields=[
                ('record_id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录ID')),
                ('borrow_date', models.DateTimeField(auto_now_add=True, verbose_name='借阅日期')),
                ('return_date', models.DateTimeField(blank=True, null=True, verbose_name='归还日期')),
                ('status', models.SmallIntegerField(choices=[(1, '借阅'), (2, '归还'), (3, '逾期')], default=1, verbose_name='状态')),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.book', verbose_name='图书ID')),
            ],
        ),
        migrations.CreateModel(
            name='ScoreRecord',
            fields=[
                ('record_id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录ID')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2, verbose_name='评分')),
                ('review', models.TextField(blank=True, null=True, verbose_name='评论')),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.book', verbose_name='图书ID')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False, verbose_name='用户ID')),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('phone', models.CharField(max_length=15, verbose_name='联系电话')),
                ('registration_date', models.DateTimeField(auto_now_add=True, verbose_name='注册日期')),
                ('role', models.SmallIntegerField(choices=[(1, '普通用户'), (2, '管理员')], default=1, verbose_name='角色')),
            ],
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.DeleteModel(
            name='Catch',
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='depart',
        ),
        migrations.DeleteModel(
            name='XX',
        ),
        migrations.AddField(
            model_name='scorerecord',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user', verbose_name='用户ID'),
        ),
        migrations.AddField(
            model_name='borrowrecord',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.user', verbose_name='用户ID'),
        ),
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]
