# Roadmap

## Milestone 1 - Repository Bootstrap

- README
- clean-room statement
- FastAPI skeleton
- React/Vite skeleton
- Docker Compose
- health endpoint

## Milestone 2 - Synthetic Rig Simulator

- [x] seeded readings
- [x] fault modes
- [x] persisted readings
- [x] latest/history endpoints

## Milestone 3 - Dashboard

- [x] live status
- [x] latest readings
- [x] time-series charts
- [x] rig controls
- [x] multi-page operational workspace
- [x] 1.0 walkthrough flow

## Milestone 4 - Rules-Based Anomaly Detection

- [x] thresholds
- [x] drift and dropout checks
- [x] alert records

## Milestone 5 - ML Anomaly Detection

- [x] IsolationForest baseline
- [x] anomaly scores
- [x] rules versus ML comparison

## Milestone 6 - Human Review

- [x] review queue
- [x] labels and notes
- [x] reviewed/unreviewed counts

## Milestone 7 - Camera Lab

- [x] disabled-by-default local status route
- [x] optional snapshot endpoint with unavailable state
- [x] dashboard camera panel

## Milestone 8 - Portfolio Polish

- [x] demo media capture guide
- [x] API docs via FastAPI OpenAPI
- [x] recruiter-friendly project summary
- [x] JSON run report export
- [x] release checklist
- [x] current CI includes backend checks, frontend build, Docker service builds, and Docker smoke checks

## Future - Cloud Infrastructure

The 1.0 release documents a small production-style cloud deployment path to strengthen the portfolio story:

- containerized backend deployment
- managed Postgres database
- object storage for camera snapshots and exported reports
- frontend hosting with preview deployments
- secrets and environment management
- observability with logs, metrics, and basic alerting
- infrastructure-as-code using Terraform, Pulumi, or provider-native templates
- CI/CD pipeline that runs tests, builds images, and deploys to a staging environment

Potential implementation options include AWS, Azure, GCP, Fly.io, Render, Railway, or Vercel plus a managed database. The goal is not heavy infrastructure for its own sake, but a clear demonstration of deployable full-stack engineering, cloud fundamentals, and operational thinking.
