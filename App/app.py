import cv2
import numpy as np


class Coche:
    """
    Clase para encapsular las características de un vehículo detectado.
    """
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.centro_x = x + w // 2
        self.centro_y = y + h // 2
        self.centro = (self.centro_x, self.centro_y)

    def dibujar(self, frame):
        """
        Dibuja el recuadro del vehículo y su punto central en el frame.
        """
        # Dibujar rectángulo (Fino: thickness=1)
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 255, 0), 1)
        # Dibujar centro
        cv2.circle(frame, self.centro, 3, (255, 0, 0), -1)

    def obtener_centro(self):
        return self.centro


def es_nuevo_coche(centro_detectado, centros_registrados, dist_min=30):
    """
    Verifica si un centro detectado está lo suficientemente lejos de los centros
    ya registrados para considerarse un nuevo vehículo.
    """
    for c, vida in centros_registrados:
        # Calculamos la distancia euclidiana
        distancia = np.linalg.norm(np.array(centro_detectado) - np.array(c))
        if distancia < dist_min:
            return False
    return True


def procesar_trafico(video_path, carriles_config, min_area=800, offset=10, frame_size=(640, 480)):
    """
    Función principal para procesar el video y contar vehículos usando la clase Coche.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error al abrir el video: {video_path}")
        print("Asegúrate de que el archivo existe o cambia 'ruta_video' en el main.")
        return

    # Inicializar el substractor de fondo
    fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50, detectShadows=True)

    # Kernel para operaciones morfológicas
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Redimensionar frame
            frame = cv2.resize(frame, frame_size)

            # Pre-procesamiento de imagen
            fgmask = fgbg.apply(frame)
            _, fgmask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)

            # Limpieza de ruido
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

            # Dibujar líneas de detección configuradas
            for carril in carriles_config:
                for linea in carril["lineas"]:
                    cv2.line(frame, (linea["inicio"], linea["posicion"]),
                             (linea["fin"], linea["posicion"]), carril["color"], 2)

            # Detectar contornos
            contornos, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contorno in contornos:
                area = cv2.contourArea(contorno)
                if area < min_area:
                    continue

                # --- INSTANCIACIÓN DE LA CLASE COCHE ---
                x, y, w, h = cv2.boundingRect(contorno)
                vehiculo = Coche(x, y, w, h)

                # Usamos el método de la clase para dibujar
                vehiculo.dibujar(frame)

                # Verificar cruce en cada carril configurado
                for carril in carriles_config:
                    for linea in carril["lineas"]:
                        # Comprobar si el centro del OBJETO vehículo está dentro de los límites
                        dentro_x = linea["inicio"] <= vehiculo.centro_x <= linea["fin"]
                        dentro_y = (linea["posicion"] - offset) <= vehiculo.centro_y <= (linea["posicion"] + offset)

                        if dentro_x and dentro_y:
                            if es_nuevo_coche(vehiculo.centro, carril["centros"]):
                                carril["contador"] += 1
                                # Añadir centro con 'vida' de 15 frames para evitar reconteo inmediato
                                carril["centros"].append((vehiculo.centro, 15))

            # Actualizar vida de los centros registrados (limpieza de memoria)
            # Esto reduce la 'vida' de los puntos detectados frame a frame
            for carril in carriles_config:
                carril["centros"] = [(c, vida - 1) for c, vida in carril["centros"] if vida > 1]

            # Dibujar contadores en pantalla
            for i, carril in enumerate(carriles_config):
                texto = f'{carril["nombre"]}: {carril["contador"]}'
                cv2.putText(frame, texto, (10, 50 + i * 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, carril["color"], 2)

            # Mostrar ventanas
            cv2.imshow("Trafico Detectado", frame)
            cv2.imshow("Mascara Blobs", fgmask) # Descomentar para ver la máscara binaria

            if cv2.waitKey(30) & 0xFF == 27:  # ESC para salir
                break

    except Exception as e:
        print(f"Ocurrió un error durante la ejecución: {e}")

    finally:
        cap.release()
        cv2.destroyAllWindows()


def main():
    # --- Configuración ---
    # Asegúrate de tener este archivo o cambia el nombre a 0 para usar webcam
    ruta_video = 'App/trafico01.mp4'
    resolucion = (640, 480)
    area_minima = 800
    margen_cruce = 10
    

    # Configuración de carriles (Rojo, Verde, Azul)
    configuracion_carriles = [
        {
            "nombre": "Carril 1",
            "lineas": [
                {"posicion": 400, "inicio": 425, "fin": 430},  # Zona estrecha ejemplo
                {"posicion": 420, "inicio": 350, "fin": 500}  # Zona ancha
            ],
            "contador": 0,
            "centros": [],  # Lista para guardar tuplas ((x,y), vida)
            "color": (0, 0, 255)  # Rojo (BGR)
        },
        {
            "nombre": "Carril 2",
            "lineas": [
                {"posicion": 450, "inicio": 100, "fin": 300}
            ],
            "contador": 0,
            "centros": [],
            "color": (0, 165, 255)  # Naranja (BGR)
        },
        {
            "nombre": "Carril 3",
            "lineas": [
                {"posicion": 350, "inicio": 460, "fin": 600}
            ],
            "contador": 0,
            "centros": [],
            "color": (255, 0, 0)  # Azul (BGR)
        }
    ]

    # --- Ejecución ---
    procesar_trafico(ruta_video, configuracion_carriles, min_area=area_minima, offset=margen_cruce,
                     frame_size=resolucion)


if __name__ == "__main__":
    main()