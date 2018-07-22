import json
import pandas as pd
from pandas.io.json import json_normalize

#df = pd.read_csv('ImageNet_classIDs_indices.txt',delimiter=' ',names=['Id','pred_index','class'])
df = pd.read_csv('ImageNet_classIDs_indices.txt',delimiter=': ',names=['OutputNum','class'])

print(df.head())
car_ID = 'n02958343'

par_child = pd.read_csv('parent_child.txt',delimiter=' ',names=['parent','child'])

print(par_child.head())

car_df = par_child[par_child['parent']==car_ID]

print(car_df.head())

car_subtypes = car_df['child'].tolist()
#print(car_subtypes)

'''allwords_df = pd.read_csv('word_list.txt',delimiter='\t',names=['Id','class'])

print(allwords_df.head())


car_df = allwords_df[allwords_df['Id'].isin(car_subtypes)]
print(len(car_df))
print(car_df.head(20))'''

df = pd.read_table('fixed_imagenet_class_index.json',names=['Num','Id','Class'])
print(df.head())

car_df = df[df['Id'].isin(car_subtypes)]

print(car_df.head(10))

print(car_df['Num'].tolist())

exit(0)

car_IDs = [
'n03791235',
'n02704792',
'n02854630',
'n02958343',
'n03221643',
'n03389761',
'n03444034',
'n03445924',
'n03506880',
'n03790512',
'n04252225',
'n04490091']

car_IDs = [
'n04170037',
'n03919096',
'n04062807',
'n04566561',
'n02740533',
'n02970100',
'n03384352',
'n03684823',
'n03791235',
'n04065272',
'n04335435',
'n04464852',
'n04465501']

print('\n\n')

car_df = df[df['Id'].isin(car_IDs)]
print(len(car_df))
print(car_df.head(20))




#
