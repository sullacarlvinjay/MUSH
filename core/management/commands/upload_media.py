"""Copy files from the local media/ folder into the configured default storage (Supabase)."""

from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Upload files in MEDIA_ROOT to Supabase Storage, keeping their paths.'

    def handle(self, *args, **options):
        if not settings.USE_SUPABASE_STORAGE:
            raise CommandError('Supabase Storage is not configured (set SUPABASE_PROJECT_REF and S3 keys).')

        uploaded = skipped = 0
        for path in sorted(settings.MEDIA_ROOT.rglob('*')):
            if not path.is_file():
                continue
            name = path.relative_to(settings.MEDIA_ROOT).as_posix()
            if default_storage.exists(name):
                skipped += 1
                continue
            with path.open('rb') as f:
                default_storage.save(name, File(f))
            uploaded += 1
            self.stdout.write(f'Uploaded {name}')

        self.stdout.write(self.style.SUCCESS(f'Done: {uploaded} uploaded, {skipped} already present.'))
