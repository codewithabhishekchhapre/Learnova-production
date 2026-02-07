"""
Management command to seed categories, courses, and users (admin, instructors, students).
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from apps.users.models import User, UserProfile
from apps.courses.models import Category, Course


class Command(BaseCommand):
    help = "Create sample categories, courses, and users (admin, instructors, students)"

    def handle(self, *args, **options):
        self.stdout.write("Seeding data...")

        # Create admin
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@learnova.com",
                "first_name": "Admin",
                "last_name": "User",
                "role": User.Role.ADMIN,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin_user.set_password("admin123")
            admin_user.save()
            UserProfile.objects.get_or_create(user=admin_user)
            self.stdout.write(self.style.SUCCESS("Created admin: admin / admin123"))
        else:
            self.stdout.write("Admin already exists (username: admin)")

        # Create instructors (2–3)
        instructors_data = [
            ("instructor", "instructor@learnova.com", "John", "Instructor", "instructor123"),
            ("instructor2", "instructor2@learnova.com", "Sarah", "Johnson", "instructor123"),
            ("instructor3", "instructor3@learnova.com", "Mike", "Williams", "instructor123"),
        ]
        instructors = []
        for username, email, first, last, pwd in instructors_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": first,
                    "last_name": last,
                    "role": User.Role.INSTRUCTOR,
                    "is_staff": False,
                    "is_superuser": False,
                },
            )
            if created:
                user.set_password(pwd)
                user.save()
                UserProfile.objects.get_or_create(user=user)
                instructors.append(user)
                self.stdout.write(self.style.SUCCESS(f"Created instructor: {username} / {pwd}"))
            else:
                instructors.append(user)
                self.stdout.write(f"Instructor already exists: {username}")

        instructor = instructors[0]  # primary for courses

        # Create students (7)
        students_data = [
            ("student1", "student1@learnova.com", "Emma", "Davis"),
            ("student2", "student2@learnova.com", "James", "Brown"),
            ("student3", "student3@learnova.com", "Olivia", "Miller"),
            ("student4", "student4@learnova.com", "Liam", "Wilson"),
            ("student5", "student5@learnova.com", "Ava", "Taylor"),
            ("student6", "student6@learnova.com", "Noah", "Anderson"),
            ("student7", "student7@learnova.com", "Sophia", "Thomas"),
        ]
        for username, email, first, last in students_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": first,
                    "last_name": last,
                    "role": User.Role.STUDENT,
                    "is_staff": False,
                    "is_superuser": False,
                },
            )
            if created:
                user.set_password("student123")
                user.save()
                UserProfile.objects.get_or_create(user=user)
                self.stdout.write(self.style.SUCCESS(f"Created student: {username} / student123"))
            else:
                self.stdout.write(f"Student already exists: {username}")

        # Create categories
        categories_data = [
            {"name": "Competitive Exams", "slug": "competitive-exams", "description": "JEE, NEET, Olympiad and other competitive exam preparation", "class_range": "Class 3 - 13"},
            {"name": "School Tuition", "slug": "school-tuition", "description": "CBSE, ICSE and board curriculum", "class_range": "Class 3 - 12"},
            {"name": "Courses for kids", "slug": "courses-for-kids", "description": "Fun, interactive programs for young learners", "class_range": "Class LKG - 8"},
            {"name": "Programming", "slug": "programming", "description": "Coding and software development", "class_range": "All levels"},
            {"name": "Science & Math", "slug": "science-math", "description": "Physics, Chemistry, Mathematics for all levels", "class_range": "Class 6 - 12"},
            {"name": "Languages", "slug": "languages", "description": "English, Hindi, and regional languages", "class_range": "All levels"},
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
            {"title": "Spoken English Program", "slug": "spoken-english-program", "description": "Master fluency in English speaking with interactive sessions.", "category": "courses-for-kids", "status": Course.Status.PUBLISHED, "audience": Course.Audience.KIDS, "class_range": "Class LKG - 8", "duration_hours": 40, "level": "Beginner", "instructor_idx": 0},
            {"title": "Learn Math", "slug": "learn-math", "description": "Turn your child into a Math wizard with step-by-step learning.", "category": "courses-for-kids", "status": Course.Status.PUBLISHED, "audience": Course.Audience.KIDS, "class_range": "Class KG - 8", "duration_hours": 60, "level": "Beginner", "instructor_idx": 0},
            {"title": "Coding classes", "slug": "coding-classes", "description": "Learn to build apps and games, be future ready.", "category": "courses-for-kids", "status": Course.Status.PUBLISHED, "audience": Course.Audience.KIDS, "class_range": "Class 1 - 8", "duration_hours": 80, "level": "Beginner", "instructor_idx": 0},
            {"title": "JEE Foundation", "slug": "jee-foundation", "description": "Build strong fundamentals for JEE preparation.", "category": "competitive-exams", "status": Course.Status.PUBLISHED, "audience": Course.Audience.STUDENT, "class_range": "Class 9 - 12", "duration_hours": 120, "level": "Advanced", "instructor_idx": 0},
            {"title": "NEET Biology", "slug": "neet-biology", "description": "Complete NEET Biology syllabus with practice tests.", "category": "competitive-exams", "status": Course.Status.PUBLISHED, "audience": Course.Audience.STUDENT, "class_range": "Class 11 - 12", "duration_hours": 100, "level": "Advanced", "instructor_idx": 1},
            {"title": "Advanced Web Development", "slug": "advanced-web-development", "description": "MERN stack, HTML, CSS, JS, Node.js - full stack development course.", "category": "programming", "status": Course.Status.PUBLISHED, "audience": Course.Audience.STUDENT, "class_range": "", "duration_hours": 120, "level": "Advanced", "instructor_idx": 0},
            {"title": "Python for Beginners", "slug": "python-for-beginners", "description": "Learn Python from scratch with hands-on projects.", "category": "programming", "status": Course.Status.PUBLISHED, "audience": Course.Audience.STUDENT, "class_range": "All levels", "duration_hours": 60, "level": "Beginner", "instructor_idx": 1},
            {"title": "CBSE Physics Class 10", "slug": "cbse-physics-class-10", "description": "Complete CBSE Physics syllabus for Class 10 board exams.", "category": "school-tuition", "status": Course.Status.PUBLISHED, "audience": Course.Audience.STUDENT, "class_range": "Class 10", "duration_hours": 80, "level": "Intermediate", "instructor_idx": 2},
            {"title": "Art & Craft for Kids", "slug": "art-craft-kids", "description": "Creative art and craft activities for young learners.", "category": "courses-for-kids", "status": Course.Status.PUBLISHED, "audience": Course.Audience.KIDS, "class_range": "Class KG - 5", "duration_hours": 30, "level": "Beginner", "instructor_idx": 2},
        ]

        for data in courses_data:
            cat_slug = data.pop("category")
            instr_idx = data.pop("instructor_idx", 0)
            data["category"] = created_cats[cat_slug]
            data["instructor"] = instructors[instr_idx]
            course, created = Course.objects.get_or_create(
                slug=data["slug"],
                defaults=data,
            )
            if created:
                self.stdout.write(f"  Created course: {course.title}")

        self.stdout.write(self.style.SUCCESS("Seed data completed."))
