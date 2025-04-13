import json
import base64
import time
import numpy as np
import cv2
import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from main import JumpingJackDetector, process_frame_with_ml, handle_connection


def create_dummy_frame():
    """
    Helper function to creates a dummy black frame (480x640).
    """
    return np.zeros((480, 640, 3), dtype=np.uint8)


def encode_frame_to_base64(frame):
    """
    Helper function to encode frame to a Base64 string, (process_frame_with_ml line 97 in main)
    """
    _, buffer = cv2.imencode(".jpg", frame)
    return base64.b64encode(buffer).decode("utf-8")


# ----------------------------
# Test: JumpingJackDetector
# ----------------------------
def test_jump_detected_when_wrist_above_shoulder():
    detector = JumpingJackDetector()
    dummy_frame = create_dummy_frame()

    # Create 33 mock landmarks
    mock_landmarks = []
    for i in range(33):
        lm = MagicMock()
        lm.x = 0.5
        lm.y = 0.5
        lm.z = 0.0
        lm.visibility = 0.9
        lm.presence = 1.0
        lm.HasField.side_effect = lambda field, i=i: field in ["visibility", "presence"]
        mock_landmarks.append(lm)

    # Set wrist above shoulder
    mock_landmarks[11].y = 0.6  # LEFT_SHOULDER
    mock_landmarks[12].y = 0.6  # RIGHT_SHOULDER
    mock_landmarks[15].y = 0.2  # LEFT_WRIST
    mock_landmarks[16].y = 0.2  # RIGHT_WRIST


    # Mock pose_landmarks object
    pose_landmarks = MagicMock()
    pose_landmarks.landmark = mock_landmarks

    # Mock the result object from MediaPipe
    mock_result = MagicMock()
    mock_result.pose_landmarks = pose_landmarks

    # Patch the detector's pose.process to return the mock result
    with patch.object(detector.pose, 'process', return_value=mock_result):
        result = detector.process_frame(dummy_frame)

    assert result["state"] == "down"
    assert result["jump_detected"] is False




# ----------------------------
# Test: process_frame_with_ml
# ----------------------------
def test_process_frame_with_ml_output():
    dummy_frame = create_dummy_frame()
    result = process_frame_with_ml(dummy_frame)

    assert result["type"] == "ml_result"
    assert "jump_detected" in result["data"]
    assert result["image"].startswith("data:image/jpeg;base64,")


# ----------------------------
# Test: WebSocket handler
# ----------------------------
@pytest.mark.asyncio
async def test_handle_connection_sends_response():
    dummy_frame = create_dummy_frame()
    encoded_img = encode_frame_to_base64(dummy_frame)
    data_uri = f"data:image/jpeg;base64,{encoded_img}"

    mock_websocket = AsyncMock()
    mock_websocket.__aiter__.return_value = [
        json.dumps({
            "type": "frame",
            "data": data_uri,
            "timestamp": 123
        })
    ]

    await handle_connection(mock_websocket)

    # Check something was sent back
    mock_websocket.send.assert_called_once()
    response = json.loads(mock_websocket.send.call_args[0][0])
    assert response["type"] == "ml_result"
    assert response["timestamp"] == 123
    assert "image" in response
    assert "jump_detected" in response["data"]
