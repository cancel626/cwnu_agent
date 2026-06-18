from app.db.base import Base, engine
from app.models.model_config import ModelConfig

Base.metadata.create_all(bind=engine, tables=[ModelConfig.__table__])
print("model_configs table created")
