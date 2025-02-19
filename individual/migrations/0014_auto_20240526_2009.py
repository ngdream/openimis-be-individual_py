# Generated by Django 3.2.25 on 2024-05-26 20:09

import core.fields
import datetime
import dirtyfields.dirtyfields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('individual', '0013_add_group_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalGroupDataSource',
            fields=[
                ('id', models.UUIDField(db_column='UUID', db_index=True, default=None, editable=False)),
                ('is_deleted', models.BooleanField(db_column='isDeleted', default=False)),
                ('json_ext', models.JSONField(blank=True, db_column='Json_ext', null=True)),
                ('date_created', core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True)),
                ('date_updated', core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True)),
                ('version', models.IntegerField(default=1)),
                ('validations', models.JSONField(blank=True, default=dict)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('group', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='individual.group')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('upload', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='individual.individualdatasourceupload')),
                ('user_created', models.ForeignKey(blank=True, db_column='UserCreatedUUID', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(blank=True, db_column='UserUpdatedUUID', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical group data source',
                'verbose_name_plural': 'historical group data sources',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='GroupDataSource',
            fields=[
                ('id', models.UUIDField(db_column='UUID', default=None, editable=False, primary_key=True, serialize=False)),
                ('is_deleted', models.BooleanField(db_column='isDeleted', default=False)),
                ('json_ext', models.JSONField(blank=True, db_column='Json_ext', null=True)),
                ('date_created', core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True)),
                ('date_updated', core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True)),
                ('version', models.IntegerField(default=1)),
                ('validations', models.JSONField(blank=True, default=dict)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='individual.group')),
                ('upload', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='individual.individualdatasourceupload')),
                ('user_created', models.ForeignKey(db_column='UserCreatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='groupdatasource_user_created', to=settings.AUTH_USER_MODEL)),
                ('user_updated', models.ForeignKey(db_column='UserUpdatedUUID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='groupdatasource_user_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]
