import cv2
import time
from mediapipe.python.solutions import pose as mp_pose
from mediapipe.python.solutions import drawing_utils as mp_drawing


class JumpingJackCounter:
    def __init__(self):
        self.pose = mp_pose.Pose(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        )
        self.count = 0
        self.state = "down" # Initial state
        self.last_state_change = time.time()
        self.cooldown = 1.0  # Cooldown period in seconds

    def process_frame(self, frame):
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and get pose landmarks
        results = self.pose.process(rgb_frame)

        if results.pose_landmarks:
            # Draw pose landmarks
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

            # Get key points
            landmarks = results.pose_landmarks.landmark

            # Get shoulder and wrist points
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

            # Calculate vertical positions
            shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
            wrist_y = (left_wrist.y + right_wrist.y) / 2

            # Detect jumping jack motion
            current_time = time.time()
            if current_time - self.last_state_change > self.cooldown:
                if self.state == "down" and wrist_y < shoulder_y:
                    self.state = "up"
                    self.last_state_change = current_time
                elif self.state == "up" and wrist_y > shoulder_y:
                    self.state = "down"
                    self.count += 1
                    self.last_state_change = current_time

            # Display count
            cv2.putText(
                frame,
                f"Count: {self.count}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

        return frame


def main():
    counter = JumpingJackCounter()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process frame
        frame = counter.process_frame(frame)

        # Display frame
        cv2.imshow("Jumping Jack Counter", frame)

        # Break loop on 'q' key
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
