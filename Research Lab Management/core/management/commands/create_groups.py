from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Project, Equipment, Inventory, Publication, Grant, Protocol, Staff

class Command(BaseCommand):
    help = 'Creates user groups and assigns permissions'

    def handle(self, *args, **options):
        groups = {
            'Principal Investigator': {
                Project: ['add', 'change', 'delete', 'view'],
                Equipment: ['view'],
                Inventory: ['view'],
                Publication: ['add', 'change', 'delete', 'view'],
                Grant: ['add', 'change', 'delete', 'view'],
                Protocol: ['add', 'change', 'delete', 'view'],
                Staff: ['add', 'change', 'delete', 'view'],
            },
            'Postdoctoral Researcher': {
                Project: ['view'],
                Equipment: ['view'],
                Inventory: ['add', 'change', 'view'],
                Publication: ['add', 'change', 'view'],
                Protocol: ['add', 'change', 'view'],
            },
            'Graduate Student': {
                Project: ['view'],
                Equipment: ['view'],
                Inventory: ['view'],
                Publication: ['add', 'view'],
                Protocol: ['view'],
            },
            'Lab Manager': {
                Project: ['view'],
                Equipment: ['add', 'change', 'delete', 'view'],
                Inventory: ['add', 'change', 'delete', 'view'],
                Staff: ['add', 'change', 'delete', 'view'],
            },
        }

        for group_name, permissions in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created group "{group_name}"'))
            for model, perms in permissions.items():
                content_type = ContentType.objects.get_for_model(model)
                for perm_codename in perms:
                    permission = Permission.objects.get(codename=f'{perm_codename}_{model._meta.model_name}')
                    group.permissions.add(permission)
            self.stdout.write(self.style.SUCCESS(f'Successfully assigned permissions to group "{group_name}"'))
