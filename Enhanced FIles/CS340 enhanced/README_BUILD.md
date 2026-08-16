# Milestone Four Enhancement - Build/Run Notes

## Requirements
    pip install pymongo mongomock

## Running the automated tests (no live MongoDB needed)
    python3 test_crud_enhancements.py

This validates create_indexes() and get_breed_outcome_stats() against an
in-memory MongoDB provided by mongomock, using a small fixed sample
dataset with hand-checked expected results.

## Running the dashboard
The dashboard (ProjectTwoDashboard_enhanced.ipynb) requires a live MongoDB
instance with the Austin Animal Center "aac.animals" collection loaded, the
same as the original project. On startup it now also calls:
  - db.create_indexes()         to create the breed_sex_age_idx compound index
  - db.apply_schema_validation() to apply the $jsonSchema validator

Both require a real MongoDB connection to take effect; they were not
exercised against mongomock, which does not enforce collMod validators.
