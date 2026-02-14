# Add Mantra (API key leak hunter in JS/HTML) to Tools Arsenal if not present.
# https://github.com/brosck/mantra

from django.db import migrations


def add_mantra_tool(apps, schema_editor):
    InstalledExternalTool = apps.get_model('scanEngine', 'InstalledExternalTool')
    if InstalledExternalTool.objects.filter(name='mantra').exists():
        return
    InstalledExternalTool.objects.create(
        name='mantra',
        description=(
            'Hunt down API key leaks in JS files and HTML pages. Checks source code '
            'for strings identical or similar to API keys. https://github.com/brosck/mantra'
        ),
        github_url='https://github.com/brosck/mantra',
        license_url='https://github.com/brosck/mantra/blob/main/LICENSE',
        version_lookup_command='go version -m /home/rengine/tools/go/bin/mantra',
        update_command='go install -v github.com/Brosck/mantra@latest',
        install_command='go install -v github.com/Brosck/mantra@latest',
        version_match_regex=r'v?(\d+\.\d+\.\d+[\w.-]*)',
        is_default=True,
        is_subdomain_gathering=False,
        is_github_cloned=False,
        github_clone_path=None,
        logo_url=None,
        subdomain_gathering_command=None,
    )


def remove_mantra_tool(apps, schema_editor):
    InstalledExternalTool = apps.get_model('scanEngine', 'InstalledExternalTool')
    InstalledExternalTool.objects.filter(name='mantra').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('scanEngine', '0014_fix_byp4xx_version_command'),
    ]

    operations = [
        migrations.RunPython(add_mantra_tool, remove_mantra_tool),
    ]
