# import pandas as pd
# import numpy as np

# url = 'https://www.pro-football-reference.com/boxscores/202209110htx.htm#all_passing_advanced'




# df = pd.read_html(url)

# print(df[2])


# # print(df)
# # # df = df.fillna(0)

#'https://www.pro-football-reference.com/boxscores/202210300ram.htm'
#'https://www.pro-football-reference.com/boxscores/202301290phi.htm'

# # # df.to_csv('testing.csv')


import requests
from bs4 import BeautifulSoup
import pandas as pd
import regex as re
import urllib.request
import urllib.error
import time
from apyori import apriori




# url = 'https://www.pro-football-reference.com/boxscores/202209110chi.htm'
# resDf = pd.DataFrame()
# lst = ['https://www.pro-football-reference.com/boxscores/202209110chi.htm', 'https://www.pro-football-reference.com/boxscores/202209250den.htm'
#        , 'https://www.pro-football-reference.com/boxscores/202210090car.htm', 'https://www.pro-football-reference.com/boxscores/202210160atl.htm'
#        , 'https://www.pro-football-reference.com/boxscores/202211210crd.htm',
#        'https://www.pro-football-reference.com/boxscores/202212150sea.htm', 'https://www.pro-football-reference.com/boxscores/202301010rai.htm'
#        ]


# for i in lst:


#     response = requests.get(i)



#     winOrLoss = 1   #1 for win, 0 for loss

#     tie = 0



#     df = pd.read_html(i)

#     scores = df[0]

#     first_row = scores.iloc[0]
#     second_row = scores.iloc[1]


#     if(first_row['Final']>second_row['Final']):

#         if(first_row['Unnamed: 1']=="San Francisco 49ers"):

#             winOrLoss = 1

#         else:

#             winOrLoss = 0

#     elif(first_row['Final']<second_row['Final']):

#         if(first_row['Unnamed: 1']=="San Francisco 49ers"):

#             winOrLoss = 0

#         else:

#             winOrLoss = 1

#     else:
#         tie = 1


#     stringWinOrLoss = ""
#     if(winOrLoss):

#         stringWinOrLoss+="Win"

#     else:
#         stringWinOrLoss+="Loss"






#     soup = BeautifulSoup(response.content, 'html.parser')




#     # tags = soup.find_all(class_="table_wrapper setup_commented commented")

#     # for i in tags:

#     #     print(i.prettify())

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

#     df = pd.read_html(advancedPassing)


#     df = df[0]

#     df['W/L'] = stringWinOrLoss

#     idx = (df[df['Player'] == 'Player'].index)

#     dfLen = len(df)



#     if((df.iloc[idx-1]['Tm'][0])=='SFO'):
#         ninersSubset = df.iloc[:idx[0]]
#         resDf = pd.concat([ninersSubset, resDf])
#         #print(ninersSubset)

#     else:

#         ninersSubset = df.loc[idx[0]+1:dfLen]
#         resDf = pd.concat([ninersSubset, resDf])

#         #print(ninersSubset)

# resDf.fillna(0)
# resDf.to_csv('testing.csv')
# print(resDf)


df = pd.read_csv('testing.csv')
df = df.drop('Tm', axis=1)
df = df.drop('Unnamed: 0', axis=1)

tempDf = df.copy()
tempDf['Drop%'] = tempDf['Drop%'].str.rstrip('%')
tempDf['Bad%'] = tempDf['Bad%'].str.rstrip('%')
tempDf['Prss%'] = tempDf['Prss%'].str.rstrip('%')



subset = tempDf['Player']
tempDf.drop('Player', axis=1, inplace=True)
temp = tempDf['W/L']
tempDf.drop('W/L', axis=1, inplace=True)
tempDf.fillna(0, inplace=True)
tempDf = tempDf.astype(float)




for col in tempDf.columns:
    avg = tempDf[col].mean()
    
    def check_value(val, name):
        if val >= avg:
            return ">avg"+name
        else:
            return "<avg"+name
    
    tempDf[col] = tempDf[col].apply(check_value, args=(col,))


tempDf['W/L'] = temp
tempDf['Player'] = subset
tempDf.fillna(0, inplace=True)
tempDf.to_csv('copy.csv')
# print(tempDf.columns)


length = len(tempDf)
records = []
for i in range(0, length):
    records.append([str(tempDf.values[i,j]) for j in range(0, 26)])
association_rules = apriori(records, min_support=0.55, min_confidence=0.9, min_lift=1)
association_results = list(association_rules)
print(len(association_results))
for item in association_results:

    # first index of the inner list
    # Contains base item and add item
    pair = item[0] 
    items = [x for x in pair]
    print("Rule: " + items[0] + " -> " + items[1])

    #second index of the inner list
    print("Support: " + str(item[1]))

    #third index of the list located at 0th
    #of the third index of the inner list

    print("Confidence: " + str(item[2][0][2]))
    print("Lift: " + str(item[2][0][3]))
    print("=====================================")




























































# temp = soup.find_all(id="all_rushing_advanced")
# x = temp[0]
# x = str(x)

# last = len(x)

# y = (re.search('<div class="table_container" id="div_rushing_advanced">', x))
# start = y.start()

# newStr = (x[start:last])

# tableRe = re.search('</table>', newStr)
# end = tableRe.end()

# advancedRushing = newStr[0: end]

# df = pd.read_html(advancedRushing)







# temp = soup.find_all(id="all_receiving_advanced")
# x = temp[0]
# x = str(x)

# last = len(x)

# y = (re.search('<div class="table_container" id="div_receiving_advanced">', x))
# start = y.start()

# newStr = (x[start:last])

# tableRe = re.search('</table>', newStr)
# end = tableRe.end()

# advancedReceiving = newStr[0: end]

# df = pd.read_html(advancedReceiving)




# temp = soup.find_all(id="all_defense_advanced")
# x = temp[0]
# x = str(x)

# last = len(x)

# y = (re.search('<div class="table_container" id="div_defense_advanced">', x))
# start = y.start()

# newStr = (x[start:last])

# tableRe = re.search('</table>', newStr)
# end = tableRe.end()

# advancedDefense = newStr[0: end]

# df = pd.read_html(advancedDefense)



