/*#    Copyright (C) 2020 Daniel Gamermann <gamermann@gmail.com>
#
#    This file is part of Surpriser
#
#    Surpriser is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Surpriser is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Surpriser.  If not, see <http://www.gnu.org/licenses/>.
#
#    
#    Please, cite us in your reasearch!
#*/
void seed(void); // seed the random number generator
double drand(void); // random number from numerical recepies
void stats(double *nums, int N, double *xb, double *sig, double *t, int assy); // evaluate descriptive stats
double zeta(double gamma, int n); // Rieman zeta function
double zeta_xmin(double gamma, int n, int x0); // Rieman zeta function with xmin
double dzetadx(double gamma, int n); // derivative of the zeta function
double dzetadx_xmin(double gamma, int n, int x0); // derivative of the zeta function with xmin
int irand_SF(double gamma, int iMAX); // SF integer random number
int irand_SF_xmin(double gamma, int x0, int iMAX); // SF integer random number with xmin
double drand_SF(double gamma); // SF double random number
double drand_SF_xmin(double gamma, double x0); // SF double random number with xmin
double lnL(int *nums, int N, double gamma, int xmin, int nsum); // log LKHD for discrete SF distribution
double lnL_cont(double *nums, int N, double gamma, double xmin); // log LKHD for continous SF distribution
double gamma_MLE(int *nums, int N, double x0, double eps, int nsum); // Estimates gamma by MLE method for discrete distribution
double gamma_MLE_cont(double *nums, int N, double x0); //Estimates gamma by MLE method for continous distribution
double gamma_MLE_xmin(int *nums, int N, int xmin, double x0, double eps, int nsum); // Estimates gamma by MLE method for discrete distribution
void maxLKHD_gamma_cont(double *nums, int N, double *gamma, double *x0, double delt); // 
void uncertainty_cont(double *nums, int N, double gamma, double x0, double eps, double *gap, double *gam); // uncertainty for maxlkhd estimation continous
void uncertainty_int(int *nums, int N, double gamma, int x0, double eps, double *gap, double *gam, int nsum); // uncertainty for maxlkhd estimation discrete

