"""AttendanceSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views #import this
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404
from django.views.static import serve
from django.urls import re_path as url
import cv2
import numpy as np
from PIL import ImageDraw,Image
from PIL import Image
import numpy as np
import cv2
from facenet_pytorch import MTCNN
from django.http import StreamingHttpResponse


class FaceDetector(object):
    """
    Face detector class
    """

    def __init__(self, mtcnn):
        self.mtcnn = mtcnn

    def _draw(self, frame, boxes, probs, landmarks):
        """
        Draw landmarks and boxes for each face detected
        """
        try:
            draw = ImageDraw.Draw(frame)
            for box, prob, ld in zip(boxes, probs, landmarks):
                draw.rectangle(((box[0],box[1]),(box[2],box[3])),outline=(255,0,0),width=5)
                
                draw.text((box[2],box[3]),str(prob))
                
        except:
            pass

        return frame
    
    def detect(self,frame):
        boxes, probs, landmarks = self.mtcnn.detect(frame, landmarks=True)
        return boxes, probs, landmarks


    def run(self,frame):
        """
            Run the FaceDetector and draw landmarks and boxes around detected faces
        """
        # draw on frame
        boxes, probs, landmarks = self.detect(frame)
        
        self._draw(frame, boxes, probs, landmarks)
        

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):


        mtcnn = MTCNN()
        fcd = FaceDetector(mtcnn)
        ret, frame = self.video.read()
        try:
            
            image = Image.fromarray(frame)
            fcd.run(image)
            frame = np.array(image)

            
        except:
            pass
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    #path('', include('django.contrib.auth.urls')),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='base/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="base/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='base/password_reset_complete.html'), name='password_reset_complete'),
    url(r'^images/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('face-recognition/', lambda r: StreamingHttpResponse(gen(VideoCamera()),
                                                     content_type='multipart/x-mixed-replace; boundary=frame')),
    url(r'^', include('favicon.urls')),

]
      

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
handler404 = "base.views.handle_not_found"

