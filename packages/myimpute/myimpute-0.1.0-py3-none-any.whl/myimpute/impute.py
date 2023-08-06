# Fill missing month specially chosen mean value
# parameter:
#    df - should be a large dataframe containing all data including CHLA, Temperature, Total P
# return: a new DataFrame with all values imputed, the input will not be changed
def linear_impute(df):
    length_row = len(df)
    length_col = len(df.columns)
    # reset column for convenient referencing
    index = df.index.values.tolist()
    # reset index for convenient manipulation
    df = df.reset_index(drop=True)
    for j in range(length_col):
        # index of first non-NaN value
        first_non_nan = df.iloc[:, j].first_valid_index()
        if first_non_nan == len(df) - 1 or first_non_nan is None:
            # the condition that the number of valid value is lesst than or equals to one
            continue
        # index of last non-NaN value
        last_non_nan = df.iloc[:, j].last_valid_index()
        if last_non_nan == 0 or last_non_nan is None or last_non_nan == first_non_nan:
            # the condition that the number of record in this year is less than or equal to one
            continue

        # interpolate missing data in middle
        df.iloc[first_non_nan:last_non_nan, j] = df.interpolate().iloc[first_non_nan:last_non_nan, j]

        init_forward = df.iloc[last_non_nan, j]
        diff_forward = df.iloc[last_non_nan, j] - df.iloc[last_non_nan - 1, j]
        init_backward = df.iloc[first_non_nan, j]
        diff_backward = df.iloc[first_non_nan, j] - df.iloc[first_non_nan + 1, j]

        # iteratively impute consecutive missing data start from May or end by October,
        # this part of imputation is actually calculate a arithmetic progression,
        #   i.e.  a0,a1,a2,a3,a4,a5, suppose a2,a3 is not NaN and others are NaN,
        #         then, a4 = a3 + (a3 - a2), a5 = a3 + 2(a3 - a2),
        #               a1 = a2 + (a2 - a3), a0 = a2 + 2(a2 - a3)
        for k in reversed(range(first_non_nan)):
            df.iloc[k, j] = init_backward + (first_non_nan - k) * diff_backward if init_backward + (
                    first_non_nan - k) * diff_backward > 0 else 0
        for k in range(last_non_nan + 1, length_row):
            df.iloc[k, j] = init_forward + (k - last_non_nan) * diff_forward if init_forward + (
                    k - last_non_nan) * diff_forward else 0

    # resume the index of the slice of the data so that it can be put into the original dataframe
    df = df.set_index([index])

    return df


if __name__ == '__main__':
    import pandas as pd
    import numpy as np

    a = pd.DataFrame({'A': [np.nan, np.nan, 5, 8, 4], 'B': [3, np.nan, np.nan, 10, 11], 'C': [3, 5, 9, np.nan, np.nan],
                      'D': [1, np.nan, 3, np.nan, 5], 'E': [np.nan, np.nan, np.nan, np.nan, np.nan],
                      'F': [np.nan, np.nan, np.nan, 3, np.nan], 'G': [1, np.nan, np.nan, np.nan, 5]})
    print(a)
    b = linear_impute(a)
    print(b)
