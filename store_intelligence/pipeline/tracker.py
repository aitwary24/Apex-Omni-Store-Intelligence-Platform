import os
import cv2
import uuid
import requests
from datetime import datetime, timedelta

class StoreVideoPipeline:
    def __init__(self, api_endpoint: str):
        # Clean parameter injection removes local networking loop definitions
        self.api_url = api_endpoint
        self.camera_mapping = {
            "cam1.mp4": {"zone": "ENTRANCE", "type": "ENTRY"},
            "cam2.mp4": {"zone": "MAKEUP", "type": "ZONE_ENTER"},
            "cam3.mp4": {"zone": "SKINCARE", "type": "ZONE_ENTER"},
            "cam4.mp4": {"zone": "BATH-AND-BODY", "type": "ZONE_ENTER"},
            "cam5.mp4": {"zone": "BILLING_QUEUE", "type": "BILLING_QUEUE_JOIN"}
        }

    def run_ingestion_pipeline(self, target_store_id: str, video_dir: str):
        clean_store_id = str(target_store_id).strip().upper()
        print(f"🎬 Initiating Tracking Frame Loop for Store: [{clean_store_id}]")
        base_time = datetime.now()
        total_processed_records = 0

        for video_filename, metadata in self.camera_mapping.items():
            path_to_video = os.path.join(video_dir, video_filename)
            
            if not os.path.exists(path_to_video):
                print(f"⚠️ Video track target source '{video_filename}' cannot be located at {video_dir}. Skipping.")
                continue

            print(f"📹 Processing frames from channel: {video_filename} [{metadata['zone']}]")
            capture = cv2.VideoCapture(path_to_video)
            bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=300, varThreshold=70, detectShadows=True)
            
            frame_idx = 0
            detection_idx = 0
            payload_buffer = []

            while capture.isOpened():
                success, frame = capture.read()
                if not success:
                    break

                frame_idx += 1
                if frame_idx % 30 != 0:
                    continue

                mask = bg_subtractor.apply(frame)
                struct_element = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
                dilated_mask = cv2.dilate(mask, struct_element, iterations=2)
                _, clean_binary = cv2.threshold(dilated_mask, 200, 255, cv2.THRESH_BINARY)
                
                contours, _ = cv2.findContours(clean_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for contour in contours:
                    if 4500 < cv2.contourArea(contour) < 160000:
                        detection_idx += 1
                        x, y, w, h = cv2.boundingRect(contour)
                        is_staff = True if (x < 65 and y < 65) else False
                        
                        uid_event = f"evt_{clean_store_id}_{video_filename.split('.')[0]}_{frame_idx}_{detection_idx}"
                        uid_visitor = f"VIS_{video_filename.split('.')[0]}_{uuid.uuid4().hex[:6].upper()}"
                        calculated_time = base_time + timedelta(seconds=frame_idx // 25)

                        payload_buffer.append({
                            "event_id": uid_event,
                            "store_id": clean_store_id,
                            "camera_id": video_filename.split(".")[0],
                            "visitor_id": uid_visitor,
                            "event_type": metadata["type"],
                            "timestamp": calculated_time.isoformat(),
                            "zone_id": metadata["zone"],
                            "dwell_ms": int(42000 + (w * 15)),
                            "is_staff": is_staff,
                            "confidence": 0.95,
                            "metadata": {
                                "session_seq": frame_idx,
                                "sku_zone": metadata["zone"],
                                "queue_depth": min(detection_idx, 7) if metadata["zone"] == "BILLING_QUEUE" else 0
                            }
                        })

                if len(payload_buffer) >= 50:
                    total_processed_records += self._post_payload_batch(payload_buffer)
                    payload_buffer.clear()

            if payload_buffer:
                total_processed_records += self._post_payload_batch(payload_buffer)

            capture.release()
            print(f"✅ Channel [{video_filename}] completed. Logged {detection_idx} targets.")

        return total_processed_records

    def _post_payload_batch(self, payload):
        try:
            res = requests.post(self.api_url, json=payload, timeout=5)
            if res.status_code == 200:
                return res.json().get("inserted", 0)
        except Exception as e:
            print(f"❌ Handshake processing failure: {e}")
        return 0