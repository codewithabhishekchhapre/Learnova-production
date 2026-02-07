# Generated migration - Add default categories for landing page

from django.db import migrations


def create_default_categories(apps, schema_editor):
    Category = apps.get_model('courses', 'Category')
    defaults = [
        {'name': 'Competitive Exams', 'slug': 'competitive-exams', 'class_range': 'Class 3 - 13'},
        {'name': 'School Tuition', 'slug': 'school-tuition', 'class_range': 'Class 3 - 12'},
        {'name': 'Courses for kids', 'slug': 'courses-for-kids', 'class_range': 'Class LKG - 8'},
    ]
    for d in defaults:
        Category.objects.get_or_create(slug=d['slug'], defaults=d)


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_add_audience_class_range'),
    ]

    operations = [
        migrations.RunPython(create_default_categories, reverse_noop),
    ]
