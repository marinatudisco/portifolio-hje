from django.db import models
from django.utils.text import slugify


class Profile(models.Model):
    full_name = models.CharField(max_length=200)
    headline = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)

    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    cv_url = models.URLField(blank=True)
    profile_photo_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("frontend", "Frontend"),
        ("backend", "Backend"),
        ("data", "Data"),
        ("devops", "DevOps"),
        ("soft", "Soft Skills"),
        ("biomed", "Biomed"),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=80)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="backend")
    level = models.PositiveSmallIntegerField(default=3)  # 1–5
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return f"{self.name} ({self.category})"


class Project(models.Model):
    STATUS_CHOICES = [("draft", "Draft"), ("published", "Published")]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)

    summary = models.CharField(max_length=280, blank=True)
    description = models.TextField(blank=True)

    repo_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)

    tech_stack = models.CharField(max_length=300, blank=True)  # ex: "Django,Postgres,HTML"
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="published")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            i = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField()
    caption = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"Image {self.id} - {self.project.title}"


class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="experiences")
    company = models.CharField(max_length=150)
    position = models.CharField(max_length=150)
    location = models.CharField(max_length=120, blank=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)

    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-is_current", "-start_date", "company"]

    def __str__(self):
        return f"{self.position} @ {self.company}"


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="educations")
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=120, blank=True)
    field = models.CharField(max_length=160, blank=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_date", "institution"]

    def __str__(self):
        return self.institution


class Certification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="certifications")
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=160, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True)

    class Meta:
        ordering = ["-issue_date", "name"]

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    STATUS_CHOICES = [("new", "New"), ("read", "Read"), ("replied", "Replied")]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="messages")
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} ({self.email})"