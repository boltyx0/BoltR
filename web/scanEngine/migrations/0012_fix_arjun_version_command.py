# Arjun has no --version flag; use pip show for version lookup.

from django.db import migrations


def fix_arjun_version(apps, schema_editor):
    InstalledExternalTool = apps.get_model('scanEngine', 'InstalledExternalTool')
    for tool in InstalledExternalTool.objects.filter(name='Arjun'):
        tool.version_lookup_command = 'pip show arjun'
        tool.save()
        break


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('scanEngine', '0011_add_arjun_external_tool'),
    ]

    operations = [
        migrations.RunPython(fix_arjun_version, noop_reverse),
    ]
