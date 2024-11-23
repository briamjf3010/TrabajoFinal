from flask import Flask, Response, render_template
from ultralytics import YOLO
import cv2


# Configuración del modelo como clase separada (Principio SRP - Single Responsibility)
class YOLOModel:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame)
        return results[0].plot()


# Clase para manejar la cámara (Abstracción y facilidad de pruebas)
class Camera:
    def __init__(self, camera_index=1):
        self.camera = cv2.VideoCapture(camera_index)

    def get_frame(self):
        success, frame = self.camera.read()
        if not success:
            raise RuntimeError("No se pudo capturar el frame de la cámara")
        return frame

    def release(self):
        self.camera.release()


# Configuración de Flask App
app = Flask(__name__)

# Instancias globales (Inyección de dependencias)
yolo_model = YOLOModel(r'C:\Users\steven\Downloads\Jimenez_BriamMonedero_Steven\Jimenez_Briam&Monedero_Steven\best (3).pt')
camera = Camera()


def generate_frames():
    try:
        while True:
            frame = camera.get_frame()

            # Procesa el frame con el modelo
            annotated_frame = yolo_model.detect(frame)

            # Convierte el frame a JPEG
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()

            # Devuelve el frame en formato streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except RuntimeError as e:
        print(f"Error en el stream: {e}")
    finally:
        camera.release()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Punto de entrada
if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        camera.release()  # Asegura que la cámara se libere al finalizar
