import os
import sys
import requests
import json
import time

def execute_harness_audit(api_root_url: str, store_code_argument: str, tracking_asset_dir: str):
    target_store = str(store_code_argument).strip().upper()
    print("\n" + "="*75)
    print(f"🏁 INTEGRATION HARNESS METRIC VALIDATION FOR TARGET STORE ID: [{target_store}] 🏁")
    print("="*75 + "\n")

    # 1. Connectivity Health Test Block
    try:
        health_status = requests.get(f"{api_root_url}/health", timeout=3).json()
        print(f"✅ Context Check Complete. System Communication Status: [{health_status['status']}]")
    except Exception:
        print(f"❌ Communication Fault! Ensure target server is live on routing path: {api_root_url}")
        return

    # 2. Trigger Tracking Engine Linkage
    print(f"\n🎬 Deploying Computer Vision Extraction Stream for store identifier: {target_store}...")
    from pipeline.tracker import StoreVideoPipeline
    
    pipeline_ingestion_url = f"{api_root_url}/events/ingest"
    video_engine = StoreVideoPipeline(api_endpoint=pipeline_ingestion_url)
    
    records_count = video_engine.run_ingestion_pipeline(target_store_id=target_store, video_dir=tracking_asset_dir)
    print(f"➡️ Pipeline compilation success. Transmitted [{records_count}] database lines.")

    # 3. Validation Extraction Queries
    print(f"\n📊 Requesting analytics distribution fields for target profile route...")
    
    print(f"\n[Subsystem 1 - Core Metrics]:")
    print(json.dumps(requests.get(f"{api_root_url}/stores/{target_store}/metrics").json(), indent=2))

    print(f"\n[Subsystem 2 - Conversion Funnel Stages]:")
    print(json.dumps(requests.get(f"{api_root_url}/stores/{target_store}/funnel").json(), indent=2))

    print(f"\n[Subsystem 3 - Spatial Zone Density Heatmaps]:")
    print(json.dumps(requests.get(f"{api_root_url}/stores/{target_store}/heatmap").json(), indent=2))

    print(f"\n[Subsystem 4 - Layout Anomalies Tracker]:")
    print(json.dumps(requests.get(f"{api_root_url}/stores/{target_store}/anomalies").json(), indent=2))
    print("\n" + "="*75)

if __name__ == "__main__":
    # Standard runtime initialization settings via arguments or environment maps
    TARGET_HOST = os.getenv("API_URL", "http://127.0.0.1:8000")
    TARGET_VIDEO_DIR = os.getenv("VIDEO_ASSET_DIR", ".")
    
    # Run test sequences dynamically across separate properties to prove compliance
    execute_harness_audit(api_root_url=TARGET_HOST, store_code_argument="ST1008", tracking_asset_dir=TARGET_VIDEO_DIR)
    
    print("\n-- HOLDING EXECUTION QUEUE MOMENTARILY FOR TARGET COMPILATION CHECK --\n")
    time.sleep(2)
    
    execute_harness_audit(api_root_url=TARGET_HOST, store_code_argument="ST1042", tracking_asset_dir=TARGET_VIDEO_DIR)