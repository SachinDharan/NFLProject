import pandas as pd

import requests
from bs4 import BeautifulSoup
import pandas as pd
import regex as re
import urllib.request
import urllib.error
import time
from apyori import apriori
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules



# url = 'https://www.pro-football-reference.com/teams/min/2022.htm'

# response = requests.get(url)

# soup = BeautifulSoup(response.content, 'html.parser')

# text = str(soup)

# pattern = r'data-stat="game_result" ><([^,]*)'
# matches = re.findall(pattern, text)
# mySet = set(matches)

# lst = list(mySet)
# scoreList = []
# for i in lst:

#     link = i[8:-3]
#     res = i[-1]
#     scoreList.append((link, res))



# refString = 'https://www.pro-football-reference.com/'

# rushingDf = pd.DataFrame()
# passingDf = pd.DataFrame()
# receivingDf = pd.DataFrame()
# defenseDf = pd.DataFrame()



# for i in scoreList:

        
#     url = refString+str(i[0])
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')


#     temp = soup.find_all(id="all_rushing_advanced")
#     x = temp[0]
#     x = str(x)
#     last = len(x)
#     y = (re.search('<div class="table_container" id="div_rushing_advanced">', x))
#     start = y.start()
#     newStr = (x[start:last])
#     tableRe = re.search('</table>', newStr)
#     end = tableRe.end()
#     advancedRushing = newStr[0: end]
#     tempRush = pd.read_html(advancedRushing)[0]
#     tempRush['W/L'] = i[1]
#     rushingDf = pd.concat([rushingDf, tempRush])



#     temp = soup.find_all(id="all_passing_advanced")
#     x = temp[0]
#     x = str(x)
#     last = len(x)
#     y = (re.search('<div class="table_container" id="div_passing_advanced">', x))
#     start = y.start()
#     newStr = (x[start:last])
#     tableRe = re.search('</table>', newStr)
#     end = tableRe.end()
#     advancedPassing = newStr[0: end]
#     tempPassing = pd.read_html(advancedPassing)[0]
#     tempPassing['W/L'] = i[1]
#     passingDf = pd.concat([passingDf, tempPassing])
  


#     temp = soup.find_all(id="all_receiving_advanced")
#     x = temp[0]
#     x = str(x)
#     last = len(x)
#     y = (re.search('<div class="table_container" id="div_receiving_advanced">', x))
#     start = y.start()
#     newStr = (x[start:last])
#     tableRe = re.search('</table>', newStr)
#     end = tableRe.end()
#     advancedReceiving = newStr[0: end]
#     tempRec = pd.read_html(advancedReceiving)[0]
#     tempRec['W/L'] = i[1]
#     receivingDf = pd.concat([receivingDf, tempRec])


#     temp = soup.find_all(id="all_defense_advanced")
#     x = temp[0]
#     x = str(x)
#     last = len(x)
#     y = (re.search('<div class="table_container" id="div_defense_advanced">', x))
#     start = y.start()
#     newStr = (x[start:last])
#     tableRe = re.search('</table>', newStr)
#     end = tableRe.end()
#     advancedDef = newStr[0: end]
#     tempDef = pd.read_html(advancedDef)[0]
#     tempDef['W/L'] = i[1]
#     defenseDf = pd.concat([defenseDf, tempDef])




# rushingDf.to_csv('testingOne.csv')
# passingDf.to_csv('testingTwo.csv')
# receivingDf.to_csv('testingThree.csv')
# defenseDf.to_csv('testingFour.csv')



rushingDf = pd.read_csv('testingOne.csv')
passingDf = pd.read_csv('testingTwo.csv')
receivingDf = pd.read_csv('testingThree.csv')
defenseDf = pd.read_csv('testingFour.csv')





rushingDf = rushingDf.drop('Unnamed: 0', axis=1)
rushingDf = rushingDf.fillna(0)
rushingDf = rushingDf.drop_duplicates()

temp = rushingDf[rushingDf['Tm']=='MIN']
temp = temp[temp['Tm']!='Player']
temp = temp.fillna(0)
temp = temp.drop('Tm', axis=1)
players = temp['Player']
winLoss = temp['W/L']
temp = temp.drop('Player', axis=1)
temp = temp.drop('W/L', axis=1)

temp = temp.astype(float)



for col in temp.columns:
    avg = temp[col].mean()
    
    def check_value(val, name):
        if val >= avg:
            return ">avg"+name
        else:
            return "<avg"+name
    
    temp[col] = temp[col].apply(check_value, args=(col,))

temp.insert(0, 'Player', players)
temp.insert(0, 'W/L', winLoss)


records = []
for i in range(len(temp)):
    records.append([str(temp.values[i,j]) for j in range(12)])





te = TransactionEncoder()
te_ary = te.fit(records).transform(records)
df = pd.DataFrame(te_ary, columns=te.columns_)
freqItems = (apriori(df, min_support=0.6, use_colnames=True))
filtered_itemsets = freqItems[freqItems['itemsets'].apply(lambda x: any([item in temp['W/L'].values for item in x])) & freqItems['itemsets'].apply(lambda x: len(x) > 1)]
filteredRules = association_rules(freqItems, metric='lift', min_threshold=1.5) 

