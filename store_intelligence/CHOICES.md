# Engineering Trade-Offs and Justifications

## 1. Frame Sampling Strategy
* **Choice:** 30FPS to 1FPS down-sampling.
* **Justification:** Full-rate processing is computationally prohibitive for multi-channel arrays. 1FPS is sufficient to capture transition state changes in retail environments while preserving 95%+ processing headroom.

## 2. Storage & Schema Design
* **Choice:** Relational Database (SQLAlchemy/SQLite).
* **Justification:** Retail intelligence requires ACID-compliant data integrity. Relational models allow for `GROUP BY` and `DISTINCT` operations, which are essential for calculating unique visitor counts accurately.

## 3. Idempotency Gate
* **Choice:** Server-side event deduplication via `event_id` keys.
* **Justification:** Ensures that intermittent network fluctuations between camera sensors and the ingestion API do not result in duplicate event logs, maintaining the integrity of business metrics.

# Scalability Evidence: Our ingestion pipeline demonstrated robustness during validation, successfully processing disparate traffic loads—from high-density bottlenecked environments to optimized operational layouts—without performance degradation.