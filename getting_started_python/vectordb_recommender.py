import pandas as pd 
import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
model_name="all-MiniLM-L6-v2"
)

collection = client.create_collection(
    name="product_search",
    embedding_function = embedding_function
) ## till here is the code for initializing a chroma db


##now from here on its the reading of the csv file and then addingindb

products_df = pd.read_csv("products.csv")

all_titles = products_df["title"]
all_descriptions = products_df["description"]


all_title_description = zip(all_titles,all_descriptions)

texts= [f"{title}{description}" for title,description in all_title_description]

##now for adding and storing in the vector db

collection.add(
  documents=texts,
   metadatas=[{
  'product_id': pid,
  'title': title,
  'category': category,
  'price': price,
} for pid, title, category, price in zip(
products_df['product_id'],
products_df['title'],
products_df['category'],
products_df['price']
)],
ids=[pid for pid in products_df['product_id']]
)

## now for querying the db to ge the results

query = "camera for taking professional looking photos"

results = collection.query(
    query_text= [query],
    n_results = 3
)

for metadata in results[metadata][0]:
    print(f"{metadata["product_id"]}: {metadata["title"]}")

## so 3 things create_collection , add ,query before that .Client()


## now product recommendations using dataclasseso


@dataclass
class Product:
    products: List[] = field(default_factory= )

    def get_descriptions(self):
        return f"{self.title} {self.description}"

@dataclass
class Purchasehistory:
    products: Product = field(default_factory ="")

    def has_product(self,product_id):
        return any(product_id ==product.product_id for product in
              self.products )

    def has_description(self):
        return[product.get_descriptions for product in self.products]


@dataclass
class User:
    username:str,
    purchase_history: Purchasehistory  = field(default_factory="")



    def get_recommendations(self,n_recommendations,category_score=0.7):

        result = []

        if not purchase_history.products:
            return []

        query_texts = purchase_history.has_description()

        results = self.collection.query(
            query_texts = query_texts,
            n_results = n_recommendations + len(purchase_history.
                                                products)
        )

        for idx,metadata in enumerate(results[metadata][0]):
            product_id = metadata["product_id"]

            if purchase_history.has_product(product_id):
                continue

            cat_score = category_score any(
                metadata["category"] == product.category for product
                in purchase_history.products
            )

            product = find_product(metadata["product_id"])

            product.relevance_score = cat_score + results[distance][0][idx]
                                           
            result.append(product)

            if len(result)>n_recommendations:
                break

            result.sort(lambda x:x.relevance_score)

        return result            

##metadata can be looped and checked in metadata[0] ofcurse results
## but if you see distanc[0][idx] means first querys's intthat also
##acc to idx why did we not do for others like this because we for
##them are first doing results.get("metadata")[0] then after idx
##or something but here for distance we did not do that so we have
##tofirstdolikethat then inthat firstone

