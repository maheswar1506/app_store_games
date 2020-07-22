import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import missingno as msno
import seaborn as sns
import datetime
import os

import warnings
warnings.filterwarnings("ignore")

#changing working directory
os.chdir("/home/master/Downloads/")

#Reading data
data = pd.read_csv("appstore_games.csv")


#Data cleaning

#Dropping unused columns and rows with no data of User rating count
names = ['URL','ID','Subtitle','Icon URL','Description','Developer','Primary Genre']
data = data.drop(columns=names)
data.columns = ['Name','Average User Rating','User Rating Count','Price','In-app Purchases','Age Rating','Languages','Size','Genres','Original Release Date','Current Version Release Date']
data = data[pd.notnull(data['User Rating Count'])]

#finding time gap between original release date and current version date
data['Original Release Date'] = pd.to_datetime(data['Original Release Date'])
data['Current Version Release Date'] = pd.to_datetime(data['Current Version Release Date'])
data['update_time'] = data['Current Version Release Date']-data['Original Release Date']
data['update_time'] = data['update_time']/np.timedelta64(1,'M')

#dropping rows with update time < 6 months and user rating count < 200
data.drop(data[data['update_time']<6].index ,inplace=True)
data.drop(data[data['User Rating Count']<200].index,inplace=True)



# games and entertainment tags are removed
data['Genres'] = data['Genres'].str.replace(',', '').str.replace('Games', '').str.replace('Entertainment', '')
data['Genres'] = data['Genres'].str.split(' ').map(lambda x: ' '.join(sorted(x)))
data['Genres']= data['Genres'].str.strip()

"""

    Puzzle= Puzzle/Board
    Adventure= Adventure/Role/Role Playing
    Action = Action
    Family = Family/Education

"""

data.loc[data['Genres'].str.contains('Puzzle'),'Genres'] = 'Puzzle'
data.loc[data['Genres'].str.contains('Board'),'Genres'] = 'Puzzle'
data.loc[data['Genres'].str.contains('Adventure'),'Genres'] = 'Adventure'
data.loc[data['Genres'].str.contains('Role'),'Genres'] = 'Adventure'
data.loc[data['Genres'].str.contains('Role Playing'),'Genres'] = 'Adventure'
data.loc[data['Genres'].str.contains('Action'),'Genres'] = 'Action'
data.loc[data['Genres'].str.contains('Family'),'Genres'] = 'Family'
data.loc[data['Genres'].str.contains('Education'),'Genres'] = 'Family'

#determining number of games exist per genre having rating 4-5

#creating another copy having ratings only between 4-5
db = data.copy()
db.drop(db[db['Average User Rating']<4].index,inplace=True)


#bar plot
x=['Puzzle','Action','Adventure','Family']
y = [data['Genres'][(data['Genres']=='Puzzle')].count(),data['Genres'][(data['Genres']=='Action')].count(),     data['Genres'][(data['Genres']=='Adventure')].count(),data['Genres'][(data['Genres']=='Family')].count()]
plt.bar(x,y,width=0.4,color=('r','g','b','black'))
plt.title('Games per Genre in all data')
plt.xlabel('Genres')
plt.ylabel('Number of games')
plt.show()

#pie chart

sizes = [data['Genres'][data['Genres']=='Puzzle'].count(),data['Genres'][data['Genres']=='Action'].count(),     data['Genres'][data['Genres']=='Adventure'].count(),data['Genres'][data['Genres']=='Family'].count()]
names= ['Puzzle','Action','Adventure','Family']
plt.pie(sizes, labels=names, startangle=90, autopct='%.1f%%')
plt.title('Games per genre in  all data')
plt.show()

print("from bar plot and pie chart we can see for all games in data follows the order puzzle > adventure > action > Family")

#bar plot
x=['Puzzle','Action','Adventure','Family']
y = [db['Genres'][(db['Genres']=='Puzzle')].count(),db['Genres'][(db['Genres']=='Action')].count(),db['Genres'][(db['Genres']=='Adventure')].count(),db['Genres'][(db['Genres']=='Family')].count()]
plt.bar(x,y,width=0.4,color=('r','g','b','black'))
plt.title('Games per Genre in data with rating between 4-5')
plt.xlabel('Genres')
plt.ylabel('Number of games')
plt.show()

#pie chart

sizes = [db['Genres'][db['Genres']=='Puzzle'].count(),db['Genres'][db['Genres']=='Action'].count(),db['Genres'][db['Genres']=='Adventure'].count(),db['Genres'][db['Genres']=='Family'].count()]
names= ['Puzzle','Action','Adventure','Family']
plt.pie(sizes, labels=names, startangle=90, autopct='%.1f%%')
plt.title('Games per genre in data with rating between 4-5')
plt.show()

print("from bar plot and pie chart we can see that games of rating between 4-5 follows the order puzzle > adventure > action > Family\n")


#Rough estimation by sorting

test = data.sort_values(by='User Rating Count', ascending=False)[['Name', 'Average User Rating','Genres', 'User Rating Count']].head(8)
print(test.iloc[:, 0:-1])
print("\n")

print("from above result , more people has given good rating for apps having genre of action and it is followed by adventure when sorted by User rating count")

test = data.sort_values(by=['Price','In-app Purchases'], ascending=False)[['Name','Genres','In-app Purchases','Price']].head(8)
print(test.iloc[:, 0:-1])
print("\n")

