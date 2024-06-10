from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Profile, Skill

from django.contrib import auth

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.utils.dateparse import parse_date


def register(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        cpassword = req.POST.get('password1')

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(req, 'This username already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password)
                user_profile = Profile.objects.create(user=user)
                messages.success(req, 'Your account has been created! You can now log in.')
                return redirect('login')
        else:
            messages.info(req, 'Passwords do not match')
            return redirect('register')

    return render(req, 'profiles/register.html')

@login_required
def profile(request):
    if request.method == 'POST':
        # Profile and skill updates
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        date_of_birth = request.POST.get('date_of_birth') or None
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')
        skills = request.POST.get('skills').split(',') if request.POST.get('skills') else []
        email = request.POST.get('email')

        if not first_name or not last_name:
            messages.error(request, 'First name and last name cannot be empty.')
            return redirect('profile')

        user = request.user
        user.first_name = first_name
        user.last_name = last_name

        if not user.profile.email_updated:
            user.email = email
        user.save()

        profile, created = Profile.objects.get_or_create(user=user)
        profile.date_of_birth = date_of_birth
        profile.gender = gender
        profile.address = address
        profile.phone_number = phone_number
        profile.bio = bio
        if profile_picture:
            profile.profile_picture = profile_picture
        profile.email_updated = True
        profile.save()

        # Update or create skills
        existing_skills = Skill.objects.filter(user=user)
        existing_skill_names = [skill.skill_name for skill in existing_skills]
        for skill_name in skills:
            if skill_name not in existing_skill_names:
                Skill.objects.create(user=user, skill_name=skill_name, proficiency_level='Beginner')

        project_ids = request.POST.getlist('project_id')
        project_titles = request.POST.getlist('project_title')
        project_descriptions = request.POST.getlist('project_description')
        project_links = request.POST.getlist('project_link')
        project_images = request.FILES.getlist('project_image')

        for i, (project_id, title, description, link) in enumerate(zip(project_ids, project_titles, project_descriptions, project_links)):
            if project_id:
                project = Project.objects.get(id=project_id, user=request.user)
                project.title = title
                project.description = description
                project.link = link
                if i < len(project_images):
                    project.image = project_images[i]
                project.save()
            elif title and description and link:
                Project.objects.create(user=request.user, title=title, description=description, link=link, image=project_images[i] if i < len(project_images) else None)
          
        # Work experience updates
        work_experience_ids = request.POST.getlist('work_experience_id')
        work_experience_positions = request.POST.getlist('work_experience_position')
        work_experience_descriptions = request.POST.getlist('work_experience_description')
        work_experience_companies = request.POST.getlist('work_experience_company')
        work_experience_start_dates = request.POST.getlist('work_experience_start_date')
        work_experience_end_dates = request.POST.getlist('work_experience_end_date')
        for work_experience_id, position, description, company, start_date, end_date in zip(work_experience_ids, work_experience_positions, work_experience_descriptions, work_experience_companies, work_experience_start_dates, work_experience_end_dates):
            start_date = start_date or None
            end_date = end_date or None
            if work_experience_id:
                work_experience = WorkExperience.objects.get(id=work_experience_id, user=user)
                work_experience.position = position
                work_experience.description = description
                work_experience.company = company
                work_experience.start_date = start_date
                work_experience.end_date = end_date
                work_experience.save()
            elif position and description and company:
                WorkExperience.objects.create(user=user, position=position, description=description, company=company, start_date=start_date, end_date=end_date)
        
        # Education updates
        education_ids = request.POST.getlist('education_id')
        education_degrees = request.POST.getlist('education_degree')
        education_descriptions = request.POST.getlist('education_description')
        education_institutions = request.POST.getlist('education_institution')
        education_start_dates = request.POST.getlist('education_start_date')
        education_end_dates = request.POST.getlist('education_end_date')
        for education_id, degree, description, institution, start_date, end_date in zip(education_ids, education_degrees, education_descriptions, education_institutions, education_start_dates, education_end_dates):
            start_date = start_date or None
            end_date = end_date or None
            if education_id:
                education = Education.objects.get(id=education_id, user=user)
                education.degree = degree
                education.description = description
                education.institution = institution
                education.start_date = start_date
                education.end_date = end_date
                education.save()
            elif degree and description and institution:
                Education.objects.create(user=user, degree=degree, description=description, institution=institution, start_date=start_date, end_date=end_date)
        
        # Certification updates
        certification_ids = request.POST.getlist('certification_id')
        certification_titles = request.POST.getlist('certification_title')
        certification_descriptions = request.POST.getlist('certification_description')
        certification_organizations = request.POST.getlist('certification_organization')
        certification_issue_dates = request.POST.getlist('certification_issue_date')
        certification_expiry_dates = request.POST.getlist('certification_expiry_date')
        for certification_id, title, description, organization, issue_date, expiry_date in zip(certification_ids, certification_titles, certification_descriptions, certification_organizations, certification_issue_dates, certification_expiry_dates):
            issue_date = issue_date or None
            expiry_date = expiry_date or None
            if certification_id:
                certification = Certification.objects.get(id=certification_id, user=user)
                certification.title = title
                certification.description = description
                certification.issuing_organization = organization
                certification.issue_date = issue_date
                certification.expiration_date = expiry_date
                certification.save()
            elif title and description and organization:
                Certification.objects.create(user=user, title=title, description=description, issuing_organization=organization, issue_date=issue_date, expiration_date=expiry_date)

        messages.success(request, 'Your profile has been updated!')
        return redirect('profile')

    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    skills = Skill.objects.filter(user=user)
    projects = Project.objects.filter(user=user)
    work_experiences = WorkExperience.objects.filter(user=user)
    educations = Education.objects.filter(user=user)
    certifications = Certification.objects.filter(user=user)

    context = {
        'user': user,
        'profile': profile,
        'skills': skills,
        'projects': projects,
        'work_experiences': work_experiences,
        'educations': educations,
        'certifications': certifications,
    }

    return render(request, 'profiles/profile.html', context)




def logout(req):
    auth.logout(req)

    return redirect('login')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully.')
            return redirect('profile') 
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'profiles/login.html')

@login_required
def home(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    skills = Skill.objects.filter(user=user)
    projects = Project.objects.filter(user=user)
    work_experiences = WorkExperience.objects.filter(user=user)
    educations = Education.objects.filter(user=user)
    certifications = Certification.objects.filter(user=user)

    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
        'work_experiences': work_experiences,
        'educations': educations,
        'certifications': certifications,
    }
    return render(request, 'profiles/home.html', context)

from django.shortcuts import render
from .models import Profile, Skill, Project, WorkExperience, Education, Certification

def public_home(request):
    profiles = Profile.objects.exclude(user__is_superuser=True)

    # Preload related data for each profile
    for profile in profiles:
        profile.skills = Skill.objects.filter(user=profile.user)
        profile.projects = Project.objects.filter(user=profile.user)
        profile.work_experiences = WorkExperience.objects.filter(user=profile.user)
        profile.educations = Education.objects.filter(user=profile.user)
        profile.certifications = Certification.objects.filter(user=profile.user)

    context = {
        'profiles': profiles,
    }
    return render(request, 'profiles/public_home.html', context)
