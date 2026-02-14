# Add Semgrep (static analysis / SAST) to Tools Arsenal if not present.
# Install: pip install semgrep. https://github.com/semgrep/semgrep

from django.db import migrations


def add_semgrep_tool(apps, schema_editor):
    InstalledExternalTool = apps.get_model('scanEngine', 'InstalledExternalTool')
    if InstalledExternalTool.objects.filter(name='Semgrep').exists():
        return
    InstalledExternalTool.objects.create(
        name='Semgrep',
        description=(
            'Lightweight static analysis for many languages. Find bug variants '
            'with patterns that look like source code. Supports 30+ languages; '
            'SAST, SCA, secrets. CLI: semgrep scan, semgrep ci. '
            'https://github.com/semgrep/semgrep'
        ),
        github_url='https://github.com/semgrep/semgrep',
        license_url='https://github.com/semgrep/semgrep/blob/develop/LICENSE',
        version_lookup_command='pip show semgrep',
        update_command='pip install --upgrade semgrep',
        install_command='pip install semgrep',
        version_match_regex=r'(\d+\.\d+\.\d+)',
        is_default=True,
        is_subdomain_gathering=False,
        is_github_cloned=False,
        github_clone_path=None,
        logo_url='https://raw.githubusercontent.com/semgrep/semgrep/develop/semgrep.svg',
        subdomain_gathering_command=None,
    )


def remove_semgrep_tool(apps, schema_editor):
    InstalledExternalTool = apps.get_model('scanEngine', 'InstalledExternalTool')
    InstalledExternalTool.objects.filter(name='Semgrep').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('scanEngine', '0017_add_cloud_enum_external_tool'),
    ]

    operations = [
        migrations.RunPython(add_semgrep_tool, remove_semgrep_tool),
    ]
