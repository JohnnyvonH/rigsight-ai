# Roadmap

## Milestone 1 - Repository Bootstrap

- README
- clean-room statement
- FastAPI skeleton
- React/Vite skeleton
- Docker Compose
- health endpoint

## Milestone 2 - Synthetic Rig Simulator

- seeded readings
- fault modes
- persisted readings
- latest/history endpoints

## Milestone 3 - Dashboard

- live status
- latest readings
- time-series charts
- rig controls

## Milestone 4 - Rules-Based Anomaly Detection

- thresholds
- drift and dropout checks
- alert records

## Milestone 5 - ML Anomaly Detection

- IsolationForest baseline
- anomaly scores
- rules versus ML comparison

## Milestone 6 - Human Review

- review queue
- labels and notes
- reviewed/unreviewed counts

## Milestone 7 - Camera Lab

- optional OpenCV capture
- frame/status route
- dashboard camera panel

## Milestone 8 - Portfolio Polish

- screenshots
- demo GIF/video
- API docs
- recruiter-friendly project summary

## Future - Cloud Infrastructure

Explore a small production-style cloud deployment path to strengthen the portfolio story:

- containerized backend deployment
- managed Postgres database
- object storage for camera snapshots and exported reports
- frontend hosting with preview deployments
- secrets and environment management
- observability with logs, metrics, and basic alerting
- infrastructure-as-code using Terraform, Pulumi, or provider-native templates
- CI/CD pipeline that runs tests, builds images, and deploys to a staging environment

Potential implementation options include AWS, Azure, GCP, Fly.io, Render, Railway, or Vercel plus a managed database. The goal is not heavy infrastructure for its own sake, but a clear demonstration of deployable full-stack engineering, cloud fundamentals, and operational thinking.
