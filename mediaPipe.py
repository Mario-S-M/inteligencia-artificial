import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=2, 
                                  min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Captura de video
cap = cv2.VideoCapture(0)

# Puntos de referencia para calcular el área facial (contorno aproximado)
contorno_cara = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 
                 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 
                 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]

# Puntos para medidas específicas
puntos_medidas = {
    'nariz': 1,                  # Punta de la nariz
    'cachete_izq': 123,          # Cachete izquierdo
    'cachete_der': 352,          # Cachete derecho
    'ojo_izq_sup': 159,          # Parte superior ojo izquierdo
    'ojo_der_sup': 386,          # Parte superior ojo derecho
    'boca_sup': 13,              # Labio superior
    'boca_inf': 14,              # Labio inferior
    'ojo_izq': 33,               # Ojo izquierdo (pupila)
    'ojo_der': 263,              # Ojo derecho (pupila)
    'frente': 10,                # Punto superior de la frente
    'barbilla': 152              # Punto inferior de la barbilla
}

def calcular_area_poligono(puntos):
    """Calcula el área de un polígono dado un conjunto de puntos."""
    if len(puntos) < 3:
        return 0.0
    x = puntos[:, 0]
    y = puntos[:, 1]
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

def dibujar_linea_con_texto(frame, p1, p2, texto, color):
    """Dibuja una línea entre dos puntos y coloca texto en el medio."""
    cv2.line(frame, p1, p2, color, 1)
    punto_medio = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
    cv2.putText(frame, texto, (punto_medio[0], punto_medio[1] - 5), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for i, face_landmarks in enumerate(results.multi_face_landmarks):
            puntos_contorno = []
            puntos = {}
            
            # Obtener puntos del contorno para área
            for idx in contorno_cara:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos_contorno.append([x, y])
                cv2.circle(frame, (x, y), 1, (0, 255, 255), -1)
            
            # Obtener puntos para medidas específicas
            for nombre, idx in puntos_medidas.items():
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos[nombre] = (x, y)
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
            
            # Calcular y mostrar área facial
            if len(puntos_contorno) > 2:
                area = calcular_area_poligono(np.array(puntos_contorno))
                cv2.putText(frame, f"Area facial: {int(area)} px", (10, 30 + i*120), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
            
            # Calcular y mostrar distancias específicas
            if all(k in puntos for k in ['nariz', 'cachete_izq', 'cachete_der']):
                # Distancia nariz a cachetes
                dist_izq = int(dist.euclidean(puntos['nariz'], puntos['cachete_izq']))
                dist_der = int(dist.euclidean(puntos['nariz'], puntos['cachete_der']))
                
                dibujar_linea_con_texto(frame, puntos['nariz'], puntos['cachete_izq'], 
                                       f"N-CI: {dist_izq}", (255, 0, 0))
                dibujar_linea_con_texto(frame, puntos['nariz'], puntos['cachete_der'], 
                                       f"N-CD: {dist_der}", (255, 0, 0))
                
                # Mostrar diferencia entre cachetes
                diferencia = abs(dist_izq - dist_der)
                cv2.putText(frame, f"Dif. cachetes: {diferencia}", (10, 60 + i*120), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
            
            # Distancia boca a ojos
            if all(k in puntos for k in ['boca_inf', 'ojo_izq_sup', 'ojo_der_sup']):
                dist_boca_ojo_izq = int(dist.euclidean(puntos['boca_inf'], puntos['ojo_izq_sup']))
                dist_boca_ojo_der = int(dist.euclidean(puntos['boca_inf'], puntos['ojo_der_sup']))
                
                dibujar_linea_con_texto(frame, puntos['boca_inf'], puntos['ojo_izq_sup'], 
                                       f"B-OI: {dist_boca_ojo_izq}", (0, 0, 255))
                dibujar_linea_con_texto(frame, puntos['boca_inf'], puntos['ojo_der_sup'], 
                                       f"B-OD: {dist_boca_ojo_der}", (0, 0, 255))
                
                promedio = (dist_boca_ojo_izq + dist_boca_ojo_der) // 2
                cv2.putText(frame, f"Prom. boca-ojos: {promedio}", (10, 90 + i*120), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
            
            # Distancia frente-barbilla (altura facial)
            if all(k in puntos for k in ['frente', 'barbilla']):
                dist_frente_barbilla = int(dist.euclidean(puntos['frente'], puntos['barbilla']))
                dibujar_linea_con_texto(frame, puntos['frente'], puntos['barbilla'], 
                                       f"Altura: {dist_frente_barbilla}", (255, 255, 0))
                
                cv2.putText(frame, f"Altura facial: {dist_frente_barbilla}", (10, 120 + i*120), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
            
            # Dibujar línea entre ojos para referencia
            if all(k in puntos for k in ['ojo_izq', 'ojo_der']):
                cv2.line(frame, puntos['ojo_izq'], puntos['ojo_der'], (0, 255, 0), 1)
                dist_ojos = int(dist.euclidean(puntos['ojo_izq'], puntos['ojo_der']))
                cv2.putText(frame, f"Dist. ojos: {dist_ojos}", 
                           ((puntos['ojo_izq'][0] + puntos['ojo_der'][0]) // 2, 
                            (puntos['ojo_izq'][1] + puntos['ojo_der'][1]) // 2 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow('Analisis Facial Completo', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()