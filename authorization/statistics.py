import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import os
import uuid
from django.conf import settings 


class DataPreprocessor:
    def __init__(self, data):
        self.data = data

    def mean(self):
        return self.data.mean()


    def max(self):
        return self.data.max()
    
    def dropNull(self):
        return self.data.dropna()
    
    def fillNull(self):
        return self.data.fillna(self.data.mean(),inplace=True)

    def describe(self):
        return self.data.describe()    

    def calculate_quantiles(self, column, quantiles):
        return self.data[column].quantile(q=quantiles)
    
    
    def linegraph(self):
        columns = list(self.data.columns)
        x = columns[0]
        y = columns[1]
        plt.plot(self.data[x], self.data[y])
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title('Line Graph')
        plt.grid(True)
        
        # Generate a unique filename
        filename = f'line_graph_{uuid.uuid4()}.png'
        
        # Save the plot as an image file in the static/img folder
        save_path = os.path.join(settings.BASE_DIR, 'static', 'img', filename)
        plt.savefig(save_path)
        plt.close()  # Close the plot to release memory
        
        return filename  # Return the filename
