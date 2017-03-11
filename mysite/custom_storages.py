# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


class MediaStorage(S3BotoStorage):
    """
    Storage for uploaded media files.
    """
    location = settings.MEDIAFILES_LOCATION
