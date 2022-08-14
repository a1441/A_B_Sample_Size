#!/usr/bin/env python
# coding: utf-8

# # Libraries & Dependencies

# In[1]:


import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.stats.api as sms
from math import ceil
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from math import ceil


# # Problem statement

# https://towardsdatascience.com/ab-testing-with-python-e5964dd66143 - by Renato Fillinich

# ![image.png](attachment:image.png)

# # Hypothesis

# ![image.png](attachment:image.png)

# Our alpha is effectively 0.05
# 
# The α value is a threshold we set, by which we say “if the probability of observing a result as extreme or more (p-value) is lower than α, then we reject the Null hypothesis”. Since our α=0.05 (indicating 5% probability), our confidence interval (1 — α) is 95%.

# # Calculating sample size

# ![image.png](attachment:image.png)

# Power analysis is an important aspect of experimental design. 
# 
# It allows us to determine the sample size required to detect an effect of a given size with a given degree of confidence. 
# 
# Conversely, it allows us to determine the probability of detecting an effect of a given size with a given level of confidence, under sample size constraints. 
# 
# If the probability is unacceptably low, we would be wise to alter or abandon the experiment.
# 
# https://www.statmethods.net/stats/power.html

# In[2]:


base_line_rate = 0.13

expected_uplift = 0.02


# In[3]:


#Calculate Effect size for a test comparing two proportions for use in power function

effect_size = sms.proportion_effectsize(base_line_rate, base_line_rate+expected_uplift)  
effect_size


# In[5]:


#Statistical Power calculations for z-test for two independent samples. Currently only uses pooled variance


required_n = sms.NormalIndPower().solve_power(
    effect_size, 
    power=0.8, 
    alpha=0.05, 
    ratio=1
    ) 
required_n


# Having set the power parameter to 0.8 in practice means that if there exists an actual difference in conversion rate between our designs, assuming the difference is the one we estimated (13% vs. 15%), we have about 80% chance to detect it as statistically significant in our test with the sample size we calculated.

# In[6]:


required_n = ceil(required_n) 


# In[7]:


required_n


# # Voltron

# In[9]:


class A_B_sample_size:
    
    """Class to estimate needed sample size to detect significance during A/B testing"""
    
    def __init__(
                  self 
                 ,baseline 
                 ,uplift 
                 ,power = 0.8
                 ,alpha = 0.05
                 ,ratio = 1
                ):
        
        import numpy as np
        import scipy.stats as stats
        import statsmodels.stats.api as sms
        from math import ceil
        
        """Initializing the function with baseline rate & expected uplift as arguments"""
        # arguments in the class 
        self.base_line_rate = baseline
        self.expected_uplift = uplift
        self.power= power 
        self.alpha= alpha
        self.ratio= ratio
        # proportion effect size
        self.effect_size = sms.proportion_effectsize(self.base_line_rate, self.base_line_rate+self.expected_uplift)  
        #required sample size
        self.required_n = sms.NormalIndPower().solve_power(
        self.effect_size, 
        power=self.power, 
        alpha=self.alpha, 
        ratio=self.ratio
        )  
        #rounding the sample size
        self.sample_size = ceil(self.required_n)
    


# In[40]:


A_B_sample_size(0.012, 0.003).sample_size


# In[41]:


A_B_sample_size(0.012, 0.005).sample_size


# In[42]:


A_B_sample_size(0.012, 0.001).sample_size


# In[44]:


[A_B_sample_size(0.012, up_lift).sample_size for up_lift in [0.0001, 0.0005, 0.001, 0.0015, 0.002, 0.003, 0.004]]


# In[37]:


sample_df = pd.DataFrame([[0.0001, 0.0005, 0.001, 0.0015, 0.002, 0.003, 0.004],
              [A_B_sample_size(0.012, up_lift).sample_size for up_lift in [0.0001, 0.0005, 0.001, 0.0015, 0.002, 0.003, 0.004]]]).T

sample_df.columns = ['uplift','sample']

import plotly.express as px

fig = px.line(sample_df, x="uplift", y="sample", title='Relationship between uplift & sample_size')
fig.show()


# In[46]:


sample_df = pd.DataFrame([[0.0001, 0.0005, 0.001, 0.0015, 0.002, 0.003, 0.004],
              [A_B_sample_size(baseline, 0.001).sample_size for baseline in [0.01, 0.011, 0.012, 0.015, 0.02, 0.03]]]).T

sample_df.columns = ['baseline','sample']

import plotly.express as px

fig = px.line(sample_df, x="baseline", y="sample", title='Relationship between uplift & sample_size')
fig.show()


# In[ ]:




