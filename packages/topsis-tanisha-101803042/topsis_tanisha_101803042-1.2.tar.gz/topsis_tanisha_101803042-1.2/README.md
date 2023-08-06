# TOPSIS
Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) is a multi-criteria decision making method. 
The method is based on finding an ideal and an anti-ideal solution and comparing the distance of each one of the alternatives to those.
TOPSIS chooses the alternative of shortest Euclidean distance from the ideal solution, and greatest distance from the negative-ideal solution.

## Package Usage
To install the package:  
**pip install topsis_tanisha_101803042**  
This is a package focusing on finding the topsis score and rank of a dataframe **(csv file)** with only numerical values.

## Python IDLE or any Editor   
> import topsis_tanisha_101803042.topsis  
> f = "input_csv_filepath"  
> w = "1,1,1,1"  
> im = "+,+,+,-"  
> r = "result_csv_filepath"  
> topsis_tanisha_101803042.topsis.rank(f,w,im,r)  
The final result can be seen in the result file given as r.  
