"""
Learnova LMS - Common Validation Functions
Reusable validators used across the project for consistency.
"""
import re
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class BaseValidator:
    """Base validator class for Django model validators."""

    def __call__(self, value):
        raise NotImplementedError("Subclasses must implement __call__")


@deconstructible
class MinLengthValidator(BaseValidator):
    """Validate minimum string length."""

    def __init__(self, min_length, message=None):
        self.min_length = min_length
        self.message = message or f"Must be at least {min_length} characters."

    def __call__(self, value):
        if value and len(str(value).strip()) < self.min_length:
            raise ValidationError(self.message)


@deconstructible
class MaxLengthValidator(BaseValidator):
    """Validate maximum string length."""

    def __init__(self, max_length, message=None):
        self.max_length = max_length
        self.message = message or f"Must be at most {max_length} characters."

    def __call__(self, value):
        if value and len(str(value)) > self.max_length:
            raise ValidationError(self.message)


@deconstructible
class RegexValidator(BaseValidator):
    """Validate against regex pattern."""

    def __init__(self, regex, message=None, flags=0):
        self.regex = re.compile(regex, flags)
        self.message = message or "Invalid format."

    def __call__(self, value):
        if value and not self.regex.match(str(value)):
            raise ValidationError(self.message)


# Common patterns
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_PATTERN = r'^\+?[\d\s\-()]{10,20}$'
SLUG_PATTERN = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
USERNAME_PATTERN = r'^[a-zA-Z0-9._]+$'


def validate_email_format(value):
    """Validate email format."""
    if not value:
        return
    if not re.match(EMAIL_PATTERN, value):
        raise ValidationError("Enter a valid email address.")


def validate_phone_format(value):
    """Validate phone number format."""
    if not value:
        return
    if not re.match(PHONE_PATTERN, str(value)):
        raise ValidationError("Enter a valid phone number.")


def validate_slug_format(value):
    """Validate URL slug format (lowercase, hyphens only)."""
    if not value:
        return
    if not re.match(SLUG_PATTERN, value):
        raise ValidationError("Slug must be lowercase with hyphens only (e.g., my-course-name).")


def validate_username_format(value):
    """Validate username format."""
    if not value:
        return
    if not re.match(USERNAME_PATTERN, value):
        raise ValidationError("Username can only contain letters, numbers, dots, and underscores.")
    if len(value) < 3:
        raise ValidationError("Username must be at least 3 characters.")


def validate_future_date(value):
    """Ensure date is in the future."""
    if value and value <= date.today():
        raise ValidationError("Date must be in the future.")


def validate_past_date(value):
    """Ensure date is in the past."""
    if value and value >= date.today():
        raise ValidationError("Date must be in the past.")


def validate_date_range(start_date, end_date):
    """Ensure end_date is after start_date."""
    if start_date and end_date and end_date <= start_date:
        raise ValidationError("End date must be after start date.")


def validate_percentage(value):
    """Validate percentage value (0-100)."""
    if value is not None and (value < 0 or value > 100):
        raise ValidationError("Percentage must be between 0 and 100.")


def validate_positive_number(value):
    """Validate positive number."""
    if value is not None and value < 0:
        raise ValidationError("Value must be positive.")


def validate_file_size(file, max_size_mb=10):
    """Validate uploaded file size."""
    if file and file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"File size must not exceed {max_size_mb} MB.")


def validate_video_duration(duration_seconds):
    """Validate video duration is reasonable (e.g., max 4 hours)."""
    if duration_seconds is not None and (duration_seconds < 0 or duration_seconds > 14400):
        raise ValidationError("Video duration must be between 0 and 4 hours.")


def validate_quiz_time_limit(minutes):
    """Validate quiz time limit (reasonable range)."""
    if minutes is not None and (minutes < 1 or minutes > 480):
        raise ValidationError("Time limit must be between 1 and 480 minutes (8 hours).")
