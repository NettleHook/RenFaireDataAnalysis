import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


#Making a data frame from the data observed at a californian renaissance faire, superhero weekend, Saturday only
#Unfortunately limited by only counting what I was able to recognize
observed=['Zelda', 'Hercules', 'Donkey', 'Gandalf', 'Non-descript Jedi', 'Loki', 'Wonder Woman', 'Westley', 'Harley Quinn',
          'Link', 'Harley Quinn', 'Loki', 'Joker', 'Shego', 'Captain America', 'Midoriya Deku', 'Mona', 'Joker', 'Maleficent', 'Harley Quinn', 'Link', 'Ahsoka', 'Non-descript Jedi', 'Teenage Mutant Ninja Turtle',
          'Link', 'Link', 'Megara', 'Harley Quinn', 'Spiderman', 'Link', 'Midna', 'Fiona', 'Megara', 'Sherrif of Nottingham', 'Superman', 'Robin Hood', 'Deadpool', 'Batman', 'Shrek', 'Gandalf', 'Hades', 'Fiona']

#Create the lists that will be columns in the data frame (media source, gender of character, year of observation
media_src=[]
gender=[]
year=[2023]*len(observed)
for inst in observed:
    if inst in ['Wonder Woman', 'Superman', 'Harley Quinn', 'Batman', 'Joker']:
       media_src.append('DC')
    elif inst in ['Captain America', 'Loki', 'Spiderman', 'Deadpool', 'Teenage Mutant Ninja Turtle']:
        media_src.append('Marvel')
    elif inst in ['Ahsoka', 'Non-descript Jedi']:
        media_src.append('Star Wars')
    elif inst in ['Robin Hood', 'Fiona', 'Donkey', 'Shrek', 'Hercules', 'Megara', 'Shego', 'Maleficent', 'Sherrif of Nottingham', 'Hades']:
        media_src.append('Disney')
    elif inst in ['Midna', 'Link', 'Zelda']:
        media_src.append('Legend of Zelda')
    elif inst in ['Gandalf']:
        media_src.append('LOTR')
    elif inst in ['Mona']:
        media_src.append('Genshin Impact')
    elif inst in ['Midoriya Deku']:
        media_src.append('MHA')
    elif inst in ['Westley']:
        media_src.append('Princess Bride')
    else:
        media_src.append('Other')
    if inst in ['Wonder Woman', 'Harley Quinn', 'Ahsoka', 'Mona', 'Shego', 'Maleficent', 'Megara', 'Fiona', 'Midna', 'Zelda']:
        gender.append('Fem')
    elif inst in ['Loki', 'Non-descript Jedi']:
        gender.append('NB')
    else:
        gender.append('Masc')
obs_df = pd.DataFrame({'Characters':observed,
                       'Media Source': media_src,
                       'Gender':gender,
                       'Year':year})
obs_df['Media Source'] = obs_df['Media Source'].astype(pd.CategoricalDtype(['DC', 'Disney', 'LOTR', 'Marvel', 'Star Wars', 'Legend of Zelda', 'Genshin Impact', 'MHA', 'Princess Bride'], ordered = True))
plt.figure(figsize=(12, 8))
sns.set_palette(sns.color_palette('husl',10))
sns.set_context('paper')
sns.countplot(x='Media Source', data=obs_df, hue = 'Media Source')
plt.title('CA RenFair Cosplay Count')
plt.xticks(rotation=80)
#plt.show()
plt.savefig('../graphs/CARenFaireCosCount2023.svg')
obs_df.to_csv('../csvs/RenFaireObservations.csv', index=False)
