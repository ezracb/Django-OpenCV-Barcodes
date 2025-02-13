import os
import time
from datetime import datetime

from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from PIL import Image
from pyzbar.pyzbar import decode
from utils.camera_streaming_widget import CameraStreamingWidget


# Camera feed 0
def camera_feed(request):
    stream = CameraStreamingWidget(0)
    frames = stream.get_frames()

    # if ajax request is sent
    if request.is_ajax():
        print('Ajax request received')
        time_stamp = str(datetime.now().strftime("%d-%m-%y"))
        image = os.path.join(os.getcwd(), "media",
                             "images", f"img_{time_stamp}.png")
        if os.path.exists(image):
            # open image if exists
            im = Image.open(image)
            # decode barcode
            if decode(im):
                for barcode in decode(im):
                    barcode_data = (barcode.data).decode('utf-8')
                    file_saved_at = time.ctime(os.path.getmtime(image))
                    # return decoded barcode as json response
                    return JsonResponse(data={'barcode_data': barcode_data, 'file_saved_at': file_saved_at})
            else:
                return JsonResponse(data={'barcode_data': None})
        else:
            return JsonResponse(data={'barcode_data': None})
    # else stream the frames from camera feed
    else:
        return StreamingHttpResponse(frames, content_type='multipart/x-mixed-replace; boundary=frame')

# Camera feed 1
def camera_feed_1(request):
    stream = CameraStreamingWidget(1)
    frames = stream.get_frames()

    return StreamingHttpResponse(frames, content_type='multipart/x-mixed-replace; boundary=frame')


def detect(request):
    stream = CameraStreamingWidget(0)
    stream1 = CameraStreamingWidget(1)
    success, frame = stream.camera.read()
    success1, frame1 = stream1.camera.read()
    if success:
        status = True
    else:
        status = False
    if success1:
        status1 = True
    else:
        status1 = False
    return render(request, 'detect_barcodes/detect.html', context={'cam_status': status, 'cam_status_1': status1})
