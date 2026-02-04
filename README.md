# Detector y contador de vehículos (OpenCV) 🚗🛣️

![OpenCV + Python](https://img.shields.io/badge/OpenCV-Python%203.13-blue?logo=opencv)

Este proyecto consiste en un sistema de visión artificial capaz de detectar y contar vehículos que circulan por una autopista, diferenciando el conteo por carriles. Ha sido desarrollado para la asignatura **Fundamentos de Sistemas Inteligentes (FSI)** en el Grado de Ciencia e Ingeniería de Datos de la **ULPGC**.

## 📌 Descripción
El programa procesa un flujo de vídeo y utiliza técnicas de procesamiento digital de imágenes para identificar el movimiento, rastrear los vehículos y registrar cuántos cruzan líneas de detección específicas configuradas para tres carriles distintos.

## 🚀 Demostración en Vivo
Mira el sistema en acción detectando y contando vehículos en tiempo real:

![Demo del Contador de Vehículos](App/demoapp.gif)

## 🚀 Características
* **Detección de Movimiento:** Utiliza el sustractor de fondo `MOG2` para aislar objetos en movimiento.
* **Procesamiento Morfológico:** Aplicación de filtros para eliminar ruido y mejorar la precisión de los contornos.
* **Lógica de Conteo:** Sistema basado en el seguimiento del centroide del vehículo para evitar dobles conteos.
* **Multicarril:** Configuración independiente para 3 carriles con visualización de datos en tiempo real.

## 🛠️ Tecnologías Utilizadas
* **Python 3.x**
* **OpenCV:** Para el procesamiento de vídeo y visión artificial.
* **NumPy:** Para el manejo eficiente de matrices y cálculos de distancia euclidiana.

## 📂 Estructura del Repositorio
```text
.
├── App/
│   ├── app.py           # Script principal del programa
│   └── trafico01.mp4    # Vídeo de muestra para procesamiento
└── README.md            # Documentación del proyecto

```
## ⚙️ Funcionamiento
1. **Sustracción de fondo:** Se genera una máscara binaria de los objetos en movimiento.
2. **Detección de Contornos:** Se identifican los "blobs" que superan un área mínima definida para ser considerados vehículos.
3. **Clase Coche:** Cada detección se instancia como un objeto con propiedades de posición y centro.
4. **Validación de Cruce:** Si el centro del vehículo entra en el rango de coordenadas de una línea de carril, se incrementa el contador correspondiente.

## 🔧 Instalación y Uso
1. **Clona el repositorio:**
   ```bash
   git clone [https://github.com/aythamilorenzo/Contador-vehiculos-FSI-ULPGC.git](https://github.com/aythamilorenzo/Contador-vehiculos-FSI-ULPGC.git)
  
2. **Instala las dependencias necesarias:**
   ```bash
   pip install opencv-python numpy

3. **Ejecuta la aplicación:**
   ```bash
   python App/app.py
