# Add Arjun (HTTP parameter discovery) to Tools Arsenal if not present.
# Install: pip install arjun. Usage: https://github.com/s0md3v/Arjun/wiki/Usage

from django.db import migrations


def add_arjun_tool(apps, schema_editor):
    InstalledExternalTool = apps.get_model('scanEngine', 'InstalledExternalTool')
    if InstalledExternalTool.objects.filter(name='Arjun').exists():
        return
    InstalledExternalTool.objects.create(
        name='Arjun',
        description=(
            'Arjun is an HTTP parameter discovery suite. It finds query parameters '
            'for URL endpoints using a default dictionary of 25,890 parameter names. '
            'Supports GET/POST/JSON/XML, rate limits, export to BurpSuite/text/JSON. '
            'Usage: https://github.com/s0md3v/Arjun/wiki/Usage'
        ),
        github_url='https://github.com/s0md3v/Arjun',
        license_url='https://github.com/s0md3v/Arjun/blob/master/LICENSE',
        version_lookup_command='pip show arjun',
        update_command='pip install -U arjun',
        install_command='pip install arjun',
        version_match_regex=r'(\d+\.\d+\.\d+)',
        is_default=True,
        is_subdomain_gathering=False,
        is_github_cloned=False,
        github_clone_path=None,
        logo_url=None,
        subdomain_gathering_command=None,
    )


def remove_arjun_tool(apps, schema_editor):
    InstalledExternalTool = apps.get_model('scanEngine', 'InstalledExternalTool')
    InstalledExternalTool.objects.filter(name='Arjun').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('scanEngine', '0010_fix_commix_commands_and_path'),
    ]

    operations = [
        migrations.RunPython(add_arjun_tool, remove_arjun_tool),
    ]
