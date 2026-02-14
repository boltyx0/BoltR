# Add cloud_enum (multi-cloud OSINT for AWS/Azure/GCP) to Tools Arsenal if not present.
# https://github.com/initstring/cloud_enum

from django.db import migrations

CLOUD_ENUM_CLONE_PATH = '/home/rengine/tools/.github/cloud_enum.git'


def add_cloud_enum_tool(apps, schema_editor):
    InstalledExternalTool = apps.get_model('scanEngine', 'InstalledExternalTool')
    if InstalledExternalTool.objects.filter(name='cloud_enum').exists():
        return
    InstalledExternalTool.objects.create(
        name='cloud_enum',
        description=(
            'Multi-cloud OSINT. Enumerate public resources in AWS (S3, awsapps), '
            'Azure (storage, blob, DBs, VMs, web apps), GCP (buckets, Firebase, '
            'App Engine, Cloud Functions). Usage: cloud_enum.py -k KEYWORD. '
            'https://github.com/initstring/cloud_enum'
        ),
        github_url='https://github.com/initstring/cloud_enum',
        license_url='https://github.com/initstring/cloud_enum/blob/master/LICENSE',
        version_lookup_command='git describe --tags',
        update_command=f'cd {CLOUD_ENUM_CLONE_PATH} && git pull && pip install -r requirements.txt',
        install_command='git clone https://github.com/initstring/cloud_enum.git',
        version_match_regex=r'(\d+\.\d+)',
        is_default=True,
        is_subdomain_gathering=False,
        is_github_cloned=True,
        github_clone_path=CLOUD_ENUM_CLONE_PATH,
        logo_url=None,
        subdomain_gathering_command=None,
    )


def remove_cloud_enum_tool(apps, schema_editor):
    InstalledExternalTool = apps.get_model('scanEngine', 'InstalledExternalTool')
    InstalledExternalTool.objects.filter(name='cloud_enum').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('scanEngine', '0016_fix_mantra_version_command'),
    ]

    operations = [
        migrations.RunPython(add_cloud_enum_tool, remove_cloud_enum_tool),
    ]
