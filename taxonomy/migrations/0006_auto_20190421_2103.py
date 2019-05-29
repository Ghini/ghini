# Generated by Django 2.2 on 2019-04-21 21:03

from django.db import migrations, models
import django.db.models.deletion


def depopulate(apps, schema_editor):
    Rank = apps.get_model('taxonomy', 'Rank')
    Rank.objects.all().delete()

def import_defaults(apps, schema_editor):
    # We can't import the model directly as it may be a newer version than
    # this migration expects. We use the historical version.
    Rank = apps.get_model('taxonomy', 'Rank')
    Rank.objects.all().delete()
    import os
    print(os.getcwd())

    import csv
    with open('taxonomy/migrations/0006_auto_20190421_2103.rank.csv', newline='') as csvfile:
         spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
         header = next(spamreader)
         for row in spamreader:
             item = dict(zip(header, row))
             for key in header:
                 if item[key] == '':
                     del item[key]
             obj = Rank.objects.create(**item)
             obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0005_auto_20190421_1128'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('short', models.CharField(max_length=8)),
                ('shows_as', models.CharField(default='.epithet sp.', max_length=32)),
            ],
        ),
        migrations.RunPython(import_defaults, depopulate),
        migrations.AlterField(
            model_name='taxon',
            name='rank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='taxonomy.Rank'),
        ),
    ]
