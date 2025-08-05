from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Grant(models.Model):
    name = models.CharField(max_length=255)
    funding_agency = models.CharField(max_length=255)
    grant_number = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class DataSet(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    data_location = models.URLField()
    metadata = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

class TrainingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_completed = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    attachment = models.FileField(upload_to='training_records/', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.name}'

class Protocol(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    attachment = models.FileField(upload_to='protocols/', null=True, blank=True)

    def __str__(self):
        return self.name

class Publication(models.Model):
    title = models.CharField(max_length=255)
    authors = models.TextField()
    journal = models.CharField(max_length=255, null=True, blank=True)
    conference = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField()
    doi = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

class Project(models.Model):
    STATUS_CHOICES = (
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    )
    name = models.CharField(max_length=255)
    lead_researcher = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    grant = models.ForeignKey(Grant, on_delete=models.SET_NULL, null=True, blank=True)
    publications = models.ManyToManyField(Publication, blank=True)
    eln_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    cas_number = models.CharField(max_length=255, null=True, blank=True)
    storage_conditions = models.CharField(max_length=255, null=True, blank=True)
    safety_data_sheet_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.item_name

class Staff(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name