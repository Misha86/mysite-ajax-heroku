from django.db.models.signals import post_delete
from loginsys.models import Profile
from django.dispatch import receiver
import os


@receiver(post_delete, sender=Profile, dispatch_uid="my_profile_delete")
def post_delete_profile_receiver(sender, instance, *args, **kwargs):
    image_url = instance.avatar.path
    os.remove(image_url)
    os.rmdir(os.path.dirname(image_url))