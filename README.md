MS-Apriori was an academic project that was a part of the CS 583 Data Mining and Text Mining course. It is an implementation of Apriori algorithm with multiple minimum supports. 
Additional constraints:

* Must have: items that should occur in the frequent itmsets generated at the end  
* Cannot be together: items that cannot occur together in a frequent itemset  
* Support difference constraint (SDC): max(sup(i)) - min(sup(i)) should be less than or equal to the SDC or phi given, where sup(i) is the actual support count of an item 'i' that belongs
to a frequent itemset. 

Instructions to run the program: 

1. Unzip the files 
2. Open the command prompt and navigate to the folder where the files were unzipped. (using 'cd' of course)
3. To run the ms_apriori.py file one needs to pass the path to the input file followed by the path to the parameters file(seperatd by a space) as command line arguments. 
Suppose the input and parameter files are stored in the 'Test' folder then the program can be run by: 
"python ms_apriori.py Test/input-data.txt Test/parameter-file.txt"

if the input and parameter files are in the same folder as the program is, then the program can be run by: 
"python ms_apriori.py input-data.txt parameter-file.txt"

In the above commands we have assumed the transactions data is stored in 'input-data.txt' and the parameters are stored in 'parameter-file.txt'. 

The program will automatically create an "output.txt" file when run successfully. This file will contain the required output in desired format. It will appear inside the same folder where the program was stored. The results will also be printed at the command prompt.
