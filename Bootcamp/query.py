import math
from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)



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

def load_docs_heading():
    lines = []
    docs_heading = []
    with open("Leetcode-Scrapper-Question/index.txt","r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split(".")[1].strip()
            docs_heading.append(line)
    return docs_heading



# ---- for terminal ------
# query_string = input("Enter your query: ")
# query_terms = [term.lower() for term in query_string.strip().split()]


# ---------variables-------------
documents = load_documents()
vocab_idf_values = load_vocab()
inverted_index = load_inverted_index()
question_links = load_links()
docs_heading = load_docs_heading()
#--------------------------------

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
        if term not in vocab_idf_values:
        #if vocab_idf_values[term] == 0:
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

# Top 15 related documents with links printing
def top_results(potential_documents):
    top_links = []
    #print("Top 15 documents related to ",query_terms)
    for index,doc_id in enumerate(potential_documents) :
        #print("Document index : ", int(doc_id)+1, "\t :","Score: ", potential_documents[doc_id],"\t", question_links[int(doc_id)])
        # adding links in top_links list and will use it later.
        top_links.append(question_links[int(doc_id)])
        if index == 14:
            break
    return top_links

def top_doc_name(potential_documents):
    doc_name = []
    #print("Top 15 documents related to ",query_terms)
    for index,doc_id in enumerate(potential_documents) :
        #print("Document index : ", int(doc_id)+1, "\t :","Score: ", potential_documents[doc_id],"\t", question_links[int(doc_id)])
        # adding links in top_links list and will use it later.
        doc_name.append(docs_heading[int(doc_id)])
        if index == 14:
            break
    return doc_name
# print("Numbet of documents: ", len(documents))
# print("Size of vocab: ", len(vocab_idf_values))
# print("Size of inverted index: ", len(inverted_index))
# print("Sample document: ", documents[0])
# print("Inverted index of the term 'the' : ", inverted_index["the"])

# Top 15 related documents with links printing
# ------for terminal------
"""
potential_documents = calculate_sorted_order_of_documents(query_terms)
top_links = top_results(potential_documents)
top_docs = top_doc_name(potential_documents)
"""






@app.route("/", methods = ["GET","POST"])
def start_page():
    if request.method == "POST":
        # getting input with name = Query in HTML form
        query_string = request.form.get("Query")
        query_terms = [term.lower() for term in query_string.strip().split()]
        potential_documents = calculate_sorted_order_of_documents(query_terms)
        top_links = top_results(potential_documents)
        top_docs = top_doc_name(potential_documents)
        return render_template("output.html", links = top_links, docs_name = top_docs)
    else:
        return render_template("index.html")
    
@app.route("/<query>", methods = ["GET"])
def search(query):

    # getting input with name = Query in HTML form
    query_terms = query
    query_terms = [term.lower() for term in query_terms.strip().split()]
    potential_documents = calculate_sorted_order_of_documents(query_terms)
    top_links = top_results(potential_documents)
    top_docs = top_doc_name(potential_documents)
    return render_template("output.html", links = top_links, docs_name = top_docs)

if __name__ == "__main__":
    app.run(debug=True)