"""
Database Reset: Drop and recreate all tables
WARNING: This will delete all existing data!
"""

from database import Base, engine
from models import Company, FinancialRecord, Assessment

print("WARNING: This will delete all existing data!")
print("Dropping all tables...")

# Drop all tables
Base.metadata.drop_all(bind=engine)
print("All tables dropped")

print("Creating tables with new schema...")

# Recreate all tables with updated schema
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
print("\nNew schema includes:")
print("  - companies table with file_hash column")
print("  - financial_records table")
print("  - assessments table")
print("\nDatabase is ready to use!")
