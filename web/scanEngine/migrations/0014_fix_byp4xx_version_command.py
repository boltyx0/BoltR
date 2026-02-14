# byp4xx has no -version flag; use 'go version -m' to get module version.

from django.db import migrations

# Default path when installed via go install (GOPATH/bin)
BYP4XX_BIN_PATH = '/home/rengine/tools/go/bin/byp4xx'


def fix_byp4xx_version(apps, schema_editor):
    InstalledExternalTool = apps.get_model('scanEngine', 'InstalledExternalTool')
    for tool in InstalledExternalTool.objects.filter(name='byp4xx'):
        tool.version_lookup_command = f'go version -m {BYP4XX_BIN_PATH}'
        tool.version_match_regex = r'v?(\d+\.\d+\.\d+[\w.-]*)'
        tool.save()
        break


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('scanEngine', '0013_add_byp4xx_external_tool'),
    ]

    operations = [
        migrations.RunPython(fix_byp4xx_version, noop_reverse),
    ]
