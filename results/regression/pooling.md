series tot_num_amusementpark, xtot_num_banks, xtot_num_correctional, xtot_num_electriccompany, xtot_num_gascompany, xtot_num_library, xtot_num_pipeline, xtot_num_postoffice, xtot_num_railroad, xtot_num_recreation, xtot_num_religious, xtot_num_restaurant, xtot_num_theatres, xtot_num_warehouse are constants and have been removed
Oneway (individual) effect Pooling Model

Call:
plm(formula = Y_ ~ X_, data = pdata, model = "pooling")

Unbalanced Panel: n=10, T=11-22, N=175

Residuals :
   Min. 1st Qu.  Median 3rd Qu.    Max. 
-32.100  -5.210  -0.867   4.790  89.900 

Coefficients :
                             Estimate Std. Error t-value  Pr(>|t|)    
(Intercept)                 15.292578   5.273413  2.8999 0.0042410 ** 
X_tot_num_buildings          0.052016   0.015229  3.4156 0.0008013 ***
X_tot_num_cardealership      1.779507   1.123383  1.5841 0.1150946    
X_tot_num_condos             0.382181   0.075066  5.0912 9.615e-07 ***
X_tot_num_emergencystation  28.922473   6.755586  4.2813 3.144e-05 ***
X_tot_num_industrial        -2.594894   1.724181 -1.5050 0.1342357    
X_tot_num_medical          -13.341864   2.188073 -6.0975 7.386e-09 ***
X_tot_num_offices            7.035083   5.302179  1.3268 0.1863986    
X_tot_num_residential       -0.062000   0.015374 -4.0327 8.410e-05 ***
X_tot_num_shopping          -6.138202   2.838728 -2.1623 0.0320348 *  
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Total Sum of Squares:    49293
Residual Sum of Squares: 24356
R-Squared      :  0.50588 
      Adj. R-Squared :  0.47698 
F-statistic: 18.7699 on 9 and 165 DF, p-value: < 2.22e-16
