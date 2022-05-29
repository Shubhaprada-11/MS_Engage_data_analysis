import csv
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd

df= pd.read_csv('cars_engage_2022.csv')
toRemove= set()
naNumbersPerColumn = df.isnull().sum()
for i in naNumbersPerColumn.index:
    if(naNumbersPerColumn[i]>(0.7*1276)):
        toRemove.add(i)
for i in toRemove:
    df.drop(i, axis=1, inplace=True)
#print(len(df.columns))
#print(df.columns)
#print(df.head())
#for col in df.columns:
 #   print(col)
specials=["Rs. "," cc"," mm"," litres","km/litre"," kg"]
for k in range(0,5):
	df.replace(specials[k],'',regex=True,inplace=True).astype(float)
print(df.loc[:,"Ex-Showroom_Price"])
#with open('cars_engage_2022.csv', 'r') as datafile:
#    reader= csv.reader(datafile)




#with open('cars_engage_2022.csv', 'r') as datafile:
 #    reader= csv.reader(datafile)
  #   temp=[]
   #  row=[]
    # ncol=len(next(reader))
     #datafile.seek(0)
   #  specials=["Rs. "," cc"," mm"," litres","km/litre","kg"]
    # for i in reader:
     #	for j in range(0,ncol):
     #		for x in specials:
	#		i[j]=str.replace(i[j],x,'')
	#		csv.writer(i[j])

#     for i in reader:
#         row.append(i)
#         if i[1]!="Make":
#             temp.append(i[2])
#             temp=list(set(temp))
#     if '' in temp:
#         temp.remove('')
#     file=open('project/static/output.txt','w')
#     # print("there are",end=' ')
#     # print(len(temp),end=' ') 
#     # print("different models")
#     # print("models are")
#     # print(temp)
#     file.write("there are"+' ')
#     file.write(str(len(temp))) 
#     file.write("different models")
#     file.write("models are")
#     file.write(str(temp))
#     n=len(temp)
#     num=[0]*n
#     #print(num)
#     for i in row:
#         for k in range(0,len(temp)):
#             if i[1]==temp[k]:
#                 num[k]+=1
#     x,y=[],[]
#     #print("number of cars of each model:")
#     file.write("number of cars of each model:")
#     for j in range(0,len(temp)):
#         #print(temp[j],end=':')
#         #print(num[j])
#         file.write(temp[j]+":")
#         file.write(str(num[j]))
#         x.append(temp[j])
#         y.append(num[j])
#     plot1=plt.figure(1)
#     plt.bar(x, y, color = 'g', width = 0.52, label = "no of each")
#     plt.xlabel('Model')
#     plt.ylabel('Num')
#     plt.xticks(rotation='vertical')
#     plt.title('number of each diff model')
#     plt.legend(loc="lower left")
#     # plot2=plt.figure(2)
#     # plt.pie(num,labels=temp)
#     plot1.savefig('project/static/model1.jpg')
#     #plot2.savefig('project/static/model2.jpg')

# def unique(no):
#     with open('cars_engage_2022.csv', 'r') as datafile:
#         reader= csv.reader(datafile)
#         temp=[]
#         row=[]
#         for i in reader:
#             row.append(i)
#             if i[1]!="Make":
#                 temp.append(i[no])
#                 temp=list(set(temp))
#         if '' in temp:
#             temp.remove('')
#         file=open('project/static/output.txt','w')
#         file.write("there are ")
#         file.write(str(len(temp))) 
#         file.write(" different "+row[0][no]+'\n')
#         file.write("they are "+'\n')
#         file.write(str(temp))
#         n=len(temp)
#         num=[0]*n
#         for i in row:
#             for k in range(0,len(temp)):
#                 if i[no]==temp[k]:
#                     num[k]+=1
#         x,y=[],[]
#         file.write("number of cars of each model:")
#         for j in range(0,len(temp)):
#             file.write(temp[j]+":")
#             file.write(str(num[j]))
#             x.append(temp[j])
#             y.append(num[j])
#         plot1=plt.figure(1)
#         plt.bar(x, y, color = 'g', width = 0.52, label = "no of each")
#         plt.xlabel(row[0][no])
#         plt.ylabel('Num')
#         plt.xticks(rotation='vertical')
#         plt.title('number of each diff '+row[0][no])
#         plt.legend(loc="lower left")
#         plt.show()  
# with open('cars_engage_2022.csv', 'r') as datafile:
#     reader= csv.reader(datafile)
#     unique(1)
