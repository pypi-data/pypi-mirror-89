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
#include <Python.h>
#include <stdio.h>
#include <stddef.h>
#include <string.h>
#include <structmember.h>
#include "randoms.h"




// *******************************************
/*           Doc strings                    */
// *******************************************
//
// Module 
static char utils_docstring[] = "Functions for statistical analysis involving graphs.";
// Functions
static char Function_stats_docstring[] = "Evaluates the statisticals for a distribution\n\
                                          usage: [M, S] = stats(lista)      or\n\
                                                 [M, S, t] = stats(lista, assymetry=True)  \n\
                                          returns M, S and (optionally) t, the average, standard deviation and skewness of the numbers in lista.";
static char Function_drand_docstring[] = "Generates an homogeneous random number between 0 and 1\n\
                                         Usage: num = drand()";
static char Function_drand_SF_docstring[] = "Generates a random number with scale-free distribution (double)\n\
                                         Usage: num = drand_SF(gamma=2.3, x0=1.)\n\
                                         gamma is the parameter of the scale-free function (p(k)~k**(-gamma)) and \n\
                                         x0 is the minimum possible value (p(k<x0)=0).";
static char Function_irand_SF_docstring[] = "Generates a random number with scale-free distribution (integer)\n\
                                         Usage: num = irand_SF(gamma=2.3, x0=1, iMAX=4000000)\n\
                                         gamma is the parameter of the scale-free function (p(k)~k**(-gamma)) and \n\
                                         x0 is the minimum possible value (p(k<x0)=0). The argument iMAX is the maximum\n\
                                         number of terms summed when needed.";
static char Function_lnL_docstring[] = "Likelihood for discrete SF distribution\n\
                                         Usage: L = lnL( list, gamma=2.3, x0=1, nsum=20)\n\
                                         Evaluates the log likelihood for the list of numbers supposing a scale-free distribution\n\
                                         with power parameter gamma and minum value x0. The nsum is the number of terms in the zeta\n\
                                          function evaluation";
static char Function_lnL_cont_docstring[] = "Likelihood for continous SF distribution\n\
                                         Usage: L = lnL_cont( list, gamma=2.3, x0=1.)\n\
                                         Evaluates the log likelihood for the list of numbers supposing a scale-free distribution\n\
                                         with power parameter gamma and minum value x0.";
static char Function_zeta_docstring[] = "Rieman zeta function.\n\
                                         Usage: rz = zeta( gamma, xmin=1, N=20 )\n\
                                         Returns the value of the Riemann zeta function at point gamma. xmin is the minimum term\n\
                                         in the sum. N is the number of terms in the sum (not the one deffining zeta, but the one\n\
                                         in the implementation of the function that converges much faster.";
static char Function_dzetadx_docstring[] = "Derivative of Rieman zeta function.\n\
                                          Usage: num = dzetadx(gamma, xmin=1, N=20)\n\
                                          xmin is the natural number where the sum starts, N is the number of terms\n\
                                          that will be summed (note that each term is not x**(-gamma), but another sum for\n\
                                          which the result usually converts after summing 20 terms.";
static char Function_gamma_MLE_docstring[] = "Estimates gamma by MLE method for discrete distribution.\n\
                                          Usage: gamma = gamma_MLE( list, x0=1, uncert=0, gamma0=2.3, eps=1.e-8, nsum=20 )\n\
                                            or\n\
                                                 gamma, (up, down) = gamma_MLE( list, x0=1, uncert=1, gamma0=2.3, eps=1.e-8, nsum=20 )\n\
                                          Estimates by maximum likelihood the value for gamma supposing the numbers in the list have\n\
                                          a discrete scale-free distribution. x0 is the minimum value of the distribution, gamma0 the point\n\
                                          at which the algorithm starts searching, eps the precision, nsum the number of terms in the zeta\n\
                                          function evaluation, eps the precision . The optional argument uncert tells whether to return \n\
                                          the up and down uncertainties in the returned value.";
