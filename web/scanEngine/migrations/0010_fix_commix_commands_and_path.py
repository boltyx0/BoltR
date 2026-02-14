# Fix Commix: run version/update from clone dir so they work in Celery worker.
# Clone path must match add_tool logic: install_command ends with commix.git -> path is .../commix.git

from django.db import migrations

# Path used when install is done via UI (add_tool uses project_name = "commix.git")
COMMIX_CLONE_PATH = '/home/rengine/tools/.github/commix.git'


def fix_commix(apps, schema_editor):
    InstalledExternalTool = apps.get_model('scanEngine', 'InstalledExternalTool')
    for tool in InstalledExternalTool.objects.filter(name='commix'):
        tool.github_clone_path = COMMIX_CLONE_PATH
        tool.version_lookup_command = f'cd {COMMIX_CLONE_PATH} && python commix.py --version'
        tool.update_command = f'cd {COMMIX_CLONE_PATH} && git pull && python commix.py --update'
        tool.save()
        break


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('scanEngine', '0009_add_commix_external_tool'),
    ]

    operations = [
        migrations.RunPython(fix_commix, noop_reverse),
    ]
