# test_crud_enhancements.py
#
# Verifies the Milestone Four database enhancements (indexing and the
# aggregation pipeline) against an in-memory MongoDB provided by
# mongomock, so the tests can run without a live MongoDB server.
#
# Run:  python3 -m pytest test_crud_enhancements.py -v
#   or: python3 test_crud_enhancements.py

import mongomock
from CRUD_Python_Module import AnimalShelter

SAMPLE_DOCS = [
    {"breed": "Labrador Retriever Mix", "sex_upon_outcome": "Intact Female",
     "age_upon_outcome_in_weeks": 52.0, "outcome_type": "Adoption",
     "location_lat": 30.5, "location_long": -97.4},
    {"breed": "Labrador Retriever Mix", "sex_upon_outcome": "Intact Female",
     "age_upon_outcome_in_weeks": 30.0, "outcome_type": "Transfer",
     "location_lat": 30.6, "location_long": -97.3},
    {"breed": "Labrador Retriever Mix", "sex_upon_outcome": "Intact Female",
     "age_upon_outcome_in_weeks": 80.0, "outcome_type": "Adoption",
     "location_lat": 30.4, "location_long": -97.5},
    {"breed": "German Shepherd", "sex_upon_outcome": "Intact Male",
     "age_upon_outcome_in_weeks": 60.0, "outcome_type": "Adoption",
     "location_lat": 30.7, "location_long": -97.2},
    {"breed": "German Shepherd", "sex_upon_outcome": "Intact Male",
     "age_upon_outcome_in_weeks": 40.0, "outcome_type": "Euthanasia",
     "location_lat": 30.8, "location_long": -97.1},
]


def make_shelter_with_mock_db():
    """Builds an AnimalShelter instance backed by mongomock instead of a
    real MongoDB connection, pre-loaded with SAMPLE_DOCS."""
    shelter = AnimalShelter.__new__(AnimalShelter)  # bypass __init__'s real MongoClient
    client = mongomock.MongoClient()
    shelter.client = client
    shelter.database = client["aac"]
    shelter.collection = shelter.database["animals"]
    shelter.db_name = "aac"
    shelter.col_name = "animals"
    shelter.collection.insert_many(SAMPLE_DOCS)
    return shelter


def test_create_indexes_creates_named_compound_index():
    shelter = make_shelter_with_mock_db()

    index_name = shelter.create_indexes()

    assert index_name == "breed_sex_age_idx"
    indexes = shelter.collection.index_information()
    assert "breed_sex_age_idx" in indexes
    index_keys = [field for field, _ in indexes["breed_sex_age_idx"]["key"]]
    assert index_keys == ["breed", "sex_upon_outcome", "age_upon_outcome_in_weeks"]


def test_breed_outcome_stats_groups_and_computes_correctly():
    shelter = make_shelter_with_mock_db()

    results = shelter.get_breed_outcome_stats()
    by_breed = {row["breed"]: row for row in results}

    # Labrador Retriever Mix: 3 records, 2 adoptions -> rate 2/3
    lab = by_breed["Labrador Retriever Mix"]
    assert lab["count"] == 3
    assert lab["adoptions"] == 2
    assert abs(lab["adoption_rate"] - (2 / 3)) < 1e-9
    assert abs(lab["avg_age_weeks"] - ((52.0 + 30.0 + 80.0) / 3)) < 1e-9

    # German Shepherd: 2 records, 1 adoption -> rate 0.5
    shep = by_breed["German Shepherd"]
    assert shep["count"] == 2
    assert shep["adoptions"] == 1
    assert abs(shep["adoption_rate"] - 0.5) < 1e-9

    # Results should be sorted by count descending
    assert results[0]["breed"] == "Labrador Retriever Mix"


def test_breed_outcome_stats_respects_filter_query():
    shelter = make_shelter_with_mock_db()

    # Mirrors the shape of the dashboard's mountain-rescue query
    query = {"breed": {"$in": ["German Shepherd"]}}
    results = shelter.get_breed_outcome_stats(query)

    assert len(results) == 1
    assert results[0]["breed"] == "German Shepherd"
    assert results[0]["count"] == 2


def test_breed_outcome_stats_returns_empty_list_for_no_matches():
    shelter = make_shelter_with_mock_db()

    results = shelter.get_breed_outcome_stats({"breed": "Chihuahua"})

    assert results == []


if __name__ == "__main__":
    tests = [
        test_create_indexes_creates_named_compound_index,
        test_breed_outcome_stats_groups_and_computes_correctly,
        test_breed_outcome_stats_respects_filter_query,
        test_breed_outcome_stats_returns_empty_list_for_no_matches,
    ]
    for t in tests:
        t()
        print(f"PASSED: {t.__name__}")
    print(f"\n{len(tests)} tests passed.")
