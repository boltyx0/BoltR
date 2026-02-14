# Generated data migration: add Commix to Tools Arsenal if not present

from django.db import migrations


def add_commix_tool(apps, schema_editor):
    InstalledExternalTool = apps.get_model('scanEngine', 'InstalledExternalTool')
    if InstalledExternalTool.objects.filter(name='commix').exists():
        return
    InstalledExternalTool.objects.create(
        name='commix',
        description=(
            'Commix (Command Injection Exploiter) is an open source penetration '
            'testing tool that automates the detection and exploitation of command injection '
            'vulnerabilities. Supports classic, time-based, file-based and dynamic code evaluation '
            'techniques. Usage: https://github.com/commixproject/commix/wiki/Usage'
        ),
        github_url='https://github.com/commixproject/commix',
        license_url='https://github.com/commixproject/commix/blob/master/LICENSE.txt',
        version_lookup_command='cd /home/rengine/tools/.github/commix.git && python commix.py --version',
        update_command='cd /home/rengine/tools/.github/commix.git && git pull && python commix.py --update',
        install_command='git clone https://github.com/commixproject/commix.git',
        version_match_regex=r'(\d+\.\d+[\w.-]*)',
        is_default=True,
        is_subdomain_gathering=False,
        is_github_cloned=True,
        github_clone_path='/home/rengine/tools/.github/commix.git',
        logo_url=None,
        subdomain_gathering_command=None,
    )


def remove_commix_tool(apps, schema_editor):
    InstalledExternalTool = apps.get_model('scanEngine', 'InstalledExternalTool')
    InstalledExternalTool.objects.filter(name='commix').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('scanEngine', '0008_extend_field_limit'),
    ]

    operations = [
        migrations.RunPython(add_commix_tool, remove_commix_tool),
    ]
