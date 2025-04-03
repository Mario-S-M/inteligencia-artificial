import cv2
import mediapipe as mp
import numpy as np
import time
from collections import deque

class LivenessDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.left_eye_upper = [159, 145, 158, 153]
        self.left_eye_lower = [23, 25, 26, 24]
        self.right_eye_upper = [386, 374, 385, 380]
        self.right_eye_lower = [252, 254, 253, 255]
        self.mouth_top = [13, 14, 312]
        self.mouth_bottom = [14, 17, 317]
        self.nose_tip = 4
        self.key_landmarks = [1, 33, 61, 199, 263, 291]
        
        self.blink_history = deque(maxlen=15)
        self.head_movement_history = deque(maxlen=90)
        self.mouth_movement_history = deque(maxlen=30)
        self.landmark_history = deque(maxlen=60)
        self.last_blink_time = 0
        self.blinks_detected = 0
        self.last_landmarks = None
        
        self.blink_threshold = 0.15
        self.movement_threshold = 0.005
        self.mouth_movement_threshold = 0.01
        self.landmark_variance_threshold = 0.0001
        self.time_window = 5
        self.start_time = time.time()
        
        self.debug_mode = True

    def calculate_eye_aspect_ratio(self, landmarks, frame_width, frame_height):
        left_eye_upper_pts = [landmarks[i] for i in self.left_eye_upper]
        left_eye_lower_pts = [landmarks[i] for i in self.left_eye_lower]
        right_eye_upper_pts = [landmarks[i] for i in self.right_eye_upper]
        right_eye_lower_pts = [landmarks[i] for i in self.right_eye_lower]
        
        left_dist = np.mean([
            np.sqrt(
                ((left_eye_upper_pts[i].x * frame_width) - (left_eye_lower_pts[i].x * frame_width)) ** 2 +
                ((left_eye_upper_pts[i].y * frame_height) - (left_eye_lower_pts[i].y * frame_height)) ** 2
            )
            for i in range(min(len(self.left_eye_upper), len(self.left_eye_lower)))
        ])
        
        right_dist = np.mean([
            np.sqrt(
                ((right_eye_upper_pts[i].x * frame_width) - (right_eye_lower_pts[i].x * frame_width)) ** 2 +
                ((right_eye_upper_pts[i].y * frame_height) - (right_eye_lower_pts[i].y * frame_height)) ** 2
            )
            for i in range(min(len(self.right_eye_upper), len(self.right_eye_lower)))
        ])
        
        return (left_dist + right_dist) / 2
    
    def calculate_mouth_aspect_ratio(self, landmarks, frame_width, frame_height):
        mouth_top_pts = [landmarks[i] for i in self.mouth_top]
        mouth_bottom_pts = [landmarks[i] for i in self.mouth_bottom]
        
        mouth_dist = np.mean([
            np.sqrt(
                ((mouth_top_pts[i].x * frame_width) - (mouth_bottom_pts[i].x * frame_width)) ** 2 +
                ((mouth_top_pts[i].y * frame_height) - (mouth_bottom_pts[i].y * frame_height)) ** 2
            )
            for i in range(min(len(self.mouth_top), len(self.mouth_bottom)))
        ])
        
        return mouth_dist
    
    def detect_blink(self, ear):
        self.blink_history.append(ear)
        if len(self.blink_history) < 5:
            return False
        
        mid_idx = len(self.blink_history) // 2
        if (np.mean(list(self.blink_history)[:mid_idx-1]) > self.blink_threshold and 
            np.mean(list(self.blink_history)[mid_idx-1:mid_idx+1]) < self.blink_threshold and 
            np.mean(list(self.blink_history)[mid_idx+1:]) > self.blink_threshold):
            current_time = time.time()
            if current_time - self.last_blink_time > 0.5:
                self.last_blink_time = current_time
                self.blinks_detected += 1
                return True
        return False
    
    def detect_head_movement(self, landmarks, frame_width, frame_height):
        nose_tip = landmarks[self.nose_tip]
        current_pos = np.array([nose_tip.x * frame_width, nose_tip.y * frame_height, nose_tip.z])
        
        if self.last_landmarks is not None:
            last_nose_tip = self.last_landmarks[self.nose_tip]
            last_pos = np.array([last_nose_tip.x * frame_width, last_nose_tip.y * frame_height, last_nose_tip.z])
            movement = np.linalg.norm(current_pos - last_pos)
            self.head_movement_history.append(movement)
            if len(self.head_movement_history) >= 30:
                movement_variance = np.var(self.head_movement_history)
                return movement_variance > self.movement_threshold
        self.last_landmarks = landmarks
        return False
    
    def detect_mouth_movement(self, landmarks, frame_width, frame_height):
        mar = self.calculate_mouth_aspect_ratio(landmarks, frame_width, frame_height)
        self.mouth_movement_history.append(mar)
        if len(self.mouth_movement_history) < 10:
            return False
        variance = np.var(self.mouth_movement_history)
        return variance > self.mouth_movement_threshold
    
    def calculate_landmark_variance(self):
        if len(self.landmark_history) < 5:
            return 0.0
        
        movements = []
        for i in range(1, len(self.landmark_history)):
            for idx in self.key_landmarks:
                prev_lm = self.landmark_history[i-1][idx]
                curr_lm = self.landmark_history[i][idx]
                movement = np.sqrt(
                    (prev_lm.x - curr_lm.x)**2 + 
                    (prev_lm.y - curr_lm.y)**2 + 
                    (prev_lm.z - curr_lm.z)**2
                )
                movements.append(movement)
        
        return np.var(movements) if movements else 0.0
    
    def detect_liveness(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_height, frame_width, _ = frame.shape
        
        results = self.face_mesh.process(frame_rgb)
        output_frame = frame.copy()
        
        blink_detected = False
        head_movement_detected = False
        mouth_movement_detected = False
        landmark_variance = 0.0
        
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            landmarks = face_landmarks.landmark
            self.landmark_history.append(landmarks)
            
            ear = self.calculate_eye_aspect_ratio(landmarks, frame_width, frame_height)
            blink_detected = self.detect_blink(ear)
            head_movement_detected = self.detect_head_movement(landmarks, frame_width, frame_height)
            mouth_movement_detected = self.detect_mouth_movement(landmarks, frame_width, frame_height)
            landmark_variance = self.calculate_landmark_variance()
            
            if self.debug_mode:
                self.mp_drawing.draw_landmarks(
                    image=output_frame,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style()
                )
            
            elapsed_time = time.time() - self.start_time
            blink_rate = self.blinks_detected / elapsed_time if elapsed_time > 0 else 0
            
            liveness_score = 0.0
            if self.blinks_detected > 0:
                liveness_score += 0.4
            if head_movement_detected:
                liveness_score += 0.3
            if mouth_movement_detected:
                liveness_score += 0.2
            if landmark_variance > self.landmark_variance_threshold:
                liveness_score += 0.3
            
            # Requiere al menos un indicador dinámico después de 5 segundos
            is_live = liveness_score >= 0.5 and (elapsed_time < 5 or self.blinks_detected > 0 or landmark_variance > self.landmark_variance_threshold)
            status_text = "REAL" if is_live else "FOTO"
            color = (0, 255, 0) if is_live else (0, 0, 255)
            
            cv2.putText(output_frame, f"Estado: {status_text}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(output_frame, f"Score: {liveness_score:.2f}", (10, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            if self.debug_mode:
                cv2.putText(output_frame, f"EAR: {ear:.2f}", (10, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                cv2.putText(output_frame, f"Parpadeos: {self.blinks_detected}", (10, 120), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                cv2.putText(output_frame, f"Mov. cabeza: {'Sí' if head_movement_detected else 'No'}", (10, 140), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                cv2.putText(output_frame, f"Mov. boca: {'Sí' if mouth_movement_detected else 'No'}", (10, 160), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                cv2.putText(output_frame, f"Varianza: {landmark_variance:.6f}", (10, 180), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                cv2.putText(output_frame, f"Tiempo: {elapsed_time:.1f}s", (10, 200), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        
        else:
            cv2.putText(output_frame, "Estado: NO DETECTADO", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        return output_frame

def main():
    detector = LivenessDetector()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo capturar el frame")
            break
        
        output_frame = detector.detect_liveness(frame)
        cv2.imshow('Liveness Detection', output_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()