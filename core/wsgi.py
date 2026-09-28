"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

from pathlib import Path
import ctypes
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


print("=== VERCEL GIS DEBUG ===")

lib_dir = Path("/var/task/lib")

print("cwd:", os.getcwd())
print("lib exists:", lib_dir.exists())

if lib_dir.exists():
    print("lib contents:", [x.name for x in lib_dir.iterdir()])

for name in [
    "libgdal.so",
    "libgeos_c.so.1",
    "libgeos.so.3.10.3",
    "libproj.so.22",
]:
    path = lib_dir / name
    print(f"{path}: exists={path.exists()}")

    if path.exists():
        try:
            ctypes.CDLL(str(path))
            print(f"[OK] ctypes: {name}")
        except Exception as e:
            print(f"[FAIL] ctypes: {name}: {e}")

print("LD_LIBRARY_PATH:", os.environ.get("LD_LIBRARY_PATH"))
print("GDAL_LIBRARY_PATH:", os.environ.get("GDAL_LIBRARY_PATH"))
print("GEOS_LIBRARY_PATH:", os.environ.get("GEOS_LIBRARY_PATH"))

print("=== END GIS DEBUG ===")

app = get_wsgi_application()

application = app
