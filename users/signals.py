from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from django.contrib.auth.models import Group


@receiver(post_save, sender=CustomUser)
def user_created(sender, instance, created, **kwargs):
    group = Group.objects.get(name="User Group")
    if created:
        instance.groups.add(group)
        instance.is_staff = True
        instance.save()
