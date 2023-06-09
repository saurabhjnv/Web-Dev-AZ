'''
    1. Read lines from the document 
    2. Preprocess the lines(document) and store it in documents[] list
    3. Create "vocab" as dictionary and store it in file
    4. Store preprocessed documents in file
    5. Store IDF(here term frequency) values of vocab terms in files
    6. Store Inverted-Index (in which document that term is present + term's frequency in that document)
'''
documents = []
vocab = {}
inverted_index = {}

# read lines from index file
with open("Leetcode-Scrapper-Question/index.txt","r",encoding="utf8") as f:
    lines = f.readlines()

# preprocess the index lines in documents
    #remove inital numbers, ",", and convert all to lower case tokens
def preprocess_index(document_text):
    #after split take only the strings and leave inital numbers and add term.lower()
    terms = [term.lower() for term in document_text.strip().split()[1:]]
    return terms

# preprocess the text lines in documents receive {list of strings as argument}
    # convert all to lower case tokens
def preprocess_text(document_text):
    # convert the doc_text lists of string into one string
    text = ""
    for line in document_text:
        text += " " + line.strip()
    # split and take text before "Example 1:"
    text = text.split("Example 1:")[0]
    terms = [term.lower() for term in text.strip().split()]
    return terms

# add all the the processed docs in the documents list
for index,line in enumerate(lines):
    # tokens of every index heading
    tokens_index = preprocess_index(line)

    # opening and adding the document related to the index - "line"(1,2,...) in 
    line_index_filepath = "Leetcode-Scrapper-Question/Qdata/{}/{}.txt"
    line_index_filepath = line_index_filepath.format(index+1,index+1)
    with open(line_index_filepath,"r") as f:
        doc_text = f.readlines()
        #tokens of text document
        tokens_doc_text = preprocess_text(doc_text)
    #overall tokens
    tokens = tokens_index + tokens_doc_text
    # repeated tokens also added in documents
    documents.append(tokens)

    # to count in how many documents a particular term comes -> we change tokens list to tokens set 
    # if we dont do this then vocab will represent tf of a particular word over all documents
    tokens = set(tokens)
    # create vocab -> add token in vocab if token not existed before else increase token count
    for token in tokens:
        if token not in vocab:
            vocab[token] = 1
        else:
            vocab[token] += 1  
# sort the vocab according to the frequency in decreasing order
vocab = dict(sorted(vocab.items(), key = lambda item : item[1], reverse=True))

# save the vocab in text file
with open("tf-idf/vocab.txt","w",encoding="utf-8") as file:
    for key in vocab.keys():
        file.write(key + "\n")

#save the idf values of vocab in text file
with open("tf-idf/idf-values.txt","w",encoding="utf-8") as file:
    for key in vocab.keys():
        file.write(str(vocab[key]) + "\n")

#save all the documents in a text file
with open("tf-idf/documents.txt","w",encoding="utf-8") as file:
    for document in documents:
        file.write(" ".join(document) + "\n")

for index, document in enumerate(documents):
    for token in document:
        if token not in inverted_index:
            inverted_index[token] = [index]
        else:
            inverted_index[token].append(index)

#save the inverted index in text file
with open("tf-idf/inverted-index.txt","w",encoding="utf-8") as file:
    for key in inverted_index.keys():
        file.write(key + "\n")
        file.write(" ".join([str(doc_id) for doc_id in inverted_index[key]]) + "\n")



print("Numbet of documents: ", len(documents))
print("Size of vocab: ", len(vocab))
print("Sample document: ", documents[1])

