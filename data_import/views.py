from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import ImportJob, ImportMapping
from .services import DataImportService
import json


class ImportDashboardView(LoginRequiredMixin, TemplateView):
    """Data import dashboard"""
    template_name = 'data_import/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_imports'] = ImportJob.objects.filter(
            user=self.request.user
        ).order_by('-created_at')[:10]
        
        # Import statistics
        context['import_stats'] = {
            'total_imports': ImportJob.objects.filter(user=self.request.user).count(),
            'successful_imports': ImportJob.objects.filter(
                user=self.request.user, status='completed'
            ).count(),
            'pending_imports': ImportJob.objects.filter(
                user=self.request.user, status='processing'
            ).count(),
            'failed_imports': ImportJob.objects.filter(
                user=self.request.user, status='failed'
            ).count(),
        }
        
        return context


class ImportJobListView(LoginRequiredMixin, ListView):
    """List all import jobs for the user"""
    model = ImportJob
    template_name = 'data_import/job_list.html'
    context_object_name = 'import_jobs'
    paginate_by = 20
    
    def get_queryset(self):
        return ImportJob.objects.filter(
            user=self.request.user
        ).order_by('-created_at')


class CreateImportView(LoginRequiredMixin, TemplateView):
    """Create new import job"""
    template_name = 'data_import/create_import.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['import_mappings'] = ImportMapping.objects.filter(
            user=self.request.user
        )
        return context
    
    def post(self, request, *args, **kwargs):
        # Handle file upload and create import job
        uploaded_file = request.FILES.get('import_file')
        import_type = request.POST.get('import_type', 'csv')
        mapping_id = request.POST.get('mapping_id')
        
        if not uploaded_file:
            messages.error(request, 'Please select a file to import.')
            return self.get(request, *args, **kwargs)
        
        # Validate file type
        if import_type == 'csv' and not uploaded_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
            return self.get(request, *args, **kwargs)
        
        if import_type == 'json' and not uploaded_file.name.endswith('.json'):
            messages.error(request, 'Please upload a JSON file.')
            return self.get(request, *args, **kwargs)
        
        # Save uploaded file
        file_path = default_storage.save(
            f'imports/{request.user.id}/{uploaded_file.name}',
            ContentFile(uploaded_file.read())
        )
        
        # Create import job
        import_job = ImportJob.objects.create(
            user=request.user,
            file_path=file_path,
            file_type=import_type,
            original_filename=uploaded_file.name,
            mapping_id=mapping_id if mapping_id else None,
            options=json.loads(request.POST.get('options', '{}'))
        )
        
        # Start import process
        try:
            service = DataImportService()
            service.process_import_async(import_job)
            messages.success(request, 'Import job created successfully. Processing will begin shortly.')
        except Exception as e:
            import_job.status = 'failed'
            import_job.error_message = str(e)
            import_job.save()
            messages.error(request, f'Failed to start import: {str(e)}')
        
        return redirect('import_job_detail', pk=import_job.id)


class ImportJobDetailView(LoginRequiredMixin, TemplateView):
    """View import job details"""
    template_name = 'data_import/job_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            job_id = self.kwargs['pk']
            context['import_job'] = ImportJob.objects.get(
                id=job_id, user=self.request.user
            )
        except ImportJob.DoesNotExist:
            messages.error(self.request, 'Import job not found.')
        
        return context


class CreateMappingView(LoginRequiredMixin, TemplateView):
    """Create new field mapping"""
    template_name = 'data_import/create_mapping.html'
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        mapping_data = request.POST.get('mapping_data')
        
        if not name or not mapping_data:
            messages.error(request, 'Please provide mapping name and data.')
            return self.get(request, *args, **kwargs)
        
        try:
            mapping_dict = json.loads(mapping_data)
            
            ImportMapping.objects.create(
                user=request.user,
                name=name,
                description=request.POST.get('description', ''),
                mapping=mapping_dict
            )
            
            messages.success(request, 'Field mapping created successfully.')
            return redirect('import_dashboard')
            
        except json.JSONDecodeError:
            messages.error(request, 'Invalid JSON format in mapping data.')
            return self.get(request, *args, **kwargs)


@login_required
def download_template(request):
    """Download CSV/JSON template for imports"""
    template_type = request.GET.get('type', 'csv')
    
    if template_type == 'csv':
        # Create CSV template
        template_content = '''name,description,address,city,postal_code,country,phone,email,website,category
"Example Business","A sample business description","123 Main St","Paris","75001","France","+33123456789","info@example.com","https://example.com","Restaurant"
'''
        response = HttpResponse(template_content, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="business_import_template.csv"'
        
    elif template_type == 'json':
        # Create JSON template
        template_data = [
            {
                "name": "Example Business",
                "description": "A sample business description",
                "address": "123 Main St",
                "city": "Paris",
                "postal_code": "75001",
                "country": "France",
                "phone": "+33123456789",
                "email": "info@example.com",
                "website": "https://example.com",
                "category": "Restaurant"
            }
        ]
        
        response = HttpResponse(
            json.dumps(template_data, indent=2),
            content_type='application/json'
        )
        response['Content-Disposition'] = 'attachment; filename="business_import_template.json"'
    
    else:
        return JsonResponse({'error': 'Invalid template type'}, status=400)
    
    return response


@login_required
def import_job_status(request, job_id):
    """Get import job status via AJAX"""
    try:
        job = ImportJob.objects.get(id=job_id, user=request.user)
        
        return JsonResponse({
            'status': job.status,
            'progress': job.progress,
            'total_records': job.total_records,
            'processed_records': job.processed_records,
            'successful_records': job.successful_records,
            'failed_records': job.failed_records,
            'error_message': job.error_message,
            'completed_at': job.completed_at.isoformat() if job.completed_at else None
        })
        
    except ImportJob.DoesNotExist:
        return JsonResponse({'error': 'Import job not found'}, status=404)


@login_required
def cancel_import_job(request, job_id):
    """Cancel an import job"""
    try:
        job = ImportJob.objects.get(id=job_id, user=request.user)
        
        if job.status in ['pending', 'processing']:
            job.status = 'cancelled'
            job.save()
            messages.success(request, 'Import job cancelled.')
        else:
            messages.error(request, 'Cannot cancel completed import job.')
            
    except ImportJob.DoesNotExist:
        messages.error(request, 'Import job not found.')
    
    return redirect('import_job_detail', pk=job_id)


@login_required
def delete_import_job(request, job_id):
    """Delete an import job"""
    try:
        job = ImportJob.objects.get(id=job_id, user=request.user)
        
        # Delete associated file
        if job.file_path and default_storage.exists(job.file_path):
            default_storage.delete(job.file_path)
        
        job.delete()
        messages.success(request, 'Import job deleted.')
        
    except ImportJob.DoesNotExist:
        messages.error(request, 'Import job not found.')
    
    return redirect('import_job_list')