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
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "randoms.h"
#include <time.h>

#define IA 16807
#define IM 2147483647
#define AM (1.0/IM)
#define IQ 127773
#define IR 2836
#define NTAB 32
#define NDIV (1+(IM-1)/NTAB)
#define EPS 1.2e-14
#define RNMX (1.0-EPS)



long *idum = NULL;


void seed(void){
    idum = malloc(sizeof(long));
    *idum = -time(NULL);
}



double drand(void) {
    int j;
    long k;
    static long iy=0;
    static long iv[NTAB];
    double temp;
    if (!idum) {
        seed();
    }
    if (*idum <= 0 || !iy) {
        if (-(*idum) < 1) *idum=1;
        else *idum = -(*idum);
        for (j=NTAB+7;j>=0;j--) { 
            k=(*idum)/IQ;
            *idum=IA*(*idum-k*IQ)-IR*k;
            if (*idum < 0) *idum += IM;
            if (j < NTAB) iv[j] = *idum;
        }
        iy=iv[0];
    }
    k=(*idum)/IQ; 
    *idum=IA*(*idum-k*IQ)-IR*k; 
    if (*idum < 0) *idum += IM; 
    j=iy/NDIV; 
    iy=iv[j]; 
    iv[j] = *idum; 
    if ((temp=AM*iy) > RNMX) return RNMX; 
    else return temp;
}




void stats(double *nums, int N, double *xb, double *sig, double *t, int assy) {
    int i;
    double sum=0., sum2=0., sum3=0., xi;
    
    if (assy) {
        for (i=0; i<N; i++) {
            xi = *(nums+i);
            sum += xi;
            sum2 += xi*xi;
            sum3 += xi*xi*xi;
        }        
        *xb = sum*1./N;
        *sig = sqrt((sum2 - N* *xb * *xb)/(N-1));
        *t = (sum3/N - 3.* *xb * *sig * *sig - *xb * *xb * *xb)/(*sig * *sig * *sig);
    } else {    
        for (i=0; i<N; i++) {
            xi = *(nums+i);
            sum += xi;
            sum2 += xi*xi;
        }
        *xb = sum*1./N;
        *sig = sqrt((sum2 - N* *xb * *xb)/(N-1));
    }
}




double zeta(double gamma, int n) {
    double b, c, d, s, ak, bla, res;
    int k;
    d = pow((3. + sqrt(8.)), n);
    d = (d + 1./d)/2.;
    b = -1.;
    c = -d;
    s = 0.;
    for (k=0; k<n; k++) {
        ak = pow(1./(k+1.), gamma);
        c = b - c;
        s = s + c*ak;
        b = (k+n)*(k-n)*b/((k+.5)*(k+1.));
    }
    res = s/d;
    bla = (1.- pow(2, (1-gamma)));
    return res/bla;
}


double zeta_xmin(double gamma, int n, int x0) {
    double res;
    int k;
    res = zeta(gamma, n);
    for (k=1; k<x0; k++) {
        res = res - pow(1.*k, -gamma);
    }
    return res;
}


double dzetadx(double gamma, int n) {
    double b, c, d, s, ak, bla, res, pp;
    int k;
    d = pow((3. + sqrt(8.)), n);
    d = (d + 1./d)/2.;
    b = -1.;
    c = -d;
    s = 0.;
    for (k=0; k<n; k++) {
        ak = pow(1./(k+1.), gamma)*log(k+1.);
        c = b - c;
        s = s + c*ak;
        b = (k+n)*(k-n)*b/((k+.5)*(k+1.));
    }
    pp = pow(2., 1-gamma);
    res = s/d + log(2.)*zeta(gamma, n)*pp;
    bla = (1.- pp);
    return -res/bla;
}


double dzetadx_xmin(double gamma, int n, int x0) {
    double res;
    int k;
    res = dzetadx(gamma, n);
    for (k=1; k<x0; k++) {
        res += pow(1.*k, -gamma) * log(1.*k);
    }
    return res;
}






