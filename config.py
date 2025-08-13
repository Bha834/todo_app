import os

# AWS S3
S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION", "ap-south-1")

# Database (RDS MySQL)
DB_USER = os.getenv("admin")
DB_PASSWORD = os.getenv("bha02#pat")
DB_HOST = os.getenv("database-1.c9u2mi4ma65b.ap-south-1.rds.amazonaws.com")
DB_NAME = os.getenv("database-1")


# SQLAlchemy URI
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
