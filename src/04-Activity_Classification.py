# -*- coding: utf-8 -*-
from autogluon.tabular import TabularDataset
from autogluon.tabular import TabularPredictor

import pandas as pd
df_train = pd.read_csv("train.csv")
df_test = pd.read_csv("test.csv")

# Group by 'tag_identification' and compute aggregate features
agg_features = df_train.groupby('tag_identification').agg({
    'x': ['mean', 'std', 'median', 'min', 'max'],
    'y': ['mean', 'std', 'median', 'min', 'max'],
    'z': ['mean', 'std', 'median', 'min', 'max']
}).reset_index()

# Rename columns for clarity
agg_features.columns = ['tag_identification',
                        'x_mean', 'x_std', 'x_median', 'x_min', 'x_max',
                        'y_mean', 'y_std', 'y_median', 'y_min', 'y_max',
                        'z_mean', 'z_std', 'z_median', 'z_min', 'z_max']

# Merge aggregate features back to the original dataframe
df_train = pd.merge(df_train, agg_features, on='tag_identification', how='left')
df_test = pd.merge(df_test, agg_features, on='tag_identification', how='left')

train_data = TabularDataset(df_train)
test_data = TabularDataset(df_test)

label_column = 'activity'

predictor = TabularPredictor(label=label_column).fit(train_data)

predictions = predictor.predict(test_data)

df = pd.DataFrame({'activity': predictions.values}, index=range(len(predictions)))

# Reset the index to make it a column
df = df.reset_index()

# Rename the columns
df.columns = ['id', 'activity']

# Save the DataFrame as a CSV file
df.to_csv('activities.csv', index=False)