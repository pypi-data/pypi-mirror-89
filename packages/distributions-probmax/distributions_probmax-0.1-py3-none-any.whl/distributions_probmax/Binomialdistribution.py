# TODO: import necessary libraries
import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Binomial(Distribution):
    
    def __init__(self,prob=0.5,n=25):
        
        self.p=prob
        self.n=n
        self.calculate_mean()
        self.calculate_stdev()
        
    def calculate_mean(self):
        self.mean = self.p*self.n
        return self.mean

    def calculate_stdev(self):
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))
        return self.stdev
    
    def replace_stats_with_data(self):
        self.n = len(self.data)
        self.p = sum(self.data)/self.n
        self.calculate_mean()
        self.calculate_stdev()
        return self.p , self.n
        
    def pdf(self, k):
        binomial_coefficient = math.factorial(self.n)/(math.factorial(k)*math.factorial(self.n-k))
        return binomial_coefficient*((self.p**k)*(1-self.p)**(self.n-k))                      

    def plot_pdf(self,plot_limit):
        x_values = list(range(1, plot_limit))
        y_values = [pdf(k) for k in x_values]
        plt.plot(x_values,y_values)
        plt.title('probability Density Function')
        plt.xlabel('Success Events')
        plt.ylabel('Probability')
        plt.show()
        return [x_values,y_values]
 
    def __add__(self,other):
                               
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise
        
        result = Binomial()
        result.p = self.p
        result.n = self.n + other.n
        result.calculate_mean()
        result.calculate_stdev()
        return result
       
    def __repr__(self):
        return f'mean {self.mean}, standard deviation {self.stdev}, p {self.p}, n {self.n}'                        
