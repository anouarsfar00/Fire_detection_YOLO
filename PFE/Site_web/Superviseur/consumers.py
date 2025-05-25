import json
import cv2
import base64
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from .models import Cam
from .views import get_pandas, model  # Assure-toi que `model` est bien chargé dans views.py

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = False

    async def disconnect(self, close_code):
        self.running = False
        if hasattr(self, 'video') and self.video.isOpened():
            self.video.release()

    async def receive(self, text_data):
        data = json.loads(text_data)
        cam_name = data.get('cam_name')
        
        try:
            cam = Cam.objects.get(name_cam=cam_name)
            rtsp_url = cam.custom_url if cam.is_full_rtsp_url else f"rtsp://{cam.adresse_cam}:{cam.num_port}{cam.rest_de_path}"
        except Cam.DoesNotExist:
            await self.send(text_data=json.dumps({'error': 'Camera not found.'}))
            return

        # Initialisation caméra
        self.video = cv2.VideoCapture(rtsp_url)
        self.running = True

        while self.running:
            grabbed, frame = self.video.read()
            if not grabbed:
                await self.send(text_data=json.dumps({'error': 'Frame not available'}))
                await asyncio.sleep(1)
                continue

            # Traitement via YOLOv8 sans stream_buffer
            results = model.predict(frame, conf=0.4)
            res_plotted = results[0].plot()
            _, buffer = cv2.imencode('.jpg', res_plotted)

            # Encodage en base64 pour WebSocket
            frame_b64 = base64.b64encode(buffer).decode('utf-8')

            # Analyse des résultats
            result_df, _ = get_pandas(results, cam_name)

            await self.send(text_data=json.dumps({
                'frame': frame_b64,
                'detections': result_df.to_dict(orient='records'),
            }))

            await asyncio.sleep(0.1)  # Ajustez selon besoin
