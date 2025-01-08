import pandas as pd
from gensim.models import Word2Vec
import pickle
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import ast


recipe_data=pd.read_csv('./datasets/final_2M_sample_recipes.csv')
recipe_data['ingredients']=recipe_data['ingredients'].apply(ast.literal_eval)
recipe_data['directions']=recipe_data['directions'].apply(ast.literal_eval)
with open('./datasets/ML Models/TFIDF/tfidf_vectorizer.pkl', 'rb') as file:
    tfidf_vectorizer = pickle.load(file)
model = Word2Vec.load("./datasets/ML Models/Word2VecModel/model_cbow3.bin")
print(model.wv.most_similar("salt"))
max_idf = max(tfidf_vectorizer.idf_)
word_idf_weight = defaultdict(
    lambda: max_idf,
    [(word, tfidf_vectorizer.idf_[i]) for word, i in tfidf_vectorizer.vocabulary_.items()],
    )

def doc_average(doc):
  mean = []
  for word in doc:
    if word in model.wv.index_to_key:
      mean.append(model.wv.get_vector(word) * word_idf_weight[word] )
    # else:
    #   print('not found')

  if not mean:
    return np.zeros(100)
  else:
    mean = np.array(mean).mean(axis=0)
    return mean


def doc_average_list(docs):
  return np.vstack([doc_average(doc) for doc in docs])

# ingredientsEmbeddings = np.load('/content/drive/MyDrive/archive/embeddings.npy')
nn=NearestNeighbors(algorithm='brute',metric='cosine')
nearestNeighborModel=nn.fit(np.load('./datasets/ML Models/Ingredients_embeddings/sample_embeddings.npy'))

def makePrediction(ingredientsList):
  ingredientsList_embedding=doc_average(ingredientsList).reshape(1,-1)
  distances,indices=nearestNeighborModel.kneighbors(ingredientsList_embedding,n_neighbors=10)
  recipes_recommendation = recipe_data.iloc[indices[0],]
  recipes_recommendation_list = recipes_recommendation.to_dict(orient='records')
  return recipes_recommendation_list

if __name__=='__main__':
  inputs=['chicken thigh', 'onion', 'rice noodle', 'seaweed nori sheet', 'sesame', 'shallot', 'soy', 'spinach', 'star', 'tofu']
  print(makePrediction(inputs))
  
  
  
  
