from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from django.conf import settings

from django.core.files.uploadedfile import SimpleUploadedFile

from timeside.core.tools.test_samples import generateSamples
from timeside.server.models import Item

import tempfile
import shutil

from timeside.server.tests.timeside_test_server import TimeSideTestServer


# class SelectionTests(APITestCase):

# class ExperienceTests(APITestCase):

# class ProviderTests(APITestCase):

# class ResultTests(APITestCase):