int irand_SF(double gamma, int iMAX) {
    double FF;
    double alp;
    double sum, num;
    int i;
    
    alp = zeta(gamma, 20);
    FF = drand()*alp;
    sum = 0.;
    i = 0;
    while (sum<FF) {
        i++;
        num = pow(1.*i, -gamma);
        sum += num;
        if (i>iMAX) {
            printf("Warning: generation of irand_SF broke iteration at %d\n", iMAX);
            i += (int) 1000*drand();
            break;
        }
    }
    return i;
}


int irand_SF_xmin(double gamma, int x0, int iMAX) {
    double FF;
    double alp;
    double sum, num;
    int i;
    
    alp = zeta_xmin(gamma, 20, x0);
    FF = drand()*alp;
    sum = 0.;
    i = x0-1;
    while (sum<FF) {
        i++;
        num = pow(1.*i, -gamma);
        sum += num;
        if (i>iMAX) {
            //printf("Warning: generation of irand_SF broke iteration at %d\n", iMAX);
            i += (int) x0*1000*drand();
            break;
        }
    }
    return i;
}






double drand_SF(double gamma) {
    double FF;
    
    FF = drand();
    return pow(FF, 1./(1.-gamma));
}


double drand_SF_xmin(double gamma, double x0) {
    double FF;
    
    FF = drand();
    return x0*(pow(1.-FF, 1./(1.-gamma)));
}



double lnL(int *nums, int N, double gamma, int xmin, int nsum) {
    double kk, res;
    int i, NN, num;
    kk = 0.;
    NN = N;
    for (i=0; i<N; i++) {
        num = *(nums+i);
        if (num>=xmin) {
            kk += log(1.*num);
        } else {
            NN--;
        }
    }
    res = -NN*log(zeta_xmin(gamma, nsum, xmin))-gamma*kk;
    return res;
}



double lnL_cont(double *nums, int N, double gamma, double xmin) {
    double kk, res, num;
    int i, NN;
    kk = 0.;
    NN = N;
    for (i=0; i<N; i++) {
        num = *(nums+i);
        if (num>=xmin) {
            kk += log(num);
        } else {
            NN--;
        }
    }
    res = NN*log( (gamma-1.) ) + NN*(gamma-1.)*log(xmin) - gamma*kk;
    return res;
}





double gamma_MLE(int *nums, int N, double x0, double eps, int nsum) {
    double diff, kk, der, ddd, xx, num, ndiff;
    double lamb=.1;
    int i;
    
    kk = 0.;
    for (i=0; i<N; i++) {
        num = 1.* *(nums+i);
        kk += log(num);
    }
    xx = x0;
    diff = -log(zeta(xx, nsum))-xx*kk/N;
    der = -dzetadx(xx, nsum)/zeta(xx, nsum)-kk/N;
    while (fabs(lamb*der)>eps) {
        ddd = xx+lamb*der;
        ndiff = -log(zeta(ddd, nsum))-ddd*kk/N;
        if (ndiff>diff) {
            diff = ndiff;
            der = -dzetadx(ddd, nsum)/zeta(ddd, nsum)-kk/N;
            xx = ddd;
            lamb *= 1.05;
        } else {
            lamb *= .8;
        }
    }
    return xx;
}


double gamma_MLE_xmin(int *nums, int N, int xmin, double x0, double eps, int nsum) {
    double diff, kk, der, ddd, xx, ndiff;
    double lamb=.1;
    int i, NN, num;
    
    kk = 0.;
    NN = N;
    for (i=0; i<N; i++) {
        num = *(nums+i);
        if (num>=xmin) {
            kk += log(1.*num);
        } else {
            NN--;
        }
    }
    xx = x0;
    diff = -log(zeta_xmin(xx, nsum, xmin))-xx*kk/NN;
    der = -dzetadx_xmin(xx, nsum, xmin)/zeta_xmin(xx, nsum, xmin)-kk/NN;
    while (fabs(lamb*der)>eps) {
        ddd = xx+lamb*der;
        ndiff = -log(zeta_xmin(ddd, nsum, xmin))-ddd*kk/NN;
        if (ndiff>diff) {
            diff = ndiff;
            der = -dzetadx_xmin(ddd, nsum, xmin)/zeta_xmin(ddd, nsum, xmin)-kk/NN;
            xx = ddd;
            lamb *= 1.05;
        } else {
            lamb *= .8;
        }
    }
    return xx;
}




