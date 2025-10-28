import cv2
import numpy as np

def extraer_fondo(video):
    cap = cv2.VideoCapture(video)
    
    ret, frame = cap.read()
    if not ret:
        print("Error: no se pudo leer el video.")
        return
    
    avg_frame = np.zeros_like(frame, np.float32)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        avg_frame += frame.astype(np.float32)
        count += 1

    cap.release()
    
    background = avg_frame / count
    background = cv2.convertScaleAbs(background)
    
    cv2.imshow("Background", background)
    cv2.imwrite("background.jpg", background)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def detectar_coches(video, background, min_area):
    # Cargar fondo y convertir a escala de grises
    fondo = cv2.imread(background)
    fondo_gray = cv2.cvtColor(fondo, cv2.COLOR_BGR2GRAY)
    
    cap = cv2.VideoCapture(video)
    cv2.namedWindow("Detección de coches", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Detección de coches", 960, 540)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convertimos el frame a gris
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Restamos el fondo
        diff = cv2.absdiff(gray, fondo_gray)
        
        # Suavizamos un poco para reducir ruido (Gaussian Blur)
        blur = cv2.GaussianBlur(diff, (5, 5), 0)
        
        # Umbralizamos: todo lo diferente al fondo se vuelve blanco
        _, umbralizado = cv2.threshold(blur, 42, 255, cv2.THRESH_BINARY)
        # También puedes probar threshold adaptativo si la luz cambia mucho:
        # thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #                                cv2.THRESH_BINARY, 11, 2)

        # Operaciones morfológicas para limpiar ruido
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        
        # Dilatar para rellenar huecos
        dilatado = cv2.dilate(umbralizado, kernel, iterations=2)
        
         # Cerrar para unir regiones cercanas
        cerrado = cv2.morphologyEx(dilatado, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        # Abrir para eliminar ruido suelto
        umbralizado = cv2.morphologyEx(cerrado, cv2.MORPH_OPEN, kernel, iterations=1)
        
    
        
        mask = np.zeros_like(umbralizado, dtype=np.uint8)

        # Ejemplo: solo analizar desde Y=300 hasta el final (ignorar el fondo lejano)
        # y excluir los últimos 120 px de la esquina inferior derecha donde están los números
        alto, ancho = umbralizado.shape
        cv2.rectangle(mask, (0, 320), (ancho, alto - 120), 255, -1)

        # Aplicamos la máscara
        umbralizado = cv2.bitwise_and(umbralizado, mask)

        # (Opcional) Visualizar la ROI
        # frame_masked = cv2.bitwise_and(frame, frame, mask=mask)
        # cv2.imshow("ROI", frame_masked)
        

        contornos, _ = cv2.findContours(umbralizado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contorno in contornos:
            area = cv2.contourArea(contorno)
            if area > min_area:
                x, y, w, h = cv2.boundingRect(contorno)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)                
        
        # Mostrar resultado
        cv2.imshow("Detección de coches", umbralizado)
        cv2.imshow("Blops marcados", frame)
        
        # Salir con 'q'
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    # extraer_fondo("OpenCV-Perception/trafico01.mp4")
    detectar_coches('OpenCV-Perception/trafico01.mp4', 'background.jpg', 500)
    

if __name__ == '__main__':
    main()
    
    