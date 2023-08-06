# README

### Introduction
It only contains one function which accept a dataframe 
with missing values and replace the NaNs with mean value 
of the value around these NaNs. The imputation is linear, e.g.
[nan,nan,5,8] => [-1,2,5,8], [3,nan,nan,9] => [3,5,7,9],
[1,5,nan,nan] => [1,5,9,13]

Currently only DataFrame is accepted, I may consider to support 
any arrry-like object in the future.


### Tips
1. This is actually a package for practice packaging in python. So there may be problems
with the algorithm and the algorithm may not be efficient.
2. There should be at least 2 non-nan value in the input, otherwise the original 
DataFrame will be returned.
3. Only float point number is tested, so be careful if use this function with other
value types