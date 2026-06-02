# System Design
1. Executive Summary
# This project implements a decoupled, event-driven architecture designed to convert high-entropy, raw CCTV video data into low-entropy, structured retail analytics. The system adheres to a Pipeline-to-Persistence pattern, ensuring that video processing can scale independently from the API analytics layer.

2. High-Level Topology
The system is partitioned into three distinct operational domains:

# Operational Layers:
Extraction Engine (pipeline/tracker.py):

# Role: Acts as the data producer. It sequentializes multi-channel video inputs, applies adaptive background subtraction (MOG2) to neutralize lighting noise, and performs spatial coordinate mapping.

# Logic: Tracks moving object contours. Filters are applied to exclude static noise (camera reflections) and internal store personnel using coordinate-based masking (x < 65, y < 65).

# Streaming: Processes frames and dispatches event-driven tracking payloads via HTTP POST requests to the ingestion gateway.

# API Services & Persistence (app/):

# Ingestion Gateway: An idempotent REST interface (/events/ingest) utilizing FastAPI. It acts as a data contract enforcer, validating incoming event schemas via Pydantic and implementing database-level deduplication via unique event_id keys to maintain transactional integrity.

# Persistence Layer: An ORM-managed relational store (SQLAlchemy) that maps tracking events, visitors, and store zones. This allows for complex relational querying—essential for accurate conversion and funnel calculations.

# Analytics & Query Engine (app/main.py):

# Computation: The core intelligence layer. On startup, it synchronizes global reference dataframes (POS_DF_MASTER and LAYOUT_ZONES_MASTER) from external source files.

# Business Fusion: When an analytics query is made (e.g., /stores/{id}/metrics), the engine performs a join operation between real-time database tracking events and the loaded static layout/transaction files to generate live business KPIs.

3. Constraint-Based Design Mitigations
# Edge Case Handling (Re-entry): Visitor traffic is derived using SQL DISTINCT queries over visitor_id, ensuring that customers exiting and re-entering the frame are not double-counted.

# Operational Bottlenecks: Anomaly detection is performed by calculating queue depth via count queries on the BILLING_QUEUE zone, triggering a CRITICAL status if the aggregate exceeds defined layout thresholds.

# Resource Efficiency: High-frequency CCTV frame data is down-sampled to 1FPS via temporal skipping, drastically reducing CPU/RAM utilization while preserving the fidelity of retail-relevant movement patterns.