print("from above result , puzzle apps are good when sorted by price and in app purchases")


test = data.sort_values(by='Size', ascending=True)[['Name','Genres','Size']].head(8)
print(test.iloc[:, 0:-1])
print("\n")

print("from above result , puzzle apps are good when sorted by size")
print("\n")


#distplot 

plt.figure(figsize = (18, 10),dpi=80)
sns.distplot(data['Price'])
plt.ylabel('Count',fontsize=20)
plt.xlabel('Price',fontsize=20)
plt.title('Distplot for all')
plt.show()

print("from the dist plot shown above price is between 0-11 for all data")
print("\n")

#distplot 

plt.figure(figsize = (18, 10),dpi=80)
sns.distplot(db['Price'])
plt.ylabel('Count',fontsize=20)
plt.xlabel('Price',fontsize=20)
plt.title('Distplot for data wth rating between 4-5')
plt.show()

print("from the dist plot shown above price is between 0-11 for all data")
print("\n")

#scatter plot

plt.scatter(x=data['Average User Rating'],y=data['Price'],marker='o')
plt.xlabel('Average User Rating')
plt.ylabel('Price')
plt.title('Average User Rating  vs  Price')
plt.show()

print("from above rating vs price graph we can see that price for good rating is less than 11 ")
print("\n")

#pie chart

plt.pie(data['Age Rating'].value_counts().values,labels=data['Age Rating'].value_counts().index,startangle=90, autopct='%.1f%%')
plt.title('Age rating for all data')
plt.show()
print("from above pie chart 4+ age rating apps have good rating")
print("\n")


plt.pie(db['Age Rating'].value_counts().values,labels=data['Age Rating'].value_counts().index,startangle=90, autopct='%.1f%%')
plt.title('Age rating for data with rating 4-5')
plt.show()
print("from above pie chart 4+ age rating apps have good rating")
print("\n")

#finding correlation

dtf = data['Genres'].apply(lambda s : s.replace('Games','').replace('&',' ').replace(',', ' ').split()) 
from sklearn.preprocessing import MultiLabelBinarizer
test = dtf
mlb = MultiLabelBinarizer()
res = pd.DataFrame(mlb.fit_transform(test), columns=mlb.classes_, index=test.index)

#heatmap

plt.figure(figsize=(8,8))
sns.heatmap(res.corr(),cmap=sns.diverging_palette(220, 10, as_cmap=True),mask=np.zeros_like(res.corr(), dtype=np.bool),vmax=.3, center=0,square=True, linewidths=.5, cbar_kws={"shrink": .5})
plt.title("correlation")
plt.show()

print("from the above heat map a very good positive correlation exists between : ")
print('Education and food\nhealth and fitness\nplaying and role')
print("\n")

#for size

plt.scatter(x=data['Average User Rating'],y=data['Size'],marker='^')
plt.xlabel('Average User Rating')
plt.ylabel('Size')
plt.title('Average User Rating  vs  Size for all')
plt.show()

print("from above Average User rating vs size graph we can see that size has to be less than 5.76031e+08 (approximately) ")
print("\n")

plt.boxplot(data['Size'],showfliers=False,patch_artist=True)
plt.title('size with all data')
plt.show()

print("from boxplot for size in all data we can see that most of the data(25 % to 75 %) lies in 5.07433e+07 to 2.27002e+08")
print("\n")


plt.boxplot(db['Size'],showfliers=False,patch_artist=True)
plt.title('size with rating between 4-5')
plt.show()

print("from boxplot for size in data with rating 4-5 the reasonable size is can be between 6.22099e+07 to 2.41186e+08")
print("\n")

#distplot for size vs count

plt.figure(figsize = (18, 10),dpi=80)
sns.distplot(db['Size'])
plt.ylabel('Count',fontsize=20)
plt.xlabel('Size',fontsize=20)
plt.title('Distplot for size in data with rating 4-5')
plt.show()

#for update time

plt.scatter(x=data['Average User Rating'],y=data['Size'],marker='^')
plt.xlabel('Average User Rating')
plt.ylabel('update_time')
plt.title('Average User Rating  vs  update_time for all')
plt.show()

print("from above average user rating vs update_time graph  for all data we can see that update date has to be less than 9.37373e+08(approximately)")
print("\n")

plt.boxplot(data['update_time'],showfliers=False,patch_artist=True)
plt.title('update_time with all data')
plt.show()

print("from above average user rating vs update time graph for all data update time is reasonable in between 17.4609 to 63.2688")
print("\n")

plt.boxplot(db['update_time'],showfliers=False,patch_artist=True)
plt.title('update_time with rating between 4-5')
plt.show()

print("from above average user rating vs update time graph for data required rating the update time is reasonable in between 17.3977 to 58.8645")
print("\n")


plt.figure(figsize = (18, 10),dpi=80)
sns.distplot(data['update_time'])
plt.ylabel('Count',fontsize=20)
plt.xlabel('update_time',fontsize=20)
plt.title('Distplot of update time for all data')
plt.show()


plt.figure(figsize = (18, 10),dpi=80)
sns.distplot(db['update_time'])
plt.ylabel('Count',fontsize=20)
plt.xlabel('Size',fontsize=20)
plt.title('Distplot of update time for data with rating 4-5')
plt.show()
print("from above update_time graphs we can see our results are fine")