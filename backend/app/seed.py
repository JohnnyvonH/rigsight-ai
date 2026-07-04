from app.database import Base, SessionLocal, engine
from app.services.demo_data import ensure_demo_data


def main() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        run = ensure_demo_data(db)
    print(f"Seeded demo telemetry for run {run.id}: {run.name}")


if __name__ == "__main__":
    main()
