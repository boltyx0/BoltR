# Add byp4xx (40X/HTTP bypasser in Go) to Tools Arsenal if not present.
# https://github.com/lobuhi/byp4xx

from django.db import migrations


def add_byp4xx_tool(apps, schema_editor):
    InstalledExternalTool = apps.get_model('scanEngine', 'InstalledExternalTool')
    if InstalledExternalTool.objects.filter(name='byp4xx').exists():
        return
    InstalledExternalTool.objects.create(
        name='byp4xx',
        description=(
            '40X/HTTP bypasser in Go. Verb tampering, headers, #bugbountytips, '
            'User-Agents, extensions, default credentials. Usage: byp4xx <URL or file> '
            'with -L, -x, -m, -H, -d (cURL options). https://github.com/lobuhi/byp4xx'
        ),
        github_url='https://github.com/lobuhi/byp4xx',
        license_url='https://github.com/lobuhi/byp4xx/blob/main/README.md',
        version_lookup_command='go version -m /home/rengine/tools/go/bin/byp4xx',
        update_command='go install -v github.com/lobuhi/byp4xx@latest',
        install_command='go install -v github.com/lobuhi/byp4xx@latest',
        version_match_regex=r'v?(\d+\.\d+\.\d+[\w.-]*)',
        is_default=True,
        is_subdomain_gathering=False,
        is_github_cloned=False,
        github_clone_path=None,
        logo_url=None,
        subdomain_gathering_command=None,
    )


def remove_byp4xx_tool(apps, schema_editor):
    InstalledExternalTool = apps.get_model('scanEngine', 'InstalledExternalTool')
    InstalledExternalTool.objects.filter(name='byp4xx').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('scanEngine', '0012_fix_arjun_version_command'),
    ]

    operations = [
        migrations.RunPython(add_byp4xx_tool, remove_byp4xx_tool),
    ]
