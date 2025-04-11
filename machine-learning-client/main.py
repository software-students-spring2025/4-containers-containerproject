"""
Main file for machine learning client that receives webcam frames via WebSockets
"""

import asyncio
import base64
import json
import logging
import time
import cv2
import numpy as np
import websockets
from mediapipe.python.solutions import pose as mp_pose
from mediapipe.python.solutions import drawing_utils as mp_drawing

# Configure logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class JumpingJackDetector:
    """
    A class that detects jumping jack exercises using pose detection.
    """

    def __init__(self):
        self.pose = mp_pose.Pose(
            min_detection_confidence=0.8, min_tracking_confidence=0.8
        )
        self.state = "down"
        self.last_state_change = time.time()
        self.cooldown = 0.5
        self.jump_detected = False

    def process_frame(self, frame):
        """
        Processes a single frame.
        """
        # Reset jump detection for this frame
        self.jump_detected = False

        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and get pose landmarks
        results = self.pose.process(rgb_frame)

        # Create a copy of the frame for drawing
        annotated_frame = frame.copy()

        if results.pose_landmarks:
            # Draw pose landmarks
            mp_drawing.draw_landmarks(
                annotated_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
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
                    logger.info("Position: UP")
                elif self.state == "up" and wrist_y > shoulder_y:
                    self.state = "down"
                    self.jump_detected = True  # Flag that a jump was completed
                    self.last_state_change = current_time
                    logger.info("Position: DOWN, Jump detected!")

        # Return both the processed frame and the results
        return {
            "annotated_frame": annotated_frame,
            "jump_detected": self.jump_detected,
            "state": self.state,
        }


# Global detector instance
detector = JumpingJackDetector()


def process_frame_with_ml(frame):
    """
    Process a frame with the JumpingJackDetector.
    """
    # Process the frame with the detector
    result = detector.process_frame(frame)

    # Encode the annotated frame as .jpg
    _, buffer = cv2.imencode(".jpg", result["annotated_frame"])
    img_str = base64.b64encode(buffer).decode("utf-8")

    # Return results including the annotated frame
    return {
        "type": "ml_result",
        "data": {"jump_detected": result["jump_detected"], "state": result["state"]},
        "image": f"data:image/jpeg;base64,{img_str}",
        "timestamp": None,  # Will be filled in by the calling function
    }


# WebSocket connection handler
async def handle_connection(websocket):
    """
    Handle a WebSocket connection from the web client.
    """
    client_id = id(websocket)
    logger.info("Client %s connected from %s", client_id, websocket.remote_address)

    async for message in websocket:
        # Parse the message
        data = json.loads(message)
        timestamp = data.get("timestamp", 0)

        if data["type"] == "frame":
            # Convert base64 image to OpenCV format
            img_data = data["data"].split(",")[
                1
            ]  # Remove data:image/jpeg;base64, prefix
            img_bytes = base64.b64decode(img_data)

            # Convert to numpy array
            nparr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Process the frame with ML
            result = process_frame_with_ml(frame)
            result["timestamp"] = timestamp

            # Send back the results
            await websocket.send(json.dumps(result))

            logger.debug(
                "Processed frame from client %s, timestamp: %s", client_id, timestamp
            )


async def start_server():
    """
    Start the WebSocket server.
    """
    host = "0.0.0.0"  # Listen on all interfaces
    port = 8765

    logger.info("Starting WebSocket server on %s:%s", host, port)

    # Create the WebSocket server
    server = await websockets.serve(
        handle_connection,
        host,
        port,
    )

    logger.info("WebSocket server running at ws://%s:%s", host, port)

    # Keep the server running
    await server.wait_closed()


def main():
    """
    Main Function.
    """
    logger.info("Jumping Jack Detector ML Client is starting...")

    # Start the WebSocket server
    asyncio.run(start_server())


if __name__ == "__main__":
    main()
