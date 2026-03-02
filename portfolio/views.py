from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Project, ContactMessage
from .forms import ContactForm


def home(request):
    profile = Profile.objects.first()

    # projetos + tags (split aqui, não no template)
    projects_qs = Project.objects.filter(status="published").order_by("-created_at")[:3]
    projects = []
    for p in projects_qs:
        tags = []
        if p.tech_stack:
            tags = [t.strip() for t in p.tech_stack.split(",") if t.strip()]
        projects.append({"obj": p, "tags": tags})

    skills = profile.skills.all() if profile else []
    experiences = profile.experiences.all().order_by("-is_current", "-start_date")[:2] if profile else []
    educations = profile.educations.all().order_by("-start_date")[:1] if profile else []
    certifications = profile.certifications.all().order_by("-issue_date")[:3] if profile else []

    context = {
        "profile": profile,
        "projects": projects,
        "skills": skills,
        "experiences": experiences,
        "educations": educations,
        "certifications": certifications,
        "form": ContactForm(),
    }
    return render(request, "portfolio/index.html", context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, status="published")
    images = project.images.all()
    return render(request, "portfolio/project_detail.html", {"project": project, "images": images})


def submit_contact(request):
    profile = Profile.objects.first()
    if request.method != "POST":
        return redirect("portfolio:home")

    form = ContactForm(request.POST)
    if form.is_valid() and profile:
        ContactMessage.objects.create(
            profile=profile,
            name=form.cleaned_data["name"],
            email=form.cleaned_data["email"],
            subject=form.cleaned_data["subject"],
            message=form.cleaned_data["message"],
        )
        return redirect("portfolio:home")

    # se inválido, re-renderiza com erros
    projects_qs = Project.objects.filter(status="published").order_by("-created_at")[:3]
    projects = []
    for p in projects_qs:
        tags = []
        if p.tech_stack:
            tags = [t.strip() for t in p.tech_stack.split(",") if t.strip()]
        projects.append({"obj": p, "tags": tags})

    skills = profile.skills.all() if profile else []
    experiences = profile.experiences.all().order_by("-is_current", "-start_date")[:2] if profile else []
    educations = profile.educations.all().order_by("-start_date")[:1] if profile else []
    certifications = profile.certifications.all().order_by("-issue_date")[:3] if profile else []

    return render(request, "portfolio/index.html", {
        "profile": profile,
        "projects": projects,
        "skills": skills,
        "experiences": experiences,
        "educations": educations,
        "certifications": certifications,
        "form": form,
    })