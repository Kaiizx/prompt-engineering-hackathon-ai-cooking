import gensim.downloader
import spacy
from collections import Counter
from string import punctuation

# Preload the corpus outside the function
corpus = gensim.downloader.load('glove-wiki-gigaword-100')

def decode_caesar_cipher(text):
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])  # Load spaCy with just the tokenizer

    def decode_text(encoded_text, shift):
        decoded_text = []
        for char in encoded_text:
            if char.isalpha():  # Only shift alphabetical characters
                shifted_char = chr(((ord(char.lower()) - ord('a') - shift) % 26) + ord('a'))
                if char.isupper():
                    shifted_char = shifted_char.upper()
                decoded_text.append(shifted_char)
            else:
                decoded_text.append(char)
        return ''.join(decoded_text)

    def lemmatize_text(text):
        doc = nlp(text)
        lemmatized_words = [token.lemma_ for token in doc if token.lemma_ != '-PRON-' and not token.is_punct]
        return lemmatized_words

    def is_meaningful(decoded_text):
        words = lemmatize_text(decoded_text)
        total_words = len(words)
        if total_words == 0:
            return False

        valid_word_count = sum(1 for word in words if word.lower() in corpus)
        if valid_word_count / total_words >= 0.8:
            return True
        return False

    encoded_text = text.strip()

    results = []
    for shift in range(1, 26):
        decoded_text = decode_text(encoded_text, shift)
        if is_meaningful(decoded_text):
            results.append((shift, decoded_text))

    if results:
        return results[0]  # Return the first meaningful result found (n, decoded_text)
    else:
        return None  # Return None if no meaningful result found

# Example usage:
encrypted_text = "J hpu Qsftfoufe"
result = decode_caesar_cipher(encrypted_text)
if result:
    shift, decoded_text = result
    print(f"For shift value {shift}: {decoded_text}")
else:
    print("No meaningful decryption found.")

import pandas as pd

# Assume decode_caesar_cipher function is defined as provided in the previous response

# Function to process the CSV file and generate the submission file
def process_csv(input_file, output_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Initialize a list to collect results
    results = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        text = row[' text']
        result = decode_caesar_cipher(text)

        if result:
            shift, decoded_text = result
            results.append({'id': row['id'], 'n': shift})

    # Create a DataFrame from the results
    submission_df = pd.DataFrame(results)

    # Write the DataFrame to a CSV file for submission
    submission_df.to_csv(output_file, index=False)
    print(f"Submission file '{output_file}' generated successfully.")

# Example usage:
input_file = 'test.csv'
output_file = 'submission.csv'
process_csv(input_file, output_file)