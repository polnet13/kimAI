from pyhwpx import Hwp


import seaborn as sns

df = sns.load_dataset('tips')

hwp = Hwp()

hwp.table_from_data(df)