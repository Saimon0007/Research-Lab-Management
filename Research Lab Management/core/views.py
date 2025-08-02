
from django.shortcuts import render
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Project, Publication, Grant

def index(request):
    return render(request, 'core/RLM.html')

def export_report(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="research_report.xlsx"'

    workbook = Workbook()

    # Projects worksheet
    projects_sheet = workbook.active
    projects_sheet.title = 'Projects'
    projects_sheet.append(['Name', 'Lead Researcher', 'Status', 'Start Date', 'End Date'])
    for project in Project.objects.all():
        projects_sheet.append([
            project.name,
            project.lead_researcher.username,
            project.get_status_display(),
            project.start_date,
            project.end_date,
        ])

    # Publications worksheet
    publications_sheet = workbook.create_sheet(title='Publications')
    publications_sheet.append(['Title', 'Authors', 'Journal/Conference', 'Year'])
    for publication in Publication.objects.all():
        publications_sheet.append([
            publication.title,
            publication.authors,
            publication.journal or publication.conference,
            publication.year,
        ])

    # Grants worksheet
    grants_sheet = workbook.create_sheet(title='Grants')
    grants_sheet.append(['Name', 'Funding Agency', 'Amount', 'Start Date', 'End Date'])
    for grant in Grant.objects.all():
        grants_sheet.append([
            grant.name,
            grant.funding_agency,
            grant.amount,
            grant.start_date,
            grant.end_date,
        ])

    workbook.save(response)
    return response
