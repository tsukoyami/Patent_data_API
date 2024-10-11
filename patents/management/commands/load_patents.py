import csv
from django.core.management.base import BaseCommand
from patents.models import Patent
from datetime import datetime

class Command(BaseCommand):
    help = 'Load patent data from CSV file'

    def handle(self, *args, **kwargs):
        with open('data/ai_patents.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Patent.objects.create(
                    source=row['Source'],
                    date_published=datetime.strptime(row['Date Published'], '%Y-%m-%d'),
                    pages=int(row['Pages']),
                    title=row['Title'],
                    inventer=row['Inventer'],
                    filing_date=datetime.strptime(row['Filing Date'], '%Y-%m-%d'),
                    applicant_name=row['Applicant Name'],
                    patent_number=row['Patent Number'],
                    relevancy=float(row['Relevency'])
                )
        self.stdout.write(self.style.SUCCESS('Patent data loaded successfully!'))
