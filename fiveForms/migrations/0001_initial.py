# Generated by Django 4.0.5 on 2022-09-16 20:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sectors', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='fiveForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Formulário')),
                ('description', models.TextField(blank=True, default='', verbose_name='Descrição do formulário')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data e hora da criação do formulário')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='última edição')),
                ('start_at', models.DateField(verbose_name='Data e hora de inicio do formulário')),
                ('end_at', models.DateField(verbose_name='Data e hora de fim do formulário')),
                ('sectorId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sectors.sectors', verbose_name='Setor')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuário que criou o formulário')),
            ],
        ),
        migrations.CreateModel(
            name='fiveFormAsk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ask', models.TextField(verbose_name='Pergunta')),
                ('askweight', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default='3', verbose_name='Peso da pergunta')),
                ('is_image', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data e hora da pergunta')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última edição da pergunta')),
                ('formId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fiveForms.fiveform', verbose_name='Formulário da pergunta')),
            ],
        ),
        migrations.CreateModel(
            name='fiveFormResponseImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='form/response/%Y%m%d', verbose_name='Imagem de resposta')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data e hora do envio da imagem')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última edição da imagem')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalfiveFormResponseImage',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('image', models.TextField(blank=True, max_length=100, null=True, verbose_name='Imagem de resposta')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Data e hora do envio da imagem')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='Última edição da imagem')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical five form response image',
                'verbose_name_plural': 'historical five form response images',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalfiveFormResponse',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('response', models.TextField(verbose_name='Resposta')),
                ('responseweight', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3)], default='5', verbose_name='Peso da resposta')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Data e hora da da pergunta')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='Última edição da pergunta')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('askId', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='fiveForms.fiveformask', verbose_name='Pergunta')),
                ('formId', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='fiveForms.fiveform', verbose_name='Formulário da resposta')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('image', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='fiveForms.fiveformresponseimage', verbose_name='imagem')),
                ('userId', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='usuário que criou a resposta')),
            ],
            options={
                'verbose_name': 'historical five form response',
                'verbose_name_plural': 'historical five form responses',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalfiveFormAsk',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('ask', models.TextField(verbose_name='Pergunta')),
                ('askweight', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default='3', verbose_name='Peso da pergunta')),
                ('is_image', models.BooleanField()),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Data e hora da pergunta')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='Última edição da pergunta')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('formId', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='fiveForms.fiveform', verbose_name='Formulário da pergunta')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical five form ask',
                'verbose_name_plural': 'historical five form asks',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalfiveForm',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Formulário')),
                ('description', models.TextField(blank=True, default='', verbose_name='Descrição do formulário')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Data e hora da criação do formulário')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, verbose_name='última edição')),
                ('start_at', models.DateField(verbose_name='Data e hora de inicio do formulário')),
                ('end_at', models.DateField(verbose_name='Data e hora de fim do formulário')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('sectorId', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sectors.sectors', verbose_name='Setor')),
                ('userId', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Usuário que criou o formulário')),
            ],
            options={
                'verbose_name': 'historical five form',
                'verbose_name_plural': 'historical five forms',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='fiveFormResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField(verbose_name='Resposta')),
                ('responseweight', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3)], default='5', verbose_name='Peso da resposta')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data e hora da da pergunta')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última edição da pergunta')),
                ('askId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fiveForms.fiveformask', verbose_name='Pergunta')),
                ('formId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='fiveForms.fiveform', verbose_name='Formulário da resposta')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='fiveForms.fiveformresponseimage', verbose_name='imagem')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='usuário que criou a resposta')),
            ],
        ),
    ]
