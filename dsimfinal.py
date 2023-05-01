import re
import sys
import pandas as pd

def extract_domains_from_log_files(log_file_paths):
    domains = set()
    for log_file_path in log_file_paths:
        with open(log_file_path, 'r') as f:
            for line in f:
                match = re.search(r'http[s]?://([\w.-]+)', line)
                if match:
                    domain = match.group(1)
                    domains.add(domain)
    return domains

def tokenize_into_trigrams(domain):
    trigrams = set()
    for i in range(len(domain) - 2):
        trigrams.add(domain[i:i+3])
    return trigrams

def calculate_jaccard_similarity(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

if len(sys.argv) < 2:
    print("Usage: python script_name.py <log_file_path1> <log_file_path2> ...")
    sys.exit(1)

log_file_paths = sys.argv[1:]
domains = extract_domains_from_log_files(log_file_paths)

# Tokenize domains into trigrams
domain_trigrams = {}
for domain in domains:
    trigrams = tokenize_into_trigrams(domain)
    domain_trigrams[domain] = trigrams

# Calculate Jaccard similarity between domains and store results in a DataFrame
results = []

for domain1 in domains:
    for domain2 in domains:
        if domain1 != domain2:
            jaccard_similarity = calculate_jaccard_similarity(domain_trigrams[domain1], domain_trigrams[domain2])
            results.append({"Domain1": domain1, "Domain2": domain2, "Jaccard_Similarity": jaccard_similarity})

result_df = pd.DataFrame(results)

# Write results to a CSV file
output_file_path = 'jaccard_similarity_results.csv'
result_df.to_csv(output_file_path, index=False)

print(f"Jaccard similarity results written to {output_file_path}")
