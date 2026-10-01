import pytest
from pyspark.sql import SparkSession
from pyspark_job import clean_data

@pytest.fixture(scope="session")
def spark_session():
    spark = SparkSession.builder.master("local[*]").appName("TestOrderCleaningJob").getOrCreate()
    yield spark
    spark.stop()

def test_clean_data(spark_session):

    data = [
    (1, "Ahmed",  100.0),   # valid -> kept, tax = 120.0
    (2, "Sara",    50.5),   # valid -> kept, tax = 60.6
    (3, "Omar",     0.0),   # amount = 0 -> removed (boundary)
    (4, "Mona",   -20.0),   # negative amount -> removed
    (5, None,      75.0),   # NULL name -> removed
    (6, None,     -10.0),   # NULL name AND bad amount -> removed
    (7, "Youssef",  0.01),  # tiny positive -> kept, tax = 0.012
    (8, "Laila",   None),   # NULL amount -> removed
    ]

    schema = "id INT, name STRING, amount DOUBLE"
    df = spark_session.createDataFrame(data, schema)

    cleaned_df = clean_data(df)

    assert cleaned_df.count() == 3  # Only 3 valid rows should remain
    assert cleaned_df.filter(cleaned_df.id == 1).select("amount_with_tax").collect()[0][0] == 120.0 ##the amount with tax for id 1 should be 120.0
    assert cleaned_df.filter(cleaned_df.name.isNull()).count() == 0  # No rows with NULL name should remain
    assert cleaned_df.filter(cleaned_df.amount.isNull()).count() == 0  # No rows with NULL amount should remain