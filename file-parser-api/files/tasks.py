import pandas as pd
import pdfplumber
from celery import shared_task
from django.core.files.base import ContentFile
from .models import File


@shared_task(bind=True)
def process_file(self, file_id):
    file_obj = File.objects.get(id=file_id)

    try:
        # Update status to processing
        file_obj.status = 'processing'
        file_obj.progress = 10
        file_obj.save()

        file_extension = file_obj.original_file.name.split('.')[-1].lower()

        # Parse based on file type
        if file_extension in ['csv', 'txt']:
            parse_csv_file(file_obj, self)
        elif file_extension in ['xlsx', 'xls']:
            parse_excel_file(file_obj, self)
        elif file_extension == 'pdf':
            parse_pdf_file(file_obj, self)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

        # Mark as completed
        file_obj.status = 'ready'
        file_obj.progress = 100
        file_obj.save()

    except Exception as e:
        file_obj.status = 'failed'
        file_obj.error_message = str(e)
        file_obj.save()
        raise e


def parse_csv_file(file_obj, task):
    # Update progress
    file_obj.progress = 30
    file_obj.save()

    # Parse CSV file
    df = pd.read_csv(file_obj.original_file.path)

    # Update progress
    file_obj.progress = 70
    file_obj.save()

    # Convert to JSON and save
    file_obj.parsed_data = df.to_dict('records')
    file_obj.save()


def parse_excel_file(file_obj, task):
    # Update progress
    file_obj.progress = 30
    file_obj.save()

    # Parse Excel file
    df = pd.read_excel(file_obj.original_file.path)

    # Update progress
    file_obj.progress = 70
    file_obj.save()

    # Convert to JSON and save
    file_obj.parsed_data = df.to_dict('records')
    file_obj.save()


def parse_pdf_file(file_obj, task):
    # Update progress
    file_obj.progress = 30
    file_obj.save()

    # Parse PDF file
    parsed_data = []
    with pdfplumber.open(file_obj.original_file.path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                parsed_data.append({"page": page.page_number, "content": text})

    # Update progress
    file_obj.progress = 70
    file_obj.save()

    # Save parsed data
    file_obj.parsed_data = parsed_data
    file_obj.save()