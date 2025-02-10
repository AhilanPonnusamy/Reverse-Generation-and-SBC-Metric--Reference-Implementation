import spacy
from sentence_transformers import SentenceTransformer, util
from nltk.translate.bleu_score import sentence_bleu
from nltk.corpus import wordnet as wn
import json
import argparse
import subprocess

# Load NLP models
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")
question_id = 0

# 1️⃣ Semantic Similarity
def semantic_similarity(req1, req2):
    emb1 = model.encode(req1, convert_to_tensor=True)
    emb2 = model.encode(req2, convert_to_tensor=True)
    return util.pytorch_cos_sim(emb1, emb2).item()

# 2️⃣ BLEU Score
def bleu_score(req1, req2):
    return sentence_bleu([req1.split()], req2.split())

# 3️⃣ Completeness Check (Updated)
def extract_keywords(text):
    doc = nlp(text)
    return {token.lemma_ for token in doc if token.pos_ in ["NOUN", "VERB", "PROPN"]}

def completeness_score(req1, req2):
    keywords1 = extract_keywords(req1)
    keywords2 = extract_keywords(req2)
    
    missing = keywords1 - keywords2
    extra = keywords2 - keywords1
    
    # Calculate penalty based on number of missing and extra keywords
    penalty = len(missing) + len(extra)
    
    # We now normalize based on the total number of unique keywords across both texts
    total_keywords = len(keywords1.union(keywords2))
    score = max(0, 1 - (penalty / max(total_keywords, 1)))  # Avoid division by zero
    
    return score, missing, extra

# 4️⃣ Final Comparison Function (Updated Weights)
def compare_requirements(req1, req2):
    semantic_score = semantic_similarity(req1, req2)
    bleu = bleu_score(req1, req2)
    completeness, missing, extra = completeness_score(req1, req2)
    
    # Adjusted Weighted Final Score (Closer to 1 means high accuracy)
    final_score = (0.7 * semantic_score) + (0.1 * bleu) + (0.2 * completeness)
    
    return json.dumps({
        "input_requirement": req1,
        "reverse_generated_requirement": req2,
        "final_accuracy_score": round(final_score, 4),  # Score between 0-1,
        "semantic_similarity": round(semantic_score, 4),
        "bleu_score": round(bleu, 4),
        "completeness_score": round(completeness, 4),
        "missing_elements": list(missing),
        "extra_elements": list(extra)
    }, indent=4)

# Command-line argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two requirements based on accuracy, BLEU score, and completeness.")
    parser.add_argument("language", type=str, help="Programming language")
    parser.add_argument("req1", type=str, help="Input requirement text")
  
    args = parser.parse_args()
    
    # Run the script as a subprocess and capture the output
    result = subprocess.run(
        ['python3', 'reverse_generation.py', args.language, args.req1],
        capture_output=True,
        text=True
    )
    
    # Parse the JSON output
    json_output = json.loads(result.stdout)
    gen_reqs = json_output.get('reverse_generated_requirements')
  
    # Compare the input requirement with the generated one
    result = compare_requirements(args.req1, gen_reqs)
    print(result)
