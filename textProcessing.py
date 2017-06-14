import collections
import numpy as np
def build_dataset(words, vocabulary_size):
  count = [['UNK', -1]]
  count.extend(collections.Counter(words).most_common(vocabulary_size - 1))
  dictionary = dict()
  for word, _ in count:
    dictionary[word] = len(dictionary)
  data = list()
  unk_count = 0
  for word in words:
    if word in dictionary:
      index = dictionary[word]
    else:
      index = 0  # dictionary['UNK']
      unk_count = unk_count + 1
    data.append(index)
  count[0][1] = unk_count
  reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys())) 
  return data, count, dictionary, reverse_dictionary

def build_contexts(window_size, data, dictionary):
    n = len(data)
    dict_size = len(dictionary)
    print dict_size, n - window_size * 2 - 1
    X = set()
    for i in xrange(window_size, n - window_size-1):
        context = set(data[i-window_size:i] + data[i+1:i+window_size+1])
        context = context - set([0])
        context = tuple(context)
        X.add(context)
    return list(X)

def find_contexts( word, window_size, data, dictionary ) :
    idx = dictionary.get(word)
    if idx is None :
        raise BaseException('Word not in a dictionary')
    print idx
    positions = [i for i,x in enumerate(data) if x == idx]
    ret = []
    for position in positions : 
        ret.append( data[position-window_size:position] + data[position+1:position+window_size+1] )
    return ret

def signature( word, window_size, data, dictionary,som ) :
    ctxs = find_contexts(word, window_size, data, dictionary)
    loc = som.map_vects( ctxs )
    sign = np.zeros((d,d))
    for x,y in loc :
        sign[x,y] += 1 
    return sign
        

    
def compute_signatures(window_size, data, dictionary,som) :
    signatures = {}
    count = 0
    for word,n in dictionary.items() : 
        if n>0 :
            sign = signature(word, window_size,data, dictionary,som)
            signatures[word] = sign
            print word
        count+=1
        #if count> 100 : 
        #    break
    return signatures

def find_similar(signatures, query, threshold = 0) : 
    query_signature = signatures[query]
    query_binary = query_signature > threshold
    similarity = []
    for word, signature in signatures.items() :
        signature_binary = signature > threshold
        similarity.append( (np.sum(np.bitwise_and(query_binary, signature_binary)), word) )
        
    similarity.sort()
    return similarity[-25:]