print(filtered_itemsets)
print(filteredRules)
print()




temp = receivingDf[receivingDf['Tm']=='MIN']
temp = temp[temp['Tm']!='Player']
temp = temp.fillna(0)
temp = temp.drop('Tm', axis=1)
temp = temp.drop('Unnamed: 0', axis=1)
players = temp['Player']
winLoss = temp['W/L']
temp = temp.drop('Player', axis=1)
temp = temp.drop('W/L', axis=1)

temp = temp.astype(float)



for col in temp.columns:
    avg = temp[col].mean()
    
    def check_value(val, name):
        if val >= avg:
            return ">avg"+name
        else:
            return "<avg"+name
    
    temp[col] = temp[col].apply(check_value, args=(col,))

temp.insert(0, 'Player', players)
temp.insert(0, 'W/L', winLoss)

temp.to_csv('copy.csv')
num_cols = temp.shape[1]


records = []
for i in range(len(temp)):
    records.append([str(temp.values[i,j]) for j in range(num_cols)])


te = TransactionEncoder()
te_ary = te.fit(records).transform(records)
df = pd.DataFrame(te_ary, columns=te.columns_)
freqItems = (apriori(df, min_support=0.6, use_colnames=True))
filtered_itemsets = freqItems[freqItems['itemsets'].apply(lambda x: any([item in temp['W/L'].values for item in x])) & freqItems['itemsets'].apply(lambda x: len(x) > 1)]
filteredRules = association_rules(freqItems, metric='lift', min_threshold=1.5) 

print(filtered_itemsets)
print(filteredRules)
print()





temp = passingDf[passingDf['Tm']=='MIN']
temp = temp[temp['Tm']!='Player']
temp = temp.fillna(0)
temp = temp.drop('Tm', axis=1)
temp = temp.drop('Unnamed: 0', axis=1)
players = temp['Player']
winLoss = temp['W/L']
temp = temp.drop('Player', axis=1)
temp = temp.drop('W/L', axis=1)

temp['Drop%'] = temp['Drop%'].str.rstrip('%')
temp['Bad%'] = temp['Bad%'].str.rstrip('%')
temp['Prss%'] = temp['Prss%'].str.rstrip('%')

temp = temp.astype(float)



for col in temp.columns:
    avg = temp[col].mean()
    
    def check_value(val, name):
        if val >= avg:
            return ">avg"+name
        else:
            return "<avg"+name
    
    temp[col] = temp[col].apply(check_value, args=(col,))

temp.insert(0, 'Player', players)
temp.insert(0, 'W/L', winLoss)

temp.to_csv('copy.csv')
num_cols = temp.shape[1]


records = []
for i in range(len(temp)):
    records.append([str(temp.values[i,j]) for j in range(num_cols)])


te = TransactionEncoder()
te_ary = te.fit(records).transform(records)
df = pd.DataFrame(te_ary, columns=te.columns_)
freqItems = (apriori(df, min_support=0.6, use_colnames=True))
filtered_itemsets = freqItems[freqItems['itemsets'].apply(lambda x: any([item in temp['W/L'].values for item in x])) & freqItems['itemsets'].apply(lambda x: len(x) > 1)]
filteredRules = association_rules(freqItems, metric='lift', min_threshold=1.5) 

print(filtered_itemsets)
print(filteredRules)
print()







temp = defenseDf[defenseDf['Tm']=='MIN']
temp = temp[temp['Tm']!='Player']
temp = temp.fillna(0)
temp = temp.drop('Tm', axis=1)
temp = temp.drop('Unnamed: 0', axis=1)
players = temp['Player']
winLoss = temp['W/L']
temp = temp.drop('Player', axis=1)
temp = temp.drop('W/L', axis=1)

temp['Cmp%'] = temp['Cmp%'].str.rstrip('%')
temp['MTkl%'] = temp['MTkl%'].str.rstrip('%')

temp = temp.astype(float)



for col in temp.columns:
    avg = temp[col].mean()
    
    def check_value(val, name):
        if val >= avg:
            return ">avg"+name
        else:
            return "<avg"+name
    
    temp[col] = temp[col].apply(check_value, args=(col,))

temp.insert(0, 'Player', players)
temp.insert(0, 'W/L', winLoss)

temp.to_csv('copy.csv')
num_cols = temp.shape[1]


records = []
for i in range(len(temp)):
    records.append([str(temp.values[i,j]) for j in range(num_cols)])


te = TransactionEncoder()
te_ary = te.fit(records).transform(records)
df = pd.DataFrame(te_ary, columns=te.columns_)
freqItems = (apriori(df, min_support=0.6, use_colnames=True))
filtered_itemsets = freqItems[freqItems['itemsets'].apply(lambda x: any([item in temp['W/L'].values for item in x])) & freqItems['itemsets'].apply(lambda x: len(x) > 1)]
filteredRules = association_rules(freqItems, metric='lift', min_threshold=1.5) 

print(filtered_itemsets)
print(filteredRules)
print()