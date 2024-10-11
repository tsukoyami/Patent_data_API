from django.db import models

class Patent(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=255)
    date_published = models.DateField()
    pages = models.IntegerField()
    title = models.CharField(max_length=500)
    inventer = models.CharField(max_length=255)
    filing_date = models.DateField()
    applicant_name = models.CharField(max_length=255)
    patent_number = models.CharField(max_length=100)
    relevancy = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.patent_number} - {self.title}"
