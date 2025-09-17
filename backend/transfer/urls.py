from django.urls import path
from . import views

urlpatterns = [
    # Ví dụ: URL để upload file
    # URL đầy đủ sẽ là /api/upload/
    path('upload/', views.upload_file, name='upload_file'),

    # Ví dụ: URL để download file
    # URL đầy đủ sẽ là /api/download/
    path('download/', views.download_file, name='download_file'),
]
