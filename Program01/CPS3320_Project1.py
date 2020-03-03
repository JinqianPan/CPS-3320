# import packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

# Connect the Google Drive and link the data path
# loading the data
from google.colab import drive
drive.mount('/content/drive/')
data = pd.read_csv('/content/drive/My Drive/Colab Notebooks/CPS3320_Project_1/listings.csv')
# get informations from data
data.info()
data.head()
data.describe()

### Data Cleaning
# Choose colunms which is interested
dataSelection = data.loc[:,['price', 
                            'host_response_time', 
                            'host_response_rate', 
                            'host_acceptance_rate', 
                            'host_is_superhost', 
                            'host_neighbourhood', 
                            'host_listings_count',
                            'host_total_listings_count', 
                            'host_has_profile_pic', 
                            'host_identity_verified', 
                            'property_type', 
                            'room_type', 
                            'accommodates', 
                            'bathrooms', 
                            'bedrooms', 
                            'beds', 
                            'bed_type', 
                            'review_scores_rating', 
                            'review_scores_accuracy', 
                            'reviews_per_month']]
dataSelection.head()
#  get how many NAs in these columns
dataSelection.isnull().sum()
# Because we have 3585 variables in this data, host_response_time, host_response_rate, host_acceptance_rate, host_neighbourhood, review_scores_rate, review_scores_accuracy, reviews_per_month cannot be used in the model.
dataSelection = data.loc[:,['price',  
                            'host_is_superhost', 
                            'host_listings_count',
                            'host_total_listings_count', 
                            'host_has_profile_pic', 
                            'host_identity_verified', 
                            'property_type', 
                            'room_type', 
                            'accommodates', 
                            'bathrooms', 
                            'bedrooms', 
                            'beds', 
                            'bed_type']]
dataSelection.head()
# for colunms which have less NAs, dropped it
dataSelection = dataSelection.dropna(axis=0,how='any')
dataSelection.info()
# in the information of data, 'price''s data type is object; so that we need to change it to float64
dataSelection['price'] = dataSelection['price'].str.lstrip("$")
dataSelection['price'] = dataSelection['price'].str.replace(",", "")
dataSelection['price'] = dataSelection['price'].astype('float')
## Label Encoding
# for those column with string data type, we need to change them as number
from sklearn import preprocessing

superhost = preprocessing.LabelEncoder()
superhost.fit(dataSelection['host_is_superhost'])

profile = preprocessing.LabelEncoder()
profile.fit(dataSelection['host_has_profile_pic'])

verified = preprocessing.LabelEncoder()
verified.fit(dataSelection['host_identity_verified'])

propertytype = preprocessing.LabelEncoder()
propertytype.fit(dataSelection['property_type'])

roomtype = preprocessing.LabelEncoder()
roomtype.fit(dataSelection['room_type'])

bedtype = preprocessing.LabelEncoder()
bedtype.fit(dataSelection['bed_type'])
# And replace it in our data
dataSelection['host_is_superhost'] = superhost.transform(dataSelection['host_is_superhost'])
dataSelection['host_has_profile_pic'] = profile.transform(dataSelection['host_has_profile_pic'])
dataSelection['host_identity_verified'] = verified.transform(dataSelection['host_identity_verified'])
dataSelection['property_type'] = propertytype.transform(dataSelection['property_type'])
dataSelection['room_type'] = roomtype.transform(dataSelection['room_type'])
dataSelection['bed_type'] = bedtype.transform(dataSelection['bed_type'])

dataSelection.head()

dataSelection.info()

### Data Visulization

plt.figure(figsize=(16,8))
plt.plot(dataSelection['price'])
plt.show()

dataSelection.plot.scatter('bedrooms','price', figsize=(10,10))
plt.show()

dataSelection.plot.scatter('beds','bedrooms', figsize=(10,10))
plt.show()


# Stepwise Regression
import statsmodels.api as sm
# define the stepwise regression
def stepwise_selection(X, y, 
                       initial_list=[], 
                       threshold_in=0.01, 
                       threshold_out = 0.05, 
                       verbose=True):
    """ Perform a forward-backward feature selection 
    based on p-value from statsmodels.api.OLS
    Arguments:
        X - pandas.DataFrame with candidate features
        y - list-like with the target
        initial_list - list of features to start with (column names of X)
        threshold_in - include a feature if its p-value < threshold_in
        threshold_out - exclude a feature if its p-value > threshold_out
        verbose - whether to print the sequence of inclusions and exclusions
    Returns: list of selected features 
    """
    included = list(initial_list)
    while True:
        changed=False
        # forward step
        excluded = list(set(X.columns)-set(included))
        new_pval = pd.Series(index=excluded)
        for new_column in excluded:
            model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included+[new_column]]))).fit()
            new_pval[new_column] = model.pvalues[new_column]
        best_pval = new_pval.min()
        if best_pval < threshold_in:
            best_feature = new_pval.argmin()
            included.append(best_feature)
            changed=True
            if verbose:
                print('Add  {:30} with p-value {:.6}'.format(best_feature, best_pval))

        # backward step
        model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included]))).fit()
        # use all coefs except intercept
        pvalues = model.pvalues.iloc[1:]
        worst_pval = pvalues.max() # null if pvalues is empty
        if worst_pval > threshold_out:
            changed=True
            worst_feature = pvalues.argmax()
            included.remove(worst_feature)
            if verbose:
                print('Drop {:30} with p-value {:.6}'.format(worst_feature, worst_pval))
        if not changed:
            break
    return included
# cut the data to which we needed
x = pd.DataFrame(dataSelection)
y = x.iloc[:, 0]
x = x.iloc[:, 1:12]
# And get the result
result = stepwise_selection(x, y)
print('resulting features:')
print(result)
# After we get the variable which we needed, making the model
x = pd.DataFrame(dataSelection)
y = x.iloc[:, 0]
x = x.iloc[:, 5:11]

x = sm.add_constant(x)
est = sm.OLS(y,x).fit()
est.summary()