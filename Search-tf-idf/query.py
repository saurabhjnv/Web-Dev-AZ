import math
def load_links():
    question_links = []
    with open("Leetcode-Scrapper-Question/Qindex.txt","r") as f:
        question_links = f.readlines()
        # use strip to cutoff "\n"
        question_links = [link.strip() for link in question_links]
    return question_links


def load_documents():
    documents = []
    with open("tf-idf/documents.txt","r") as f:
       documents = f.readlines()
       documents = [document.strip().split() for document in documents]
    return documents   

def load_vocab():
    vocab = {}
    with open("tf-idf/vocab.txt","r") as f:
        vocab_terms = f.readlines()
    with open("tf-idf/idf-values.txt","r") as f:
        vocab_idf_values = f.readlines()
    for (term,idf_value) in zip(vocab_terms,vocab_idf_values):
        vocab[term.strip()] = int(idf_value.strip())
    return vocab

def load_inverted_index():
    # inverted_index contains all counting of a term. eg - {bank : 0  748 748 748 748 748 748 748 840 873 873 1052 1052 1052 1052 1052 1565 1565 1565 1565 1588 1588 1588 1588 1798 1798 1994 1994 1994}
    inverted_index = {}
    with open("tf-idf/inverted-index.txt","r") as f:
        inverted_index_terms = f.readlines()

    for row_num in range(0,len(inverted_index_terms),2):
        term = inverted_index_terms[row_num].strip()
        documents = inverted_index_terms[row_num+1].strip().split()
        inverted_index[term] = documents
    return inverted_index
 

# variables
query_string = input("Enter your query: ")
query_terms = [term.lower() for term in query_string.strip().split()]
documents = load_documents()
vocab_idf_values = load_vocab()
inverted_index = load_inverted_index()
question_links = load_links()

def get_tf_dictionary(term):
    tf_values = {}
    if term in inverted_index.keys():
        for doc_id in inverted_index[term]:
            if doc_id in tf_values.keys():
                tf_values[doc_id] += 1
            else:
                tf_values[doc_id] = 1
    for doc_id in tf_values:
        tf_values[doc_id] /= len(documents[int(doc_id)])             
    return tf_values 
               
def get_idf_values(term):
    idf_value = math.log(len(documents) / vocab_idf_values[term])
    return idf_value


def calculate_sorted_order_of_documents(query_terms):
    # stores the documents with its score associated with the query terms
    potential_documents = {} 

    for term in query_terms:
        if vocab_idf_values[term] == 0:
            continue
        tf_value_by_document = get_tf_dictionary(term)
        idf_value = get_idf_values(term)
        #calculation of tf-idf scores and storing the {document + score(avg of tf-idf)} in potential_documents
        for doc_id in tf_value_by_document:
            if doc_id not in potential_documents:
                potential_documents[doc_id] = tf_value_by_document[doc_id] * idf_value
            else:
                potential_documents[doc_id] += tf_value_by_document[doc_id] * idf_value
    #calculating the avg score of document for query terms
    for doc_id in potential_documents:
        potential_documents[doc_id] /= len(query_terms)
    
    #sorting the potential_documents by the score of the documents
    potential_documents = dict(sorted(potential_documents.items(), key = lambda item : item[1], reverse=True))

    return potential_documents 


print("Numbet of documents: ", len(documents))
# print("Size of vocab: ", len(vocab_idf_values))
# print("Size of inverted index: ", len(inverted_index))
# print("Sample document: ", documents[0])
# print("Inverted index of the term 'the' : ", inverted_index["the"])

potential_documents = calculate_sorted_order_of_documents(query_terms)

# Top 15 related documents with links printing
print("Top 15 documents related to ",query_terms)
for index,doc_id in enumerate(potential_documents) :
    print("Document index : ", int(doc_id)+1, "\t :","Score: ", potential_documents[doc_id],"\t", question_links[int(doc_id)])
    if index == 14:
        break


