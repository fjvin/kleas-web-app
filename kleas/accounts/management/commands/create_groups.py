from django.core.management.base import BaseCommand
from sales.models import Sale
from expenses.models import ExpensesRestock, ExpensesStore
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType




class Command(BaseCommand):
    help = 'Create User Groups and Setup Permissions'
    
    def handle(self, *args, **kwargs):

        # create the groups
        admin_group, created = Group.objects.get_or_create(name="admin")
        staff_group, created = Group.objects.get_or_create(name="staff")

        # fetch permissions per model
        content_type = ContentType.objects.get_for_model(Sale)
        sale_permission = Permission.objects.filter(content_type=content_type)
        content_type = ContentType.objects.get_for_model(ExpensesRestock)
        restock_permission = Permission.objects.filter(content_type=content_type)
        content_type = ContentType.objects.get_for_model(ExpensesStore)
        store_permission = Permission.objects.filter(content_type=content_type)

        # add all permission to admin
        for model_permission in (sale_permission, restock_permission, store_permission):
            for perm in model_permission:
                admin_group.permissions.add(perm)

        # add only view_{model} permission for staff
        for model_permission in (sale_permission, restock_permission, store_permission):
            for perm in model_permission:
                if perm.codename.startswith('view'):
                    staff_group.permissions.add(perm)



       