static char Function_gamma_MLE_cont_docstring[] = "Estimates gamma by MLE method for contious distribution\n\
                                          Usage: gamma = gamma_MLE_cont( list, x0=1., uncert=0, eps=1.e-8, delt=0.02 )\n\
                                            or\n\
                                                 gamma, (up, down) = gamma_MLE( list, x0=1., uncert=1, eps=1.e-8, delt=0.02 )\n\
                                            or\n\
                                                 gamma, xmin = gamma_MLE_cont( list, x0=0., uncert=0, eps=1.e-8, delt=0.02 )\n\
                                            or\n\
                                                 gamma, xmin, (up, down) = gamma_MLE( list, x0=0., uncert=1, eps=1.e-8, delt=0.02 )\n\
                                          Estimates by maximum likelihood the value for gamma supposing the numbers in the list have\n\
                                          a continous scale-free distribution. x0 is the minimum value of the distribution (if the\n\
                                          optional argument is 0. when the functions is called, it will also estimate it), \n\
                                          delt is a numerical parameter (dx) to evaluate derivatives and eps the precisio.\n\
                                          The optional argument uncert tells whether to return the up and down\n\
                                          uncertainties in the returned value.";


// *******************************************
/*             Module functions             */
// *******************************************
/* function header */
static PyObject *Function_stats(PyObject *self, PyObject *args, PyObject *kwds);
static PyObject *Function_drand(PyObject *self);
static PyObject *Function_drand_SF(PyObject *self, PyObject *args, PyObject *kwds);
static PyObject *Function_irand_SF(PyObject *self, PyObject *args, PyObject *kwds);
static PyObject *Function_lnL(PyObject *self, PyObject *args, PyObject *kwds);
static PyObject *Function_lnL_cont(PyObject *self, PyObject *args, PyObject *kwds);
static PyObject *Function_zeta(PyObject *self, PyObject *args, PyObject *kwds);
static PyObject *Function_dzetadx(PyObject *self, PyObject *args, PyObject *kwds);
static PyObject *Function_gamma_MLE(PyObject *self, PyObject *args, PyObject *kwds);
static PyObject *Function_gamma_MLE_cont(PyObject *self, PyObject *args, PyObject *kwds);
/* Functions that will be callable from python */
static PyMethodDef module_methods[] = {
    {"stats", (PyCFunction)Function_stats, METH_VARARGS | METH_KEYWORDS, Function_stats_docstring},
    {"drand", (PyCFunction)Function_drand, METH_NOARGS, Function_drand_docstring},
    {"drand_SF", (PyCFunction)Function_drand_SF, METH_VARARGS | METH_KEYWORDS, Function_drand_SF_docstring},
    {"irand_SF", (PyCFunction)Function_irand_SF, METH_VARARGS | METH_KEYWORDS, Function_irand_SF_docstring},
    {"lnL", (PyCFunction)Function_lnL, METH_VARARGS | METH_KEYWORDS, Function_lnL_docstring},
    {"lnL_cont", (PyCFunction)Function_lnL_cont, METH_VARARGS | METH_KEYWORDS, Function_lnL_cont_docstring},
    {"zeta", (PyCFunction)Function_zeta, METH_VARARGS | METH_KEYWORDS, Function_zeta_docstring},
    {"dzetadx", (PyCFunction)Function_dzetadx, METH_VARARGS | METH_KEYWORDS, Function_dzetadx_docstring},
    {"gamma_MLE", (PyCFunction)Function_gamma_MLE, METH_VARARGS | METH_KEYWORDS, Function_gamma_MLE_docstring},
    {"gamma_MLE_cont", (PyCFunction)Function_gamma_MLE_cont, METH_VARARGS | METH_KEYWORDS, Function_gamma_MLE_cont_docstring},
    {NULL, NULL, 0, NULL}
};


// *******************************************
/*           Initialization                 */
// *******************************************
static struct PyModuleDef randomsmodule = {
    PyModuleDef_HEAD_INIT,
    "randoms",
    utils_docstring,
    -1,
    module_methods
};



PyMODINIT_FUNC PyInit_randoms(void) {
    PyObject* mod;
    // Create the module
    mod = PyModule_Create(&randomsmodule);
    if (mod == NULL) {
       return NULL;
    }
    return mod;
}




