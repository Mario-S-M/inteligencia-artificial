import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist
import pickle
import sys
from collections import defaultdict

# Configuración mejorada de MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,  # Reducir a 1 cara para mejor rendimiento
    refine_landmarks=True,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)

# Puntos clave optimizados
LANDMARKS = {
    'frente': 10, 'barbilla': 152, 'ojo_izq': 33, 'ojo_der': 263,
    'nariz': 1, 'boca_izq': 61, 'boca_der': 291, 'cachete_izq': 123,
    'cachete_der': 352, 'sien_izq': 162, 'sien_der': 389
}

FAMILY_NAMES = {
    '1': 'Mario', '2': 'Papá', '3': 'Mamá', '4': 'Abuelo',
    '5': 'Abuela', '6': 'Hermano', '7': 'Hermana', '8': 'Tío', '9': 'Tía'
}

# Cargar base de datos de forma segura
def load_database():
    try:
        with open('family_db.pkl', 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        return {}

family_db = load_database()

def get_normalized_distances(landmarks, frame_shape):
    """Versión optimizada del cálculo de distancias"""
    points = {}
    try:
        for name, idx in LANDMARKS.items():
            landmark = landmarks.landmark[idx]
            points[name] = (int(landmark.x * frame_shape[1]), int(landmark.y * frame_shape[0]))
        
        ref_distance = dist.euclidean(points['ojo_izq'], points['ojo_der'])
        if ref_distance < 5:  # Filtro mínimo de distancia
            return None, None

        distances = {
            'eyes': ref_distance,
            'nose_eye_left': dist.euclidean(points['nariz'], points['ojo_izq']) / ref_distance,
            'nose_eye_right': dist.euclidean(points['nariz'], points['ojo_der']) / ref_distance,
            'mouth_width': dist.euclidean(points['boca_izq'], points['boca_der']) / ref_distance,
            'face_height': dist.euclidean(points['frente'], points['barbilla']) / ref_distance,
            'left_profile': dist.euclidean(points['ojo_izq'], points['boca_izq']) / ref_distance,
            'right_profile': dist.euclidean(points['ojo_der'], points['boca_der']) / ref_distance
        }
        return distances, points
    except Exception as e:
        print(f"Error calculando distancias: {str(e)}")
        return None, None

def compare_faces(current_distances):
    """Comparación optimizada con tolerancia ajustada"""
    if not current_distances or not family_db:
        return None

    best_match = None
    best_score = float('inf')

    for name, data in family_db.items():
        try:
            score = np.mean([abs(current_distances[k] - data['distances'][k]) / data['distances'][k] 
                           for k in current_distances if k in data['distances']])
            
            if score < best_score and score < 0.1:  # Tolerancia del 10%
                best_score = score
                best_match = name
        except:
            continue

    return best_match if best_score != float('inf') else None

def main():
    global family_db, face_mesh

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara")
        sys.exit(1)

    register_mode = False
    current_person = None
    frame_count = 0
    register_frames = 15

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: No se pudo leer el frame")
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    distances, points = get_normalized_distances(face_landmarks, frame.shape)
                    if distances is None:
                        continue

                    if register_mode and current_person:
                        if frame_count < register_frames:
                            if current_person not in family_db:
                                family_db[current_person] = {'distances': defaultdict(list)}
                            
                            for k, v in distances.items():
                                family_db[current_person]['distances'][k].append(v)
                            
                            frame_count += 1
                            cv2.putText(frame, f"Registrando {current_person}... {frame_count}/{register_frames}", 
                                       (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        else:
                            # Finalizar registro
                            for k in family_db[current_person]['distances']:
                                family_db[current_person]['distances'][k] = np.median(family_db[current_person]['distances'][k])
                            
                            with open('family_db.pkl', 'wb') as f:
                                pickle.dump(family_db, f)
                            
                            register_mode = False
                            current_person = None
                            frame_count = 0
                    else:
                        # Modo reconocimiento
                        person = compare_faces(distances)
                        color = (0, 255, 0) if person else (0, 0, 255)
                        cv2.putText(frame, person if person else "Desconocido", 
                                   (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            # Mostrar instrucciones
            cv2.putText(frame, "Teclas: 1-9 para registrar, 'q' para salir", 
                       (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow('Reconocimiento Familiar', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif ord('1') <= key <= ord('9'):
                current_person = FAMILY_NAMES.get(chr(key), f"Persona_{chr(key)}")
                register_mode = True
                frame_count = 0

    finally:
        # Liberar recursos correctamente
        cap.release()
        cv2.destroyAllWindows()
        if face_mesh:
            face_mesh.close()
        print("Sistema terminado correctamente")

if __name__ == "__main__":
    main()