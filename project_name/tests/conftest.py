import os

from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages.storage.fallback import FallbackStorage

settings.DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}


def fake_image(img_path=None):
    """Generate a fake file object"""
    img_name = 'playdates_test_img.jpg'
    type = 'image/jpeg'

    if not img_path:
        img_path = os.path.join(settings.BASE_DIR, 'tests', img_name)

    if not os.path.exists(img_path):
        image = Image.new("RGBA", (50, 50), "blue")
        image.save(img_path)

    with open(img_path, 'rb') as img:
        file_obj = SimpleUploadedFile(img_name, img.read(), content_type=type)

    # Convenience to get path in tests
    file_obj.path = img_path

    return file_obj


def mock_messages(request):
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)