// *******************************************
/*              Functions                   */
// *******************************************











static PyObject *Function_stats(PyObject *self, PyObject *args, PyObject *kwds) {
    int N;
    PyObject *Numbers;
    int i, assy=0;
    double *nums;
    double xb, sb, t;
    
    // Parse the input
    static char *kwlist[] = {"numbers", "assymetry", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|i", kwlist, &Numbers, &assy))
        return 0;

    N = (int) PyList_Size(Numbers);
    nums = PyMem_New(double, N);
    for (i=0;i<N;i++) {
        *(nums + i) = (double) PyFloat_AsDouble(PyList_GetItem(Numbers, i));
    }
        
    if (N==0) {
        printf("Warning: Calculating average of an empty list!\n");
    }
    if (N==1) {
        printf("Warning: Calculating standard deviation of a single element!\n");
    }

    if (assy) {
        stats(nums, N, &xb, &sb, &t, 1);
        PyMem_Free(nums);
        return Py_BuildValue("ddd", xb, sb, t);
    } else {
        stats(nums, N, &xb, &sb, NULL, 0);
        PyMem_Free(nums);
        return Py_BuildValue("dd", xb, sb);
    }
}








static PyObject *Function_drand(PyObject *self) {
    double num;    
    num = drand();        
    return Py_BuildValue("d", num);
}







static PyObject *Function_drand_SF(PyObject *self, PyObject *args, PyObject *kwds) {   
    double gamma=2.3;
    double x0=1.;
    double num;

    // Parse the input
    static char *kwlist[] = {"gamma", "x0", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|dd", kwlist, &gamma, &x0))
        return 0;
    if (x0==1.) {
        num = drand_SF(gamma);
    } else {
        num = drand_SF_xmin(gamma, x0);
    }
    return Py_BuildValue("d", num);
}





static PyObject *Function_irand_SF(PyObject *self, PyObject *args, PyObject *kwds) {   
    double gamma=2.3;
    int x0=1;
    int num;
    int iMAX=4000000;

    // Parse the input
    static char *kwlist[] = {"gamma", "x0", "iMAX", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|dii", kwlist, &gamma, &x0, &iMAX))
        return 0;
    if (x0==1) {
        num = irand_SF(gamma, iMAX);
    } else {
        num = irand_SF_xmin(gamma, x0, iMAX);
    }
    return Py_BuildValue("i", num);
}



static PyObject *Function_lnL(PyObject *self, PyObject *args, PyObject *kwds) {   
    double gamma=2.3, res;
    int x0=1;
    int nsum=20, N, i;
    int *nums;
    PyObject *xi;

    // Parse the input
    static char *kwlist[] = {"xi", "gamma", "x0", "nsum", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|dii", kwlist, &xi, &gamma, &x0, &nsum))
        return 0;
    N = (int) PyList_Size(xi);
    nums = PyMem_New(int, N);
    for (i=0; i<N; i++) {
        *(nums + i) = (int) PyLong_AsSsize_t(PyList_GetItem(xi, i));
    }
    res = lnL(nums, N, gamma, x0, nsum);
    PyMem_Free(nums);
    return Py_BuildValue("d", res);
}


static PyObject *Function_lnL_cont(PyObject *self, PyObject *args, PyObject *kwds) {   
    double gamma=2.3, res;
    double xmin=1.;
    PyObject *xi;
    double *nums;
    int N, i;

    // Parse the input
    static char *kwlist[] = {"xi", "gamma", "x0", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|dd", kwlist, &xi, &gamma, &xmin))
        return 0;
    N = (int) PyList_Size(xi);
    nums = PyMem_New(double, N);
    for (i=0; i<N; i++) {
        *(nums + i) = (double) PyFloat_AsDouble(PyList_GetItem(xi, i));
    }
    res = lnL_cont(nums, N, gamma, xmin);
    PyMem_Free(nums);
    return Py_BuildValue("d", res);
}



static PyObject *Function_zeta(PyObject *self, PyObject *args, PyObject *kwds) {   
    double gamma, res;
    int N=20;
    int xmin=1;

    // Parse the input
    static char *kwlist[] = {"gamma", "xmin", "N", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "d|ii", kwlist, &gamma, &xmin, &N))
        return 0;
    
    if (xmin==1) {
        res = zeta(gamma, N);
    } else {
        res = zeta_xmin(gamma, N, xmin);
    }
    return Py_BuildValue("d", res);
}


static PyObject *Function_dzetadx(PyObject *self, PyObject *args, PyObject *kwds) {   
    double gamma, res;
    int N=20;
    int xmin=1;

    // Parse the input
    static char *kwlist[] = {"gamma", "xmin", "N", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "d|ii", kwlist, &gamma, &xmin, &N))
        return 0;
    
    if (xmin==1) {
        res = dzetadx(gamma, N);
    } else {
        res = dzetadx_xmin(gamma, N, xmin);
    }
    return Py_BuildValue("d", res);
}




static PyObject *Function_gamma_MLE(PyObject *self, PyObject *args, PyObject *kwds) {   
    double gx0=2.3;
    double eps=1.e-8;
    int xmin=1, unc=0;
    int nsum=20;
    PyObject *xi;
    int N, i;
    int *nums;
    double res;

    // Parse the input
    static char *kwlist[] = {"xi", "x0", "uncert", "gamma0", "eps", "nsum", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|iiddi", kwlist, &xi, &xmin, &unc, &gx0, &eps, &nsum))
        return 0;
    
    N = (int) PyList_Size(xi);
    nums = PyMem_New(int, N);
    for (i=0; i<N; i++) {
        *(nums + i) = (int) PyLong_AsSsize_t(PyList_GetItem(xi, i));
    }
    if (unc) {
        double gp, gn;
        if (xmin==1) {
            res = gamma_MLE(nums, N, gx0, eps, nsum);
        } else {
            res = gamma_MLE_xmin(nums, N, xmin, gx0, eps, nsum);
        }
        uncertainty_int(nums, N, res, xmin, eps, &gp, &gn, nsum);
        PyMem_Free(nums);
        return Py_BuildValue("d(d, d)", res, gp, gn);
    } else {
        if (xmin==1) {
            res = gamma_MLE(nums, N, gx0, eps, nsum);
        } else {
            res = gamma_MLE_xmin(nums, N, xmin, gx0, eps, nsum);
        }
        PyMem_Free(nums);
        return Py_BuildValue("d", res);
    }
}


static PyObject *Function_gamma_MLE_cont(PyObject *self, PyObject *args, PyObject *kwds) {   
    double x0=1.;
    double delt=0.02;
    PyObject *xi;
    int N, i, unc=0;
    double *nums;
    double res;
    double eps=1.e-8;

    // Parse the input
    static char *kwlist[] = {"xi", "x0", "uncert", "eps", "delt", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|didd", kwlist, &xi, &x0, &unc, &eps, &delt))
        return 0;
    
    N = (int) PyList_Size(xi);
    nums = PyMem_New(double, N);
    for (i=0; i<N; i++) {
        *(nums + i) = (double) PyFloat_AsDouble(PyList_GetItem(xi, i));
    }
    if (x0==0.) {
        double gamma=2.3, xmin=1.; // This part is not ok
        maxLKHD_gamma_cont(nums, N, &gamma, &xmin, delt);
        if (unc) {
            double gp, gn;
            uncertainty_cont(nums, N, gamma, xmin, eps, &gp, &gn);
            PyMem_Free(nums);
            return Py_BuildValue("dd(d, d)", gamma, xmin, gp, gn);
        } else {
            PyMem_Free(nums);
            return Py_BuildValue("dd", gamma, xmin);        
        }
    } else {
        res = gamma_MLE_cont(nums, N, x0);
        if (unc) {
            double gp, gn;
            uncertainty_cont(nums, N, res, x0, eps, &gp, &gn);
            PyMem_Free(nums);
            return Py_BuildValue("d(d, d)", res, gp, gn);
        } else {
            PyMem_Free(nums);
            return Py_BuildValue("d", res);        
        }
    }
}





