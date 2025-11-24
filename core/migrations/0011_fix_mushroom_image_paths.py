from django.db import migrations

def fix_image_paths(apps, schema_editor):
    """Remove 'static/' prefix from mushroom image paths."""
    MushroomImage = apps.get_model('core', 'MushroomImage')
    UnknownMushroom = apps.get_model('core', 'UnknownMushroom')
    
    # Fix MushroomImage entries
    for mushroom in MushroomImage.objects.all():
        if mushroom.image and mushroom.image.name.startswith('static/'):
            mushroom.image.name = mushroom.image.name.replace('static/', '', 1)
            mushroom.save()
    
    # Fix UnknownMushroom entries  
    for mushroom in UnknownMushroom.objects.all():
        if mushroom.image and mushroom.image.name.startswith('static/'):
            mushroom.image.name = mushroom.image.name.replace('static/', '', 1)
            mushroom.save()

def reverse_fix_image_paths(apps, schema_editor):
    """Add 'static/' prefix back (reverse operation)."""
    MushroomImage = apps.get_model('core', 'MushroomImage')
    UnknownMushroom = apps.get_model('core', 'UnknownMushroom')
    
    # Reverse MushroomImage entries
    for mushroom in MushroomImage.objects.all():
        if mushroom.image and not mushroom.image.name.startswith('static/'):
            mushroom.image.name = 'static/' + mushroom.image.name
            mushroom.save()
    
    # Reverse UnknownMushroom entries
    for mushroom in UnknownMushroom.objects.all():
        if mushroom.image and not mushroom.image.name.startswith('static/'):
            mushroom.image.name = 'static/' + mushroom.image.name
            mushroom.save()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0010_alter_mushroomimage_image_and_more'),
    ]
    
    operations = [
        migrations.RunPython(fix_image_paths, reverse_fix_image_paths),
    ]
