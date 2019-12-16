from __future__ import unicode_literals

from django.db import migrations

skills = ['android', 'designer', 'java', 'php', 'python', 'rails', 'wordpress', 'ios']


def make_skills(apps, schema_editor):
    Skill = apps.get_model('accounts', 'Skill')

    for skill in skills:
        Skill.objects.create(name=skill)


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20191119_2108'),
    ]

    operations = [
        migrations.RunPython(make_skills)
    ]
