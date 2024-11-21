from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Student

@receiver(post_save, sender=Student)
@receiver(post_delete, sender=Student)
def clear_student_cache(sender, instance, **kwargs):
    cache_key = f"student_{instance.id}"
    cache.delete(cache_key)
