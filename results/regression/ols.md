
Call:
lm(formula = Y_ ~ X_, data = mydata)

Residuals:
    Min      1Q  Median      3Q     Max 
-32.053  -5.211  -0.867   4.788  89.923 

Coefficients:
                            Estimate Std. Error t value Pr(>|t|)    
(Intercept)                 15.29258    5.27341   2.900 0.004241 ** 
X_tot_num_buildings          0.05202    0.01523   3.416 0.000801 ***
X_tot_num_cardealership      1.77951    1.12338   1.584 0.115095    
X_tot_num_condos             0.38218    0.07507   5.091 9.62e-07 ***
X_tot_num_emergencystation  28.92247    6.75559   4.281 3.14e-05 ***
X_tot_num_industrial        -2.59489    1.72418  -1.505 0.134236    
X_tot_num_medical          -13.34186    2.18807  -6.098 7.39e-09 ***
X_tot_num_offices            7.03508    5.30218   1.327 0.186399    
X_tot_num_residential       -0.06200    0.01537  -4.033 8.41e-05 ***
X_tot_num_shopping          -6.13820    2.83873  -2.162 0.032035 *  
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 12.15 on 165 degrees of freedom
Multiple R-squared:  0.5059,	Adjusted R-squared:  0.4789 
F-statistic: 18.77 on 9 and 165 DF,  p-value: < 2.2e-16

