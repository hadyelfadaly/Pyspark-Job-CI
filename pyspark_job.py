import pyspark.sql.functions as F

def clean_data(df):

    df = df.filter((F.col("amount") > 0) & (F.col("amount").isNotNull()) & (F.col("name").isNotNull())).withColumn("amount_with_tax", F.col("amount") * 1.20)

    return df