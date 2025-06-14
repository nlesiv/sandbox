import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer

p_stemmer = PorterStemmer()
s_stemmer = SnowballStemmer("english")

words =[
    'run',
    'runner',
    'ran',
    'runs',
    'easily',
    'fairly'
]

for word in words:
    print (word + ' ---> ' + p_stemmer.stem(word))

    
for word in words:
    print (word + ' ---> ' + s_stemmer.stem(word))