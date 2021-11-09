#from tabula import wrapper
import tabula.io
import pandas as pd

dfs = tabula.io.read_pdf('20190926_054000_pos_9411.pdf',pages = 'all')
tabula.io.convert_into("20190926_054000_pos_9411.pdf", "output.csv", output_format="csv", pages='all')
print(dfs)