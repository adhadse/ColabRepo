# These may simply be a result of my misunderstanding, stumbling though non-optimal / non-pythonic solutions, bad coding, or lack of research, but here are some issues I encountered. 
# Workarounds are provided when / if I solved them.

# COULD NOT ITERATE OVER A LIST OF DATAFRAMES AND ADD A ROW TO EACH WITH `.append`
# For each dataframe I wanted to make a TOTAL combined entry for for an element using components a and b
# It seemed like this should be doable in a loop.
# To do one, I can do this:
'''
elem_meanlength = 1
elem_meaneff = 1
elem_sumTPM = 1
elem_sumNumReads = 1
total_df = total_df.append(
        {'Name':"Elem_total",'Length':elem_meanlength,'EffectiveLength':elem_meaneff,'TPM':elem_sumTPM,'NumReads':elem_sumNumReads}, 
        ignore_index=True) # based on http://pandas.pydata.org/pandas-docs/stable/merging.html#appending-rows-to-a-dataframe
#print(total_df) # ONLY FOR DEBUGGING
'''
# But seems to only update a copy of when try to set up for iterating. Doesn't alter
# original. Find/replace worked in loop (see BELOW) but used "inplace". 
# Find/replace that worked in loop:
#-----------------
# list_of_dataframes = [total_df, another_df, yet_another_df]
#for each_df in list_of_dataframes:
#   each_df.replace({'OLD_TEXT': 'NEW_TEXT'}, regex=True, inplace = True)
#   #print(each_df) # FOR DEBUGGING ONLY
#-----------------
# COULDN'T COME UP WITH SOLUTION IN A TIMELY MANNER AT FIRST BUT LOOKED MORE.
# By searching `pandas append a row to dataframe not a copy` finally found Jun's answer at 
# https://stackoverflow.com/questions/19365513/how-to-add-an-extra-row-to-a-pandas-dataframe/19368360#19368360
# & it looked amenable to looping through several dataframes. Tested:
'''
list_of_dataframes = [total_df, another_df, yet_another_df]
print(total_df) # ONLY FOR DEBUGGING    
elem_meanlength = 1
elem_meaneff = 1
elem_sumTPM = 1
elem_sumNumReads = 1
list_of_dataframes[0].loc[len(list_of_dataframes[0])]= ["Elem_total",elem_meanlength,elem_meaneff,elem_sumTPM,elem_sumNumReads]# based on Jun's answer at https://stackoverflow.com/questions/19365513/how-to-add-an-extra-row-to-a-pandas-dataframe/19368360#19368360
print(list_of_dataframes[0])
print(total_df) # ONLY FOR DEBUGGING
# THE WORKAROUND FOR THAT
# That solution (plus the find/replace) implemented
for indx, each_df in enumerate(list_of_dataframes):
    each_df.replace({'OLD_TEXT': 'NEW_TEXT'}, regex=True, inplace = True)
    #print(each_df) # FOR DEBUGGING
    #print(each_df[each_df.Name.str.contains("ID")]) # FOR DEBUGGING, shows matches if "IDa" "IDab", etc.
    elem_meanlength = each_df[each_df.Name.str.contains("ID")].mean(0).Length
    elem_meaneff = each_df[each_df.Name.str.contains("ID")].mean(0).EffectiveLength
    elem_sumTPM = each_df[each_df.Name.str.contains("ID")].sum(0).TPM
    elem_sumNumReads = each_df[each_df.Name.str.contains("ID")].sum(0).NumReads
    list_of_dataframes[indx].loc[len(list_of_dataframes[indx])]= ["Elem_total",elem_meanlength,elem_meaneff,elem_sumTPM,elem_sumNumReads]# based on Jun's answer at https://stackoverflow.com/questions/19365513/how-to-add-an-extra-row-to-a-pandas-dataframe/19368360

# BUT DON'T USE THIS FOR A REAL,REAL LOT OF DATAFRAMES OR A LOT OF LARGE ONES. SUPER SLOW. See https://stackoverflow.com/a/17496530/8508004 for recommended way that I don't know if it is amenablet to iterating over a list of DataFrames



# CANNOT USE `sample` as a column name if want to be able to call that column using attribute notation 
# because `pandas.DataFrame.sample` is a function on the DataFrame.
# Either change the column names using `df.rename(columns={'old_name':'new_name'}, inplace=True)`
# -or use standard notation like this (compare with example of `.str.contains(pattern)` in snippets file:
import pandas as pd
import numpy as np
df = pd.DataFrame({'A': 'foo bar one123 bar foo one324 foo 0'.split(),
                   'sample': 'one546 one765 twosde three twowef two234 onedfr three'.split(),
                   'C': np.arange(8), 'D': np.arange(8) * 2})
print (df)
pattern = '|'.join(['one', 'two'])
df = df[df['sample'].str.contains(pattern)]
df['sample'].str.contains(pattern)



# if working with column names that contain spaces, use bracket notation to select and 
# not attribute notation, unless you want to change column names first (see `df.rename(columns={'old':'new'})`)
val =df[df.col3.str.contains('text\dmoretext')].mean(0)['source values']