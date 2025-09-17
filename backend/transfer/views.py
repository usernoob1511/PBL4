from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import os

# Thư mục lưu file upload
UPLOAD_DIR = os.path.join(settings.BASE_DIR, 'media', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại


@csrf_exempt
@require_http_methods(["POST"])
def upload_file(request):
    """
    API: Upload file từ client lên server.
    Gửi request dạng POST (multipart/form-data).
    """
    file = request.FILES.get('file')
    if not file:
        return JsonResponse({'status': 'error', 'message': 'Không có file nào được tải lên.'}, status=400)

    filename = file.name
    filepath = os.path.join(UPLOAD_DIR, filename)
    print(f"Saving file to: {filepath}")

    # Ghi file xuống server
    with open(filepath, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return JsonResponse({
        'status': 'success',
        'message': f"File '{filename}' đã được tải lên thành công.",
        'filename': filename
    })


@csrf_exempt
@require_http_methods(["GET"])
def download_file(request):
    """
    API: Download file từ server về client.
    Client gửi query ?filename=abc.txt
    """
    file_name = request.GET.get('filename')
    if not file_name:
        return JsonResponse({'status': 'error', 'message': 'Vui lòng cung cấp tên file.'}, status=400)

    filepath = os.path.join(UPLOAD_DIR, file_name)

    if not os.path.exists(filepath):
        return JsonResponse({'status': 'error', 'message': 'File không tồn tại.'}, status=404)

    # Trả file về client
    return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=file_name)
