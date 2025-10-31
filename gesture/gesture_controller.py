import cv2
import mediapipe as mp
import pyautogui
import time

def simple_reliable_controller():
    """Ultra-simple but reliable controller"""
    
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.6)
    cap = cv2.VideoCapture(0)
    
    print("🎯 SIMPLE & RELIABLE CONTROLLER")
    print("Open PowerPoint → F5 → Use these gestures:")
    print("👉 ONE finger = Next slide")
    print("👉 TWO fingers = Previous slide") 
    print("👉 FIST = Exit")
    print("Minimize this window after starting!")
    
    last_action = None
    action_cooldown = 0
    
    while True:
        success, frame = cap.read()
        if not success:
            continue
            
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        if action_cooldown > 0:
            action_cooldown -= 1
        
        current_action = None
        
        if results.multi_hand_landmarks and action_cooldown == 0:
            for hand_landmarks in results.multi_hand_landmarks:
                # Simple finger counting
                tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky tips
                pips = [6, 10, 14, 18]  # Corresponding PIP joints
                
                fingers_up = 0
                for tip, pip in zip(tips, pips):
                    if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
                        fingers_up += 1
                
                # Map to actions
                if fingers_up == 1:
                    current_action = "next"
                elif fingers_up == 2:
                    current_action = "prev" 
                elif fingers_up == 0:
                    current_action = "exit"
                
                # Execute if it's a new action
                if current_action and current_action != last_action:
                    if current_action == "next":
                        pyautogui.press('right')
                        print("➡️ NEXT")
                    elif current_action == "prev":
                        pyautogui.press('left')
                        print("⬅️ PREVIOUS")
                    elif current_action == "exit":
                        pyautogui.press('esc')
                        print("🚪 EXIT")
                    
                    last_action = current_action
                    action_cooldown = 10  # Very short cooldown
        
        # Simple display
        cv2.putText(frame, "Slide Controller - ACTIVE", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        if current_action:
            cv2.putText(frame, f"Action: {current_action.upper()}", (50, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow('Controller - Minimize Me', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    simple_reliable_controller()