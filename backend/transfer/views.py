from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import os
from .ftp_client import upload_file_to_ftp, download_file_from_ftp
from .tftp_client import upload_file_to_tftp, download_file_from_tftp

# Thư mục lưu file upload
UPLOAD_DIR = os.path.join(settings.BASE_DIR, 'media', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại


@csrf_exempt
@require_http_methods(["POST"])
def upload_file(request):
    """
    API: Upload file từ client lên server rồi chuyển tiếp đến máy ảo.
    """
    file = request.FILES.get('file')
    protocol = request.POST.get('protocol', 'ftp')
    
    if not file:
        return JsonResponse({'status': 'error', 'message': 'Không có file nào được tải lên.'}, status=400)

    filename = file.name
    local_filepath = os.path.join(UPLOAD_DIR, filename)
    
    # Lưu file tạm thời trên server Django
    with open(local_filepath, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # Chuyển file đến máy ảo theo protocol được chọn
    success = False
    message = ""
    
    if protocol.lower() == 'ftp':
        success, message = upload_file_to_ftp(local_filepath, filename)
    elif protocol.lower() == 'tftp':
        success, message = upload_file_to_tftp(local_filepath, filename)
    else:
        message = "Protocol không được hỗ trợ"
    
    # Xóa file tạm thời
    try:
        os.remove(local_filepath)
    except:
        pass
    
    if success:
        return JsonResponse({
            'status': 'success',
            'message': f"File '{filename}' đã được tải lên thành công qua {protocol.upper()}.",
            'filename': filename,
            'protocol': protocol
        })
    else:
        return JsonResponse({
            'status': 'error', 
            'message': f"Lỗi khi upload qua {protocol.upper()}: {message}"
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def download_file(request):
    """
    API: Download file từ máy ảo về client.
    """
    filename = request.GET.get('filename')
    protocol = request.GET.get('protocol', 'ftp')
    
    if not filename:
        return JsonResponse({'status': 'error', 'message': 'Vui lòng cung cấp tên file.'}, status=400)

    local_filepath = os.path.join(UPLOAD_DIR, filename)
    
    # Download file từ máy ảo về server Django
    success = False
    message = ""
    
    if protocol.lower() == 'ftp':
        success, message = download_file_from_ftp(filename, local_filepath)
    elif protocol.lower() == 'tftp':
        success, message = download_file_from_tftp(filename, local_filepath)
    else:
        return JsonResponse({'status': 'error', 'message': 'Protocol không được hỗ trợ'}, status=400)
    
    if not success:
        return JsonResponse({'status': 'error', 'message': f"Lỗi khi download: {message}"}, status=500)
    
    if not os.path.exists(local_filepath):
        return JsonResponse({'status': 'error', 'message': 'File không tồn tại sau khi download.'}, status=404)

    # Trả file về client
    response = FileResponse(open(local_filepath, 'rb'), as_attachment=True, filename=filename)
    
    # Xóa file tạm thời sau khi trả về
    def cleanup():
        try:
            os.remove(local_filepath)
        except:
            pass
    
    # Schedule cleanup (có thể dùng celery hoặc thread)
    import threading
    threading.Timer(5.0, cleanup).start()
    
    return response