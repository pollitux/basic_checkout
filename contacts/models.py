from django.db import models

from core.models import UUIDModel


class Contact(UUIDModel):
    """
    Represents an individual contact.
    """
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255, unique=True)
    segment = models.CharField(
        max_length=255, default='other',
        choices=(('family', 'Family'), ('work', 'Work'), ('friends', 'Friends'), ('other', 'Other'),
                 ('favourite', 'Favourite')), )
    is_blocked = models.BooleanField(default=False)
    birthday = models.DateField(null=True, blank=True)
    photo = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['full_name']
