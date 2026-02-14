# Mantra has no -version flag; use 'go version -m' to get module version.

from django.db import migrations

MANTRA_BIN_PATH = '/home/rengine/tools/go/bin/mantra'


def fix_mantra_version(apps, schema_editor):
    InstalledExternalTool = apps.get_model('scanEngine', 'InstalledExternalTool')
    for tool in InstalledExternalTool.objects.filter(name='mantra'):
        tool.version_lookup_command = f'go version -m {MANTRA_BIN_PATH}'
        tool.version_match_regex = r'v?(\d+\.\d+\.\d+[\w.-]*)'
        tool.save()
        break


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('scanEngine', '0015_add_mantra_external_tool'),
    ]

    operations = [
        migrations.RunPython(fix_mantra_version, noop_reverse),
    ]
