# Full run
# make all

# Or stepwise:
make migrate   # Schema migration
make load      # Bulk-load CSV
make extract   # Export to Parquet
make train     # Train model + save metrics
make serve     # Launch FastAPI app