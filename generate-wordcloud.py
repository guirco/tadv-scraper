from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

stopwords = set(STOPWORDS)
stopwords.add('museu')
stopwords.add('todo')
stopwords.add('toda')
stopwords.add('pois')
stopwords.add('ainda')
stopwords.add('dia')
stopwords.add('onde')
stopwords.add('tudo')
stopwords.add('sobre')
stopwords.add('lá')
stopwords.add('pode')
stopwords.add('porque')
stopwords.add('faz')
stopwords.add('então')
stopwords.add('pra')
stopwords.add('deve')
stopwords.add('assim')
stopwords.add('cada')
stopwords.add('alguma')
stopwords.add('existem')
stopwords.add('dá')
stopwords.add('dentro')
stopwords.add('deste')
stopwords.add('tão')
stopwords.add('passar')
stopwords.add('quase')
stopwords.add('Além')
stopwords.add('ir')
stopwords.add('vai')
stopwords.add('algo')
stopwords.add('etc')
stopwords.add('algumas')
stopwords.add('deixar')
stopwords.add('todas')
#stopwords.add('chile')

#Adicionando a lista stopwords em português
new_words = []
with open("stopwords-pt.txt", 'r') as f:
    [new_words.append(word) for line in f for word in line.split()]
new_stopwords = stopwords.union(new_words)

all_text = ""
for file in range(0,1):
    file = open("ReviewsOnly-MMDH-Santiago-6113c-Translated.csv")
    lines = file.readlines()
    
    for line in lines:
        all_text += " " + line

wordcloud = WordCloud(width = 1920, height = 1080, stopwords = new_stopwords, background_color ='white',  min_font_size = 10)

wordcloud.generate(all_text)

plt.figure(figsize = (1.920, 1.080), dpi=100, facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
plt.savefig('plots/word_cloud.png', dpi=1000)
plt.show()