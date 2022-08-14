#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
    


# In[ ]:




