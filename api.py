from sys import meta_path
from flask import Flask, request
import json 

from pyspark.sql import SparkSession
from pyspark.sql.functions import col



app = Flask(__name__)

PATH_DESCRIPTION_FILE = '/Users/tranhamduong/Downloads/home-depot-product-search-relevance/home-depot-product-search-relevance/product_descriptions.csv'
PATH_ATTRIBUTES_FILE = '/Users/tranhamduong/Downloads/home-depot-product-search-relevance/home-depot-product-search-relevance/attributes.csv'
def init_spark():
    spark =  SparkSession.builder.getOrCreate()
    return spark

spark = init_spark()

def read_data(spark):
    attributes_df = spark.read.format('csv').options(header='true', inferschema='true').load(PATH_ATTRIBUTES_FILE)
    description_df = spark.read.format('csv').options(header='true', inferschema='true').load(PATH_DESCRIPTION_FILE)
    
    return attributes_df, description_df

attributes_df, description_df = read_data(spark)
attributes_df.show(1)
description_df.show(1)
attributes_df.cache() 
description_df.cache() 


def query_description(product_id): 
    value = description_df.where(col("product_uid") == product_id).select('product_description').first()[0]
    
    return value.strip('"')
    

@app.route('/recommend', methods=['GET', 'POST'])
def api():
    key_word = ""
    if request.method == 'POST':
        key_word = request.json['search']
    elif request.method == 'GET':
        key_word = request.args.get("search")

    if key_word:
        value = query_description(key_word)
        return {
            "product_uid": key_word,
            "description": value
        }
    
    return "Invalid product_id"

if __name__ == '__main__':
    print("Hello World")
    app.run(host="0.0.0.0", port=8008)
