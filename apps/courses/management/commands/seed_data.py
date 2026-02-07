"""
Management command to seed categories and sample courses with instructor.
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from apps.users.models import User, UserProfile
from apps.courses.models import Category, Course


class Command(BaseCommand):
    help = "Create sample categories and courses with instructor user"

    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")

        # Create instructor if not exists
        instructor, created = User.objects.get_or_create(
            username="instructor",
            defaults={
                "email": "instructor@learnova.com",
                "first_name": "John",
                "last_name": "Instructor",
                "role": "INSTRUCTOR",
                "is_staff": False,
                "is_superuser": False,
            },
        )
        if created:
            instructor.set_password("instructor123")
            instructor.save()
            UserProfile.objects.get_or_create(user=instructor)
            self.stdout.write(self.style.SUCCESS("Created instructor: instructor / instructor123"))
        else:
            self.stdout.write("Instructor already exists (username: instructor)")

        # Create categories
        categories_data = [
            {
                "name": "Competitive Exams",
                "slug": "competitive-exams",
                "description": "JEE, NEET, Olympiad and other competitive exam preparation",
                "class_range": "Class 3 - 13",
            },
            {
                "name": "School Tuition",
                "slug": "school-tuition",
                "description": "CBSE, ICSE and board curriculum",
                "class_range": "Class 3 - 12",
            },
            {
                "name": "Courses for kids",
                "slug": "courses-for-kids",
                "description": "Fun, interactive programs for young learners",
                "class_range": "Class LKG - 8",
            },
            {
                "name": "Programming",
                "slug": "programming",
                "description": "Coding and software development",
                "class_range": "All levels",
            },
        ]

        created_cats = {}
        for data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=data["slug"], defaults=data
            )
            created_cats[data["slug"]] = cat
            if created:
                self.stdout.write(f"  Created category: {cat.name}")

        # Create sample courses
        courses_data = [
            {
                "title": "Spoken English Program",
                "slug": "spoken-english-program",
                "description": "Master fluency in English speaking with interactive sessions.",
                "category": created_cats["courses-for-kids"],
                "status": Course.Status.PUBLISHED,
                "audience": Course.Audience.KIDS,
                "class_range": "Class LKG - 8",
                "duration_hours": 40,
                "level": "Beginner",
            },
            {
                "title": "Learn Math",
                "slug": "learn-math",
                "description": "Turn your child into a Math wizard with step-by-step learning.",
                "category": created_cats["courses-for-kids"],
                "status": Course.Status.PUBLISHED,
                "audience": Course.Audience.KIDS,
                "class_range": "Class KG - 8",
                "duration_hours": 60,
                "level": "Beginner",
            },
            {
                "title": "Coding classes",
                "slug": "coding-classes",
                "description": "Learn to build apps and games, be future ready.",
                "category": created_cats["courses-for-kids"],
                "status": Course.Status.PUBLISHED,
                "audience": Course.Audience.KIDS,
                "class_range": "Class 1 - 8",
                "duration_hours": 80,
                "level": "Beginner",
            },
            {
                "title": "JEE Foundation",
                "slug": "jee-foundation",
                "description": "Build strong fundamentals for JEE preparation.",
                "category": created_cats["competitive-exams"],
                "status": Course.Status.PUBLISHED,
                "audience": Course.Audience.STUDENT,
                "class_range": "Class 9 - 12",
                "duration_hours": 120,
                "level": "Advanced",
            },
            {
                "title": "Advanced Web Development",
                "slug": "advanced-web-development",
                "description": "MERN stack, HTML, CSS, JS, Node.js - full stack development course.",
                "category": created_cats["programming"],
                "status": Course.Status.PUBLISHED,
                "audience": Course.Audience.STUDENT,
                "class_range": "",
                "duration_hours": 120,
                "level": "Advanced",
            },
        ]

        for data in courses_data:
            course, created = Course.objects.get_or_create(
                slug=data["slug"],
                defaults={**data, "instructor": instructor},
            )
            if created:
                self.stdout.write(f"  Created course: {course.title}")

        self.stdout.write(self.style.SUCCESS("Seed data completed."))
