series tot_num_amusementpark, xtot_num_banks, xtot_num_correctional, xtot_num_electriccompany, xtot_num_gascompany, xtot_num_library, xtot_num_pipeline, xtot_num_postoffice, xtot_num_railroad, xtot_num_recreation, xtot_num_religious, xtot_num_restaurant, xtot_num_theatres, xtot_num_warehouse are constants and have been removed
Oneway (individual) effect Between Model

Call:
plm(formula = Y_ ~ X_, data = pdata, model = "between")

Unbalanced Panel: n=10, T=11-22, N=175

Residuals :
   Min. 1st Qu.  Median 3rd Qu.    Max. 
      0       0       0       0       0 

Coefficients :
                             Estimate Std. Error t-value Pr(>|t|)
(Intercept)                 15.292578         NA      NA       NA
X_tot_num_buildings          0.052016         NA      NA       NA
X_tot_num_cardealership      1.779507         NA      NA       NA
X_tot_num_condos             0.382181         NA      NA       NA
X_tot_num_emergencystation  28.922473         NA      NA       NA
X_tot_num_industrial        -2.594894         NA      NA       NA
X_tot_num_medical          -13.341864         NA      NA       NA
X_tot_num_offices            7.035083         NA      NA       NA
X_tot_num_residential       -0.062000         NA      NA       NA
X_tot_num_shopping          -6.138202         NA      NA       NA

Total Sum of Squares:    1440.4
Residual Sum of Squares: 0
R-Squared      :  1 
      Adj. R-Squared :  0 
F-statistic: NaN on 9 and 0 DF, p-value: NA