double gamma_MLE_cont(double *nums, int N, double x0) {
    int i, NN;
    double kk, num, res;
    kk = 0.;
    NN = N;
    for (i=0; i<N; i++) {
        num = *(nums+i);
        if (num>=x0) {
            kk += log(num/x0);
        } else {
            NN--;
        }
    }
    res = 1. + NN*1./(kk);
    return res;
}



void uncertainty_cont(double *nums, int N, double gamma, double x0, double eps, double *gap, double *gam) {
    double point, nga=gamma;
    double lamb=.7;    
    double nlhood;
    
    point = lnL_cont(nums, N, gamma, x0)-.5;
    nga += lamb;
    nlhood = lnL_cont(nums, N, nga, x0);
    // positive uncrt
    while ((fabs(nlhood-point)>eps)&(lamb>1.e-15)) {
        if (nlhood>point) {
            lamb *= 1.2;
        } else {
            nga -= lamb;
            lamb *= .7;
        }
        nga += lamb;
        nlhood = lnL_cont(nums, N, nga, x0);
    }
    *gap = nga-gamma;
    // negative uncert
    nga = gamma;
    point = lnL_cont(nums, N, gamma, x0)-.5;
    nga -= lamb;
    nlhood = lnL_cont(nums, N, nga, x0);
    while ((fabs(nlhood-point)>eps)&(lamb>1.e-15)) {
        if (nlhood>point) {
            lamb *= 1.2;
        } else {
            nga += lamb;
            lamb *= .7;
        }
        nga -= lamb;
        nlhood = lnL_cont(nums, N, nga, x0);
    }
    *gam = gamma-nga;
}



void uncertainty_int(int *nums, int N, double gamma, int x0, double eps, double *gap, double *gam, int nsum) {
    double point, nga=gamma;
    double lamb=.7;    
    double nlhood;
    
    point = lnL(nums, N, gamma, x0, nsum)-.5;
    nga += lamb;
    nlhood = lnL(nums, N, nga, x0, nsum);
    // positive uncrt
    while ((fabs(nlhood-point)>eps)&(lamb>1.e-15)) {
        if (nlhood>point) {
            lamb *= 1.2;
        } else {
            nga -= lamb;
            lamb *= .7;
        }
        nga += lamb;
        nlhood = lnL(nums, N, nga, x0, nsum);
    }
    *gap = nga-gamma;
    // negative uncert
    nga = gamma;
    point = lnL(nums, N, gamma, x0, nsum)-.5;
    nga -= lamb;
    nlhood = lnL(nums, N, nga, x0, nsum);
    while ((fabs(nlhood-point)>eps)&(lamb>1.e-15)) {
        if (nlhood>point) {
            lamb *= 1.2;
        } else {
            nga += lamb;
            lamb *= .7;
        }
        nga -= lamb;
        nlhood = lnL(nums, N, nga, x0, nsum);
    }
    *gam = gamma-nga;
}





void maxLKHD_gamma_cont(double *nums, int N, double *gamma, double *x0, double delt) {
    double ln1, ln2, der;
    double lamb=.01, xg, xx;
    double eps=1.e-8;
    xg = *gamma;
    xx = *x0;
    ln1 = lnL_cont(nums, N, xg, xx);
    der = (lnL_cont(nums, N, gamma_MLE_cont(nums, N, xx+delt), xx+delt)-ln1)/delt;
    while (fabs(lamb*der)>eps) {
        xx += lamb*der;
        xg = gamma_MLE_cont(nums, N, xx);
        ln2 = lnL_cont(nums, N, xg, xx);
        if (ln2>ln1) {
            der = (lnL_cont(nums, N, gamma_MLE_cont(nums, N, xx+delt), xx+delt)-ln2)/delt;
            ln1 = ln2;
            lamb *= 1.2;
        } else {
            xx -= lamb*der;
            lamb *= .8;
        }
    }
    *gamma = xg;
    *x0 = xx;
}
























