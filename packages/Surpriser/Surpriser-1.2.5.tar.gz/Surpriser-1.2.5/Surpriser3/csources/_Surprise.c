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
#include "surprise.h"
#include "randoms.h"



// *******************************************
/*           Doc strings                    */
// *******************************************
//
// Module 
static char Surprise_docstring[] = "Surpriser object and other functions.";
// Object 
static char Surpriser_docstring[] = "Surpriser Object\n\
                                      to call:\n\
                                     >>> sur = Surpriser(M, coms=[])";
// Attributes
static char K_docstring[] = "Number of nodes in the graph";
static char F_docstring[] = "Number of links in the complete network";
static char M_docstring[] = "Number of links if every community is a clique";
static char p_docstring[] = "Actual number of links between nodes in the same communities";
static char nl_docstring[] = "Total actual number of links in the network";
static char Nc_docstring[] = "Number of communities";
//static char Csur_docstring[] = "C type Surpriser Object (pointer for internal use)";
static char surprise_docstring[] = "Surprise corresponding to the present partition";
// Methods
static char show_communities_docstring[] = "Shows the nodes in each community (on screen)";
static char partition_docstring[] = "Returns the community partition list.";
static char linksin_docstring[] = "Links between and from a list of nodes\n\
                                   \n\
                                   Usage:\n links_in, links_out = Surpriser.linksin(Lista)";
static char merger_docstring[] = "Merges communities.\n\
                                  \n\
                                  Usage:\n im = Surpriser.merger(ic1=-1, ic2=-1, N=1, BfA=False)\n\
                                  \n\
                                  Returns (im) the number of merges done.\n\
                                  If N>1, tries to performs merges raising the surprise N times.\n\
                                  If N=0, it will perform a merge even if the surprise value is not raised.\n\
                                  The ic1 and ic2 are the community numbers to be merged.\n\
                                    If they are less than zero, the communities are chosen at random.\n\
                                  The BfA (best from all) Tells wheather ic1 merge must be tested with all \n\
                                   possible communities and then performs only the best merge.";
static char exchanger_docstring[] = "Exchanges element between communities.\n\
                                     \n\
                                     Usage:\n ie = Surpriser.exchanger(ic1=-1, ic2=-1, N=1, iex=-1, BfA=False)\n\
                                     \n\
                                     Returns (ie) the number of exchanges done.\n\
                                     If N>1, tries to performs exchanges raising the surprise N times.\n\
                                     If N=0, it will perform an exchange even if the surprise value is not raised.\n\
                                     The ic1 and ic2 are the community numbers between which iex element is exchanged.\n\
                                       If they are less than zero, the communities and the element are chosen at random.\n\
                                       The element is taken from community ic1 to community ic2.\n\
                                     The BfA (best from all) Tells wheather all elements from ic1 must be tested with all \n\
                                      possible communities and then performs only the best exchange.";
static char extractor_docstring[] = "Extracts elements from communities.\n\
                                     \n\
                                     Usage:\n ix = Surpriser.extractor(ic1=-1, N=1, iex=-1)\n\
                                     \n\
                                     Returns (ix) the number of extractions done.\n\
                                     If N>1, tries to performs extractions raising the surprise N times.\n\
                                     If N=0, it will perform an extraction even if the surprise value is not raised.\n\
                                     The ic1 is the community number from which iex element is extracted.\n\
                                       If they are less than zero, the community and the element are chosen at random.\n\
                                     If N>0, only performs the best possible extraction.";
static char community_docstring[] = "Returns the list with the nodes in a community\n\
                                    \n\
                                    Usage:\n List_nodes = Surpriser.community(icom)";
static char connected_docstring[] = "Checks if two nodes are connected\n\
                                    \n\
                                    Usage:\n Surpriser.connected(i1, i2)";
static char montecarlo_step_docstring[] = "Makes a Monte-Carlo step. It will perform K times the annealing operations \n\
                                        in the following order: First tries a merge, then an exchange and then an extraction. \n\
                                        If the operations should be performed in the subcommunity level, it then tries to perform\n\
                                        a subcommunity extraction and then an exchange.\n\
                                        Usage: N = Surpriser.montecarlo_step( T=1., K=self.K, subcoms=0 ) \n\
                                        It return the number of successfull operations done. If the argument subcoms \n\
                                        is evaluated as True, it perform the operations over subcommunities.";
static char checkN_docstring[] = "Checks, without performing, what the change in surprise would be for each possible operation. \n\
                                   Usage: list_changes = Surpriser.checkN( im=-1, iex=-1, iec1=-1, iec2=-1, iscex=-1, isc1=-1, isc2=-1 )\n\
                                   The returned list are the changes in surprise. Its size depends on the operation investigated. If \n\
                                   im is given, it checks the merge of the community to all others (element im of the returned list is zero),\n\
                                   if iex is given, checks the extraction of each element in the given community, if iec1 and iec2 are given,\n\
                                   check the exchanges of each element from community iec1 to community iec2. If iscex is given, checks \n\
                                   the extraction of each subcommunity from this community and if isc1 and isc2 are given, the exchange of \n\
                                   each subcommunity from isc1 to isc2. It checks only one operation, if more than one possible ic are given\n\
                                   in the function call, will only perform the first one appearing.";
static char stepper0_docstring[] = "Performs once all modifications that do not change the surprise value.\n\
                                   Usage: n1, n2 = Surprise.shake(subcoms=1)\n\
                                   Returns the number of exchanges (n1) and subcommunity exchanges (n2) done.";
static char stepper_docstring[] = "Performs the algorith: All possible merges, exchanges and extractions \n\
                                    that raise the surprise, until no improvement is obtained.\n\
                                    \n\
                                    Usage:\n n1, n2, n3, n4, n5 = Surpriser.stepper()\n\
                                     n1 -> number of subcommunities extractions done.\n\
                                     n2 -> number of subcommunities exchanges done.\n\
                                     n3 -> number of merges done. Change these!\n\
                                     n4 -> number of element extractions done.\n\
                                     n5 -> number of element exchanges done.";
static char subcommuniter_docstring[] = "Extracts subcommunities from the communities.\n\
                                         \n\
                                         Usage:\n isx = Surpriser.subcommuniter(ic=-1, N=1, iex=-1)\n\
                                         \n\
                                     Returns (isx) the number of extractions done.\n\
                                     If N>1, tries to perform N extractions raising the surprise.\n\
                                     If N=0, it will perform an extraction even if surprise is not raised.\n\
                                     The ic is the community number from which iex subcommunity is extracted.\n\
                                       If they are less than zero, the community and the subcommunity are chosen at random.\n\
                                     If N>0, only performs the best possible extractions.";
static char subcommunity_exchanger_docstring[] = "Exchanges subcommunities between communities \n\
                                                  \n\
                                                  Usage: \n isx = Surpriser.subcommuniter_exchange(ic1=-1, ic2=-1, N=1, iex=-1, BfA=0)\n\
                                                  \n\
                                                  Returns (ix) the number of exchanges done.\n\
                                                  If N>1, tries to performs exchanges raising the surprise from N trials.\n\
                                                  If N=0, it will perform an exchange even if surprise is not raised.\n\
                                                  The ic1 and ic2 are the community numbers between which iex subcommunity (from ic1) is exchanged.\n\
                                                  If they are less than zero, the communities and the subcommunity are chosen at random.\n\
                                                  If N>0, only performs the best possible exchanges.";
static char subcommunity_docstring[] = "Returns the Surpriser object corresponding to the subgraph formed by a given community (i)\n\
                                       \n\
                                       Usage:\n SubComSurpriser = Surpriser.subcommunity(i)";
static char merger_an_docstring[] = "Merges communities (Annealing).\n\
                                  \n\
                                  Usage:\n im = Surpriser.merger_an(ic1=-1, ic2=-1, N=1, T=1.)\n\
                                  \n\
                                  Returns (im) the number of merges done.\n\
                                  Performs N trials. Executes the merge if the surprise value is increased\n\
                                  and if not with probability exp(-Delta_S/T). \n\
                                  The ic1 and ic2 are the community numbers to be merged.\n\
                                    If they are less than zero, the communities are chosen at random.";
static char exchanger_an_docstring[] = "Exchanges element between communities (Annealing).\n\
                                     \n\
                                     Usage:\n ie = Surpriser.exchanger_an(ic1=-1, ic2=-1, N=1, T=1.)\n\
                                     \n\
                                     Returns (ie) the number of exchanges done.\n\
                                     Performs N trials. Executes the exchange if the surprise value is increased\n\
                                     and if not with probability exp(-Delta_S/T). \n\
                                     The ic1 and ic2 are the community numbers between which an element should be exchanged.\n\
                                       If they are less than zero, the communities are chosen at random..";
static char extractor_an_docstring[] = "Extracts an element from communities (Annealing).\n\
                                     \n\
                                     Usage:\n ix = Surpriser.extractor_an(ic1=-1, N=1, T=1.)\n\
                                     \n\
                                     Returns (ix) the number of extractions done.\n\
                                     Performs N trials. Executes a extraction if the surprise value is increased\n\
                                     and if not with probability exp(-Delta_S/T). \n\
                                     The ic1 is the community from which an element should be extracted.\n\
                                       If it is less than zero, the community is chosen at random.";
static char subcommuniter_an_docstring[] = "Tries to remove subcommunity from a community (anealing). \n\
                                         Usage: N = Surpriser.subcommuniter_an( isc=-1, N=1, T=1. )\n\
                                         Returns the number of subcommunity extractions actually done.";
static char subcommunity_exchanger_an_docstring[] = "Tries to exchange a subcommunity from a community (anealing)\n\
                                                  Usage: N = Surpriser.subcommunity_exchanger_an( isc=-1, N=1, T=1. )\n\
                                                  Returns the number of subcommunity exchanges actually done.";
// Functions
static char Function_fact_docstring[] = "Evaluates the natural logarithm of a factorial.\n\
                                         Usage: lnfact = fact(N)\n\
                                         Returns log(factorial(N)).";
static char Function_gammas_docstring[] = "Evaluates the natural logarithm of a combination.\n\
                                         Usage: lncomb = gammas(n, k)\n\
                                         returns log(factorial(n))-log(factorial(k))-log(factorial(n-k)).";
static char Function_surprise_docstring[] = "Evaluates the surprise.\n\
                                            Usage: S = surprise( M, F, n, p )\n\
                                            M is the number of possible links inside communities, F is the total number of possible\n\
                                            links in the network (size of clique of size K, where K is the number of vertices in the graph),\n\
                                            n is the actual number of links the the network and p is the number of links inside communities.";
static char Function_compare_docstring[] = "Returns the variation of information between two partitions.\n\
                                           Usage: VI = compare(partition1, partition2)\n\
                                           Each partition should be a list (both of the same size) containing numbers between\n\
                                           0 and Nc-1 (the number of comunities in the partition).";
static char Function_ChiGrad_docstring[] = "Chisq and its gradient.\n\
                                     Usage: chi2, grad, tot = ChiGrad( matr, coords, gamma=-1, N=0, dlim=0.1 )\n\
                                     Returns de value of chi2, the gradient of chi2 in parameter space (2N-dimesional vector, \n\
                                     returned as a list of N lists with two elements) and the modulus of this vector:\n\
                                     matr is the distance matrix, coords are the embedded\n\
                                     coordinates, gamma gives more importance to points further (>0) or closer (<0) apart,\n\
                                     N the dimension of the matrix to be considered (if 0 the whole matrix is) and dlim is the\n\
                                     maximum distance two points must be in order for their distance to be considered.";
static char Function_embedding_docstring[] = "Two dimensional embedding.\n\
                                     Usage: coords = embedding(matr, coords=[], gamma=-1, dlim=0.1, lamb=2., adj=0.05, eps=1.e-10 )\n\
                                     Returns the coordinates corresponding to an embedding (the difference between the euclidean distances \n\
                                     and the distances in the matrix are as close as possible to zero). coords is an initial guess for\n\
                                     the coordinates (if not given the points are randomly chosen around the origin), gamma gives more \n\
                                     importance to points further (>0) or closer (<0) apart, dlim is the maximum distance two points must \n\
                                     be in order for their distance to be considered, lamb is how greedly initialy the algorithm will \n\
                                     searche for the minimum of chi2, adj is how lambda is adjusted each succesful or unsuccessful step\n\
                                     and eps is the precision below which the algorith will consider that the minimum is reached.";


// *******************************************
/*          Surpriser Type definition       */
// *******************************************
// The Surpriser structure.
typedef struct {
    PyObject_HEAD
    int K;
    int F;
    int p;
    int nl;
    int M;
    int Nc;
    double surprise;
    Surpriser *Csur;
} Surprise;
// initialization
static int Surpriser_init(Surprise *self, PyObject *args, PyObject *kwds);
static PyObject *Surpriser_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
// Deconstruction
static void Surpriser_dealloc(Surprise *self) {
    clear_surp(self->Csur);
    PyMem_Free(self->Csur);
    Py_TYPE(self)->tp_free((PyObject *) self);
    //self->ob_type->tp_free((PyObject*)self);
}



// Attributes (members)
static PyMemberDef
Surpriser_members[] = {
    { "K", T_INT, offsetof(Surprise, K), 0, K_docstring },
    { "F", T_INT, offsetof(Surprise, F), 0, F_docstring },
    { "p", T_INT, offsetof(Surprise, p), 0, p_docstring },
    { "nl", T_INT, offsetof(Surprise, nl), 0, nl_docstring },
    { "M", T_INT, offsetof(Surprise, M), 0, M_docstring },
    { "Nc", T_INT, offsetof(Surprise, Nc), 0, Nc_docstring },
    //{ "Csur", T_PYSSIZET, offsetof(Surprise, Csur), 0, Csur_docstring },
    { "surprise", T_DOUBLE, offsetof(Surprise, surprise), 0, surprise_docstring },
    { NULL }
};


// Methods
static PyObject *Surpriser_repr(Surprise *self);
static PyObject *Surpriser_show_communities(Surprise *self);
static PyObject *Surpriser_partition(Surprise *self);
static PyObject *Surpriser_linksin(Surprise *self, PyObject *args);
static PyObject *Surpriser_merger(Surprise *self, PyObject *args, PyObject *kwds);
static PyObject *Surpriser_exchanger(Surprise *self, PyObject *args, PyObject *kwds);
static PyObject *Surpriser_extractor(Surprise *self, PyObject *args, PyObject *kwds);
static PyObject *Surpriser_community(Surprise *self, PyObject *args);
static PyObject *Surpriser_connected(Surprise *self, PyObject *args);
static PyObject *Surpriser_montecarlo_step(Surprise *self, PyObject *args, PyObject *kwds);
static PyObject *Surpriser_checkN(Surprise *self, PyObject *args, PyObject *kwds);
static PyObject *Surpriser_stepper0(Surprise *self, PyObject *args, PyObject *kwds);
static PyObject *Surpriser_stepper(Surprise *self, PyObject *args, PyObject *kwds);
static PyObject *Surpriser_subcommuniter(Surprise *self, PyObject *args, PyObject *kwds);
static PyObject *Surpriser_subcommunity_exchanger(Surprise *self, PyObject *args, PyObject *kwds);
static PyObject *Surpriser_subcommunity(Surprise *self, PyObject *args);
static PyObject *Surpriser_merger_an(Surprise *self, PyObject *args, PyObject *kwds);
static PyObject *Surpriser_exchanger_an(Surprise *self, PyObject *args, PyObject *kwds);
static PyObject *Surpriser_extractor_an(Surprise *self, PyObject *args, PyObject *kwds);
static PyObject *Surpriser_subcommuniter_an(Surprise *self, PyObject *args, PyObject *kwds);
static PyObject *Surpriser_subcommunity_exchanger_an(Surprise *self, PyObject *args, PyObject *kwds);
static PyMethodDef Surpriser_methods[] = {
    { "show_communities",    (PyCFunction) Surpriser_show_communities, METH_NOARGS, show_communities_docstring },
    { "partition",    (PyCFunction) Surpriser_partition, METH_NOARGS, partition_docstring },
    { "linksin", (PyCFunction) Surpriser_linksin, METH_VARARGS, linksin_docstring},
    { "merger",    (PyCFunction) Surpriser_merger, METH_VARARGS | METH_KEYWORDS, merger_docstring },
    { "exchanger",    (PyCFunction) Surpriser_exchanger, METH_VARARGS | METH_KEYWORDS, exchanger_docstring },
    { "extractor",    (PyCFunction) Surpriser_extractor, METH_VARARGS | METH_KEYWORDS, extractor_docstring },
    { "community", (PyCFunction) Surpriser_community, METH_VARARGS, community_docstring},
    { "connected", (PyCFunction) Surpriser_connected, METH_VARARGS, connected_docstring},
    { "montecarlo_step",    (PyCFunction) Surpriser_montecarlo_step, METH_VARARGS | METH_KEYWORDS, montecarlo_step_docstring },
    { "checkN",    (PyCFunction) Surpriser_checkN, METH_VARARGS | METH_KEYWORDS, checkN_docstring },
    { "shake",    (PyCFunction) Surpriser_stepper0, METH_VARARGS | METH_KEYWORDS, stepper0_docstring },
    { "stepper",    (PyCFunction) Surpriser_stepper, METH_VARARGS | METH_KEYWORDS, stepper_docstring },
    { "subcommuniter", (PyCFunction) Surpriser_subcommuniter, METH_VARARGS | METH_KEYWORDS, subcommuniter_docstring},
    { "subcommunity_exchanger", (PyCFunction) Surpriser_subcommunity_exchanger, METH_VARARGS | METH_KEYWORDS, subcommunity_exchanger_docstring},
    { "subcommunity", (PyCFunction) Surpriser_subcommunity, METH_VARARGS, subcommunity_docstring},
    { "merger_an",    (PyCFunction) Surpriser_merger_an, METH_VARARGS | METH_KEYWORDS, merger_an_docstring },
    { "exchanger_an",    (PyCFunction) Surpriser_exchanger_an, METH_VARARGS | METH_KEYWORDS, exchanger_an_docstring },
    { "extractor_an",    (PyCFunction) Surpriser_extractor_an, METH_VARARGS | METH_KEYWORDS, extractor_an_docstring },
    { "subcommuniter_an", (PyCFunction) Surpriser_subcommuniter_an, METH_VARARGS | METH_KEYWORDS, subcommuniter_an_docstring},
    { "subcommunity_exchanger_an", (PyCFunction) Surpriser_subcommunity_exchanger_an, METH_VARARGS | METH_KEYWORDS, subcommunity_exchanger_an_docstring},
    { NULL, NULL, 0, NULL }
};

// Type
static PyTypeObject SurpriserType = {
    PyVarObject_HEAD_INIT(NULL, 0) /* ob_size */
    "Surpriser",               /* tp_name */
    sizeof(Surprise),         /* tp_basicsize */
    0,                         /* tp_itemsize */
    (destructor)Surpriser_dealloc, /* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_compare */
    (reprfunc)Surpriser_repr,     /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags*/
    Surpriser_docstring,        /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    Surpriser_methods,         /* tp_methods */
    Surpriser_members,         /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)Surpriser_init,  /* tp_init */
    0,                         /* tp_alloc */
    Surpriser_new,               /* tp_new */
};




// *******************************************
/*             Module functions             */
// *******************************************
/* function header */
static PyObject *Function_fact(PyObject *self, PyObject *args);
static PyObject *Function_gammas(PyObject *self, PyObject *args);
static PyObject *Function_surprise(PyObject *self, PyObject *args);
static PyObject *Function_compare(PyObject *self, PyObject *args);
static PyObject *Function_ChiGrad(PyObject *self, PyObject *args, PyObject *kwds);
static PyObject *Function_embedding(PyObject *self, PyObject *args, PyObject *kwds);
/* Functions that will be callable from python */
static PyMethodDef module_methods[] = {
    {"fact", (PyCFunction)Function_fact, METH_VARARGS, Function_fact_docstring},
    {"gammas", (PyCFunction)Function_gammas, METH_VARARGS, Function_gammas_docstring},
    {"surprise", (PyCFunction)Function_surprise, METH_VARARGS, Function_surprise_docstring},
    {"compare", (PyCFunction)Function_compare, METH_VARARGS, Function_compare_docstring},
    {"ChiGrad", (PyCFunction)Function_ChiGrad, METH_VARARGS | METH_KEYWORDS, Function_ChiGrad_docstring },
    {"embedding", (PyCFunction)Function_embedding, METH_VARARGS | METH_KEYWORDS, Function_embedding_docstring },
    {NULL, NULL, 0, NULL}
};




// *******************************************
/*           Initialization                 */
// *******************************************

static struct PyModuleDef surprisemodule = {
    PyModuleDef_HEAD_INIT,    
    "surprise",
    Surprise_docstring,
    -1,
    module_methods  
};


PyMODINIT_FUNC PyInit_surprise(void) {
    PyObject* mod;
    seed(); // new seed for random numbers
    reseed();
    // Create the module
    //mod = Py_InitModule3("surprise", module_methods, Surprise_docstring);
    mod = PyModule_Create(&surprisemodule);
    if (mod == NULL) {
       return NULL;
    }
    // Fill in some slots in the type, and make it ready
    if (PyType_Ready(&SurpriserType) < 0) {
       return NULL;
    }
    // Add the type to the module.
    Py_INCREF(&SurpriserType);
    PyModule_AddObject(mod, "Surpriser", (PyObject*)&SurpriserType);
    return mod;
}


// *******************************************
/*     __    Methods   __                   */
// *******************************************


static int Surpriser_init(Surprise *self, PyObject *args, PyObject *kwds) {
    // __init__ Initialization funcion
    int i, j, K, Nc, cs;
    PyObject *Matr;
    PyObject *Coms = Py_BuildValue("[]");
    int *comsizes=NULL, **communities=NULL;
    /* Parse the input  */
    static char *kwlist[] = {"matr", "communities", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|O", kwlist, &Matr, &Coms))
        return 0;
    K = (int) PyList_Size(Matr);
    // checks if communitites are there
    Nc = (int) PyList_Size(Coms);
    /* Reads the Matrix */
    int *y = malloc(sizeof(int)*K*K);
    for (i=0; i<K; i++) {
        PyObject *linha = PyList_GetItem(Matr,i);
        for (j=0; j<K; j++) {
            *(y + i*K + j) = (int) PyLong_AsSsize_t(PyList_GetItem(linha,j));
        }
    }
    // Reads the communitites
    if (Nc>0) {
        comsizes = calloc(K, sizeof(int));
        communities = malloc(K*sizeof(int*));
        for (i=0;i<K;i++) {*(communities+i)=calloc(K, sizeof(int));}
        for (i=0;i<Nc;i++) {
            PyObject *community = PyList_GetItem(Coms,i);
            cs = (int) PyList_Size(community);
            *(comsizes + i) = cs;
            for (j=0;j<cs;j++) {
                *(*(communities+i) + j) = (int) PyLong_AsSsize_t(PyList_GetItem(community, j));
            }
        }
    }
    //printf("Here 1!\n");
    // creates c Surpriser
    //free(self->Csur);
    self->Csur = PyMem_New(Surpriser, 1);
    generate_supriser(y, K, communities, comsizes, self->Csur);
    //printf("Here 2!\n");
    // Creates Python Objects
    // C Attributes (members)
    self->K = K;
    self->nl = self->Csur->nl;
    self->M = self->Csur->M;
    self->F = self->Csur->F;
    self->Nc = self->Csur->Nc;
    self->p = self->Csur->p;
    self->Csur = self->Csur;
    self->surprise = (self->Csur)->surprise;
    // discards garbage
    free(y);
    if (communities) {
        for (i=0;i<K;i++) {
            free(*(communities + i));
        }
        free(communities);
    }
    if (comsizes) {free(comsizes);}
    //printf("Here 3!\n");
    return 0;
}

static PyObject *Surpriser_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
    Surprise *self;
    self = (Surprise *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->K = 0;
        self->Nc = 0;
        self->nl = 0;
        self->M = 0;
        self->F = 0;
        self->p = 0;
        self->Csur = PyMem_New(Surpriser, 1);
    }
    return (PyObject *)self;
}



static PyObject *Surpriser_repr(Surprise *self) {
    // __repr__ representation function
    
    char *s = NULL;
    if (! asprintf(&s, "< Graph/communities info :\n   Number of nodes       : %d\n   Number of links       : %d (%d)\n   Number of communities : %d\n   Number of intralinks  : %d (%d)\n   Surprise              : %f >", (self->Csur->K), (self->Csur->nl), (self->Csur->F), (self->Csur->Nc), (self->Csur->p), (self->Csur->M), (self->Csur->surprise) )) {return Py_BuildValue("");} 
    return Py_BuildValue("s", s);
}




static PyObject *Surpriser_show_communities(Surprise *self) {
    /* shows communities */
    show_communities(self->Csur);
    return Py_BuildValue("");
}



static PyObject *Surpriser_partition(Surprise *self) {
    int *part;
    int K, j;
    
    K = self->Csur->K;
    part = malloc(K * sizeof(int));
    partition(self->Csur, part);
    
    PyObject *PyPart = PyList_New(K);
    for (j=0; j<K; j++) {
        PyObject *num = PyLong_FromSsize_t(*(part+j));
        PyList_SetItem(PyPart, j, num);
    }
    
    free(part);
    return Py_BuildValue("O", PyPart);
}




static PyObject *Surpriser_linksin(Surprise *self, PyObject *args) {
    // __init__ Initialization funcion
    int i, N;
    int intra, extra;
    PyObject *com;
    int *ccom=NULL;
    if (!PyArg_ParseTuple(args, "O", &com))
        return 0;

    N = (int) PyList_Size(com);
    ccom = malloc(sizeof(int)*N);
    for (i=0; i<N; i++) {
        *(ccom + i) = (int) PyLong_AsSsize_t(PyList_GetItem(com, i));
    }
    intra = intralinks_m(self->Csur->matr, ccom, N, self->K, &extra);
    free(ccom);
    return Py_BuildValue("ii", intra, extra);
}





static PyObject *Surpriser_merger(Surprise *self, PyObject *args, PyObject *kwds) {
    int ic1=-1, ic2=-1, N=1, res=0, bfa=0, ii;

    // Parse the input  
    static char *kwlist[] = {"ic1", "ic2", "N", "BfA", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iiii", kwlist, &ic1, &ic2, &N, &bfa))
        return 0;
    if ((ic1>=self->Csur->Nc)|(ic2>=self->Csur->Nc)) {return Py_BuildValue("i", res);}
    //
    //
    if (bfa) {
        if (N>1) {
            for (ii=0; ii<N; ii++) {
                ic1 = self->Csur->Nc * drand();
                res += merger3(self->Csur, ic1);
            }
        } else {
            if (ic1<0) {ic1 = self->Csur->Nc * drand();}
            res = merger3(self->Csur, ic1);
        }
    } else if (N==0) {
        if (ic1<0) {ic1 = self->Csur->Nc * drand();}
        if (ic2<0) {ic2 = self->Csur->Nc * drand();}
        while ( (ic1==ic2)&(self->Csur->Nc>1) ) {ic2 = self->Csur->Nc * drand();}
        res = merge(self->Csur, ic1, ic2);
    } else if (N>1) {
        for (ii=0; ii<N; ii++) {
            ic1 = self->Csur->Nc * drand();
            ic2 = self->Csur->Nc * drand();
            while ((ic1==ic2)&(self->Csur->Nc>1)) {ic2 = self->Csur->Nc * drand();}
            res += merger(self->Csur, ic1, ic2);
        }
    } else {
        if (ic1<0) {ic1 = self->Csur->Nc * drand();}
        if (ic2<0) {ic2 = self->Csur->Nc * drand();}
        while ((ic1==ic2)&(self->Csur->Nc>1)) {ic2 = self->Csur->Nc * drand();}
        res = merger(self->Csur, ic1, ic2);
    }
    self->K = self->Csur->K;
    self->nl = self->Csur->nl;
    self->M = self->Csur->M;
    self->F = self->Csur->F;
    self->Nc = self->Csur->Nc;
    self->p = self->Csur->p;
    self->surprise = self->Csur->surprise;
    return Py_BuildValue("i", res);
}



static PyObject *Surpriser_extractor(Surprise *self, PyObject *args, PyObject *kwds) {
    int ic1=-1, N=1, res=0, iex=-1, ii, bfa=0;

    // Parse the input  
    static char *kwlist[] = {"ic1", "N", "iex", "BfA", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iiii", kwlist, &ic1, &N, &iex, &bfa))
        return 0;
    if (ic1>=self->Csur->Nc) {return Py_BuildValue("i", res);}
    if (bfa) {
        if (N>1) {
            for (ii=0; ii<N; ii++) {
                ic1 = self->Csur->Nc * drand();
                res += extractor2(self->Csur, ic1);
            }
        } else if (N==1) {
            if (ic1<0) {ic1 = self->Csur->Nc * drand();}
            res = extractor2(self->Csur, ic1);
        }  else {
            if (ic1<0) {ic1 = self->Csur->Nc * drand();}
            if (iex<0) {iex = *(self->Csur->comsizes+ic1) * drand();}
            res = extract(self->Csur, ic1, iex);
        }
    } else {
        if (N>1) {
            for (ii=0; ii<N; ii++) {
                ic1 = self->Csur->Nc * drand();
                res += extractor(self->Csur, ic1);
            }
        } else if (N==1) {
            if (ic1<0) {ic1 = self->Csur->Nc * drand();}
            res = extractor(self->Csur, ic1);
        }  else {
            if (ic1<0) {ic1 = self->Csur->Nc * drand();}
            if (iex<0) {iex = *(self->Csur->comsizes+ic1) * drand();}
            res = extract(self->Csur, ic1, iex);
        }
    }
    self->K = self->Csur->K;
    self->nl = self->Csur->nl;
    self->M = self->Csur->M;
    self->F = self->Csur->F;
    self->Nc = self->Csur->Nc;
    self->p = self->Csur->p;
    self->surprise = self->Csur->surprise;
    return Py_BuildValue("i", res);
}


static PyObject *Surpriser_exchanger(Surprise *self, PyObject *args, PyObject *kwds) {
    int ic1=-1, ic2=-1, N=1, res=0, iex=-1, bfa=0, ii;

    // Parse the input  
    static char *kwlist[] = {"ic1", "ic2", "N", "iex", "BfA", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iiiii", kwlist, &ic1, &ic2, &N, &iex, &bfa))
        return 0;
    if ((ic1>=self->Csur->Nc)|(ic2>=self->Csur->Nc)) {return Py_BuildValue("i", res);}
    //
    //
    if (bfa) {
        if (N>1) {
            for (ii=0; ii<N; ii++) {
                ic1 = self->Csur->Nc * drand();
                res += exchanger3(self->Csur, ic1);
            }
        } else {
            if (ic1<0) {ic1 = self->Csur->Nc * drand();}
            res = exchanger3(self->Csur, ic1);
        }
    } else if (N==0) {
        if (ic1<0) {ic1 = self->Csur->Nc * drand();}
        if (ic2<0) {ic2 = self->Csur->Nc * drand();}
        if (iex<0) {iex = *(self->Csur->comsizes + ic1) * drand();}
        while ((ic1==ic2)&(self->Csur->Nc>1)) {ic2 = self->Csur->Nc * drand();}
        res = exchange(self->Csur, ic1, ic2, iex);
    } else if (N>1) {
        for (ii=0; ii<N; ii++) {
            ic1 = self->Csur->Nc * drand();
            ic2 = self->Csur->Nc * drand();
            while ((ic1==ic2)&(self->Csur->Nc>1)) {ic2 = self->Csur->Nc * drand();}
            res += exchanger(self->Csur, ic1, ic2);
        }
    } else {
        if (ic1<0) {ic1 = self->Csur->Nc * drand();}
        if (ic2<0) {ic2 = self->Csur->Nc * drand();}
        while ((ic1==ic2)&(self->Csur->Nc>1)) {ic2 = self->Csur->Nc * drand();}
        res = exchanger(self->Csur, ic1, ic2);
    }
    self->K = self->Csur->K;
    self->nl = self->Csur->nl;
    self->M = self->Csur->M;
    self->F = self->Csur->F;
    self->Nc = self->Csur->Nc;
    self->p = self->Csur->p;
    self->surprise = self->Csur->surprise;
    return Py_BuildValue("i", res);
}




static PyObject *Surpriser_community(Surprise *self, PyObject *args) {
    int i, j, cs, node;
    /* Parse the input  */
    if (!PyArg_ParseTuple(args, "i", &i))
        return 0;
    if (i>=self->Csur->Nc) {return Py_BuildValue("i", 0);}
    cs = *( (self->Csur) -> comsizes + i);
    PyObject *community = PyList_New(cs);
    for (j=0; j<cs; j++) {
        node = *(*(self->Csur->communities +i)+j);
        PyObject *num = PyLong_FromSsize_t(node);
        PyList_SetItem(community, j, num);
    } 

    return Py_BuildValue("O", community);
}


static PyObject *Surpriser_connected(Surprise *self, PyObject *args) {
    int i, j, cs;
    /* Parse the input  */
    if (!PyArg_ParseTuple(args, "ii", &i, &j))
        return 0;

    cs = *( (self->Csur) -> matr + i*self->K + j);
    return Py_BuildValue("i", cs);
}


static PyObject *Surpriser_montecarlo_step(Surprise *self, PyObject *args, PyObject *kwds) {
    /* Must review */
    double T=1.;
    int  K=0, subcoms=0;
    int N;

    static char *kwlist[] = {"T", "K", "subcoms", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|dii", kwlist, &T, &K, &subcoms))
        return 0;
    
    if (K==0) {
        K = self->Csur->K;
    }
    if (subcoms) {
        N = megastep(self->Csur, T, K);
    } else {
        N = megastepNSC(self->Csur, T, K);
    }
    
    self->K = self->Csur->K;
    self->nl = self->Csur->nl;
    self->M = self->Csur->M;
    self->F = self->Csur->F;
    self->Nc = self->Csur->Nc;
    self->p = self->Csur->p;
    self->surprise = self->Csur->surprise;
    return Py_BuildValue("i", N);
}


static PyObject *Surpriser_checkN(Surprise *self, PyObject *args, PyObject *kwds) {
    int im=-1, iex=-1, iec1=-1, iec2=-1, iscex=-1, isc1=-1, isc2=-1;
    int k2;
    int j;

    static char *kwlist[] = {"im", "iex", "iec1", "iec2", "iscex", "isc1", "isc2", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iiiiiii", kwlist, &im, &iex, &iec1, &iec2, &iscex, &isc1, &isc2))
        return 0;
    
    if (im>=0) {
        double *coms = malloc((self->Csur->Nc)*sizeof(double));
        mergerN(self->Csur, im, coms);
        PyObject *linha = PyList_New(self->Csur->Nc);
        for (j=0; j<self->Csur->Nc; j++) {
            PyObject *num = Py_BuildValue("d", *(coms + j));
            PyList_SetItem(linha, j, num);
        }
        free(coms);
        return linha;
    }
    if ( (iec1>=0) & (iec2>=0) ) {
        double *elems1 = malloc( *(self->Csur->comsizes+iec1) * sizeof(double));
        exchangerN(self->Csur, iec1, iec2, elems1);
        PyObject *linha = PyList_New(*(self->Csur->comsizes+iec1));
        for (j=0; j<*(self->Csur->comsizes+iec1); j++) {
            PyObject *num = Py_BuildValue("d", *(elems1 + j));
            PyList_SetItem(linha, j, num);
        }
        free(elems1);
        return linha;
    }
    if (iex>=0) {
        double *elems2 = malloc( *(self->Csur->comsizes+iex) * sizeof(double));;
        extractorN(self->Csur, iex, elems2);
        PyObject *linha = PyList_New(*(self->Csur->comsizes+iex));
        for (j=0; j<*(self->Csur->comsizes+iex); j++) {
            PyObject *num = Py_BuildValue("d", *(elems2 + j));
            PyList_SetItem(linha, j, num);
        }
        free(elems2);
        return linha;
    }    
    if (iscex>=0) {
        double *elems2 = malloc( *(self->Csur->comsizes+iscex) * sizeof(double));
        k2 = subcommuniterN(self->Csur, iscex, elems2);
        PyObject *linha = PyList_New(k2);
        for (j=0; j<k2; j++) {
            PyObject *num = Py_BuildValue("d", *(elems2 + j));
            PyList_SetItem(linha, j, num);
        }
        free(elems2);
        return linha;
    }    
    if ( (isc1>=0) & (isc2>=0) ) {
        double *elems1 = malloc( *(self->Csur->comsizes+isc1) * sizeof(double));
        k2 = subcommuniter_exchangeN(self->Csur, isc1, isc2, elems1);
        PyObject *linha = PyList_New(k2);
        for (j=0; j<k2; j++) {
            PyObject *num = Py_BuildValue("d", *(elems1 + j));
            PyList_SetItem(linha, j, num);
        }
        free(elems1);
        return linha;
    }
    return Py_BuildValue("[]");
}




static PyObject *Surpriser_stepper0(Surprise *self, PyObject *args, PyObject *kwds) {
    int k1, k2;
    int subcoms=1;
    static char *kwlist[] = {"subcoms", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|i", kwlist, &subcoms))
        return 0;
    
    if (subcoms) {
        stepper0(self->Csur, &k1, &k2);
    } else {
        stepper0nsc(self->Csur, &k1);
        k2 = 0;
    }
    return Py_BuildValue("ii", k1, k2);
}






static PyObject *Surpriser_stepper(Surprise *self, PyObject *args, PyObject *kwds) {
    /* calculates the clustering coefficents */
    int k1, k2, k3, k4, k5, k6;
    int sub=1, type=1;

    static char *kwlist[] = {"ord", "subcoms", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|ii", kwlist, &type, &sub))
        return 0;

    if (type==1) {
        if (sub) {
            stepperD(self->Csur, &k1, &k2, &k3, &k4, &k5);
        } else {
            stepperD2(self->Csur, &k1, &k2, &k3);
        }
    } else if (type==2) {
        if (sub) {
            stepper1(self->Csur, &k1, &k2, &k3, &k4, &k5, &k6);
        } else {
            stepper3(self->Csur, &k1, &k2, &k3);
        }
    } else if (type==3) {
        if (sub) {
            stepper5(self->Csur, &k1, &k2, &k3, &k4, &k5, &k6);
        } else {
            stepper6(self->Csur, &k1, &k2, &k3);
        }
    } else {
        if (sub) {
            stepper2(self->Csur, &k1, &k2, &k3, &k4, &k5, &k6);
        } else {
            stepper4(self->Csur, &k1, &k2, &k3);
        }
    }
    
    self->K = self->Csur->K;
    self->nl = self->Csur->nl;
    self->M = self->Csur->M;
    self->F = self->Csur->F;
    self->Nc = self->Csur->Nc;
    self->p = self->Csur->p;
    self->surprise = self->Csur->surprise;
    if (sub) {
        return Py_BuildValue("iiiii", k1, k2, k3, k4, k5); // removed k6 from here
    } else {
        return Py_BuildValue("iiiii", k1, k2, k3, 0, 0);
    }
}




static PyObject *Surpriser_subcommuniter(Surprise *self, PyObject *args, PyObject *kwds) {
    int res=0, ii;
    int N=1, ic=-1, iex=-1;
    /* Parse the input  */
    static char *kwlist[] = {"ic", "N", "iex", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iii", kwlist, &ic, &N, &iex))
        return 0;

    if (N==0) {
        res = subcommunited(self->Csur, ic, iex);
    } else if (N>1) {
        for (ii=0; ii<N; ii++) {
            ic = self->Csur->Nc * drand();
            res += subcommuniter(self->Csur, ic);
        }
    } else {
        if (ic<0) {ic = self->Csur->Nc * drand();}
        res = subcommuniter(self->Csur, ic);
    }
    self->K = self->Csur->K;
    self->nl = self->Csur->nl;
    self->M = self->Csur->M;
    self->F = self->Csur->F;
    self->Nc = self->Csur->Nc;
    self->p = self->Csur->p;
    self->surprise = self->Csur->surprise;
    return Py_BuildValue("i", res);
}




static PyObject *Surpriser_subcommunity_exchanger(Surprise *self, PyObject *args, PyObject *kwds) {
    int ic1=-1, ic2=-1, iex=-1, N=1, bfa=0;
    int res=0, ii;
    int kk;
    /* Parse the input  */
    static char *kwlist[] = {"ic1", "ic2", "N", "iex", "BfA", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iiiii", kwlist, &ic1, &ic2, &N, &iex, &bfa))
        return 0;
    
    if (bfa) {
        if (N>1) {
            for (ii=0; ii<N; ii++) {
                ic1 = self->Csur->Nc * drand();
                res += subcommuniter_exchange(self->Csur, ic1);
            }
        } else {
            if (ic1<0) {ic1 = self->Csur->Nc * drand();}
            res = subcommuniter_exchange(self->Csur, ic1);
        }
    } else if (N==0) {
        if (ic1<0) {ic1 = self->Csur->Nc * drand();}
        if (ic2<0) {ic2 = self->Csur->Nc * drand();}
        while ((ic1==ic2)&(self->Csur->Nc>1)) {ic2 = self->Csur->Nc * drand();}
        if (iex<0) {iex=0;}
        res = subcommuniter_exchanged(self->Csur, ic1, ic2, iex);
    } else if (N>1) {
        for (kk=0; kk<N; kk++) {
            ic1 = self->Csur->Nc * drand();
            ic2 = self->Csur->Nc * drand();
            while ((ic1==ic2)&(self->Csur->Nc>1)) {ic2 = self->Csur->Nc * drand();}
            res += subcommuniter_exchange2(self->Csur, ic1, ic2);
        }
    } else {
        if (ic1<0) {ic1 = self->Csur->Nc * drand();}
        if (ic2<0) {ic2 = self->Csur->Nc * drand();}
        while ((ic1==ic2)&(self->Csur->Nc>1)) {ic2 = self->Csur->Nc * drand();}
        res = subcommuniter_exchange2(self->Csur, ic1, ic2);
    }
    
    self->K = self->Csur->K;
    self->nl = self->Csur->nl;
    self->M = self->Csur->M;
    self->F = self->Csur->F;
    self->Nc = self->Csur->Nc;
    self->p = self->Csur->p;
    self->surprise = self->Csur->surprise;
    return Py_BuildValue("i", res);
}





static PyObject *Surpriser_subcommunity(Surprise *self, PyObject *args) {
    int i, j, cs;
    /* Parse the input  */
    if (!PyArg_ParseTuple(args, "i", &i))
        return 0;
    
    if (i>=self->Csur->Nc) {return Py_BuildValue("i", 0);}
    Surpriser *ssur=malloc(sizeof(Surpriser));
    subcommunity(self->Csur, i, ssur);
    
    PyObject *Matr = PyList_New(ssur->K);
    for (i=0; i<ssur->K; i++) {
        PyObject *linha = PyList_New(ssur->K);
        for (j=0; j<ssur->K; j++) {
            PyObject *num = Py_BuildValue("i", *(ssur->matr + i*ssur->K + j));
            PyList_SetItem(linha, j, num);
        }
        PyList_SetItem(Matr, i, linha);
    }
    PyObject *Coms = PyList_New(ssur->Nc);
    for (i=0; i<ssur->Nc; i++) {
        cs = *(ssur->comsizes + i);
        PyObject *linha = PyList_New(cs);
        for (j=0; j<cs; j++) {
            PyObject *num = Py_BuildValue("i", *(*(ssur->communities + i) + j));
            PyList_SetItem(linha, j, num);
        }
        PyList_SetItem(Coms, i, linha);
    }
    
    PyObject *PySur = PyObject_CallObject((PyObject *) &SurpriserType, Py_BuildValue("(O,O)", Matr, Coms));
    
    Py_DECREF(Matr);
    Py_DECREF(Coms);
    clear_surp(ssur);
    free(ssur);
    return Py_BuildValue("O", PySur);
}





static PyObject *Surpriser_merger_an(Surprise *self, PyObject *args, PyObject *kwds) {
    int ic1=-1, ic2=-1, N=1, res=0, ii;
    double temp=1.;

    // Parse the input  
    static char *kwlist[] = {"ic1", "ic2", "N", "T", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iiid", kwlist, &ic1, &ic2, &N, &temp))
        return 0;
    if ((ic1>=self->Csur->Nc)|(ic2>=self->Csur->Nc)|(self->Csur->Nc==1)) {return Py_BuildValue("i", res);}
    if (N>1) {
        for (ii=0; ii<N; ii++) {
            ic1 = self->Csur->Nc * drand();
            ic2 = self->Csur->Nc * drand();
            while (ic1==ic2) {ic2 = self->Csur->Nc * drand();}
            res += merger_an(self->Csur, ic1, ic2, temp);
        }
    } else if (N==1) {
        if (ic1<0) {ic1 = self->Csur->Nc * drand();}
        if (ic2<0) {ic2 = self->Csur->Nc * drand();}
        while (ic1==ic2) {ic2 = self->Csur->Nc * drand();}
        res = merger_an(self->Csur, ic1, ic2, temp);
    }
    self->K = self->Csur->K;
    self->nl = self->Csur->nl;
    self->M = self->Csur->M;
    self->F = self->Csur->F;
    self->Nc = self->Csur->Nc;
    self->p = self->Csur->p;
    self->surprise = self->Csur->surprise;
    return Py_BuildValue("i", res);
}



static PyObject *Surpriser_exchanger_an(Surprise *self, PyObject *args, PyObject *kwds) {
    int ic1=-1, ic2=-1, N=1, res=0, ii;
    double temp=1.;

    // Parse the input  
    static char *kwlist[] = {"ic1", "ic2", "N", "T", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iiid", kwlist, &ic1, &ic2, &N, &temp))
        return 0;
    if ((ic1>=self->Csur->Nc)|(ic2>=self->Csur->Nc)|(self->Nc==1)) {return Py_BuildValue("i", res);}
    if (N>1) {
        for (ii=0; ii<N; ii++) {
            ic1 = self->Csur->Nc * drand();
            ic2 = self->Csur->Nc * drand();
            while (ic1==ic2) {ic2 = self->Csur->Nc * drand();}
            res += exchanger_an(self->Csur, ic1, ic2, temp);
        }
    } else if (N==1) {
        if (ic1<0) {ic1 = self->Csur->Nc * drand();}
        if (ic2<0) {ic2 = self->Csur->Nc * drand();}
        while (ic1==ic2) {ic2 = self->Csur->Nc * drand();}
        res = exchanger_an(self->Csur, ic1, ic2, temp);
    }
    self->K = self->Csur->K;
    self->nl = self->Csur->nl;
    self->M = self->Csur->M;
    self->F = self->Csur->F;
    self->Nc = self->Csur->Nc;
    self->p = self->Csur->p;
    self->surprise = self->Csur->surprise;
    return Py_BuildValue("i", res);
}


static PyObject *Surpriser_extractor_an(Surprise *self, PyObject *args, PyObject *kwds) {
    int ic1=-1, N=1, res=0, ii;
    double temp=1.;

    // Parse the input  
    static char *kwlist[] = {"ic1", "N", "T", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iid", kwlist, &ic1, &N, &temp))
        return 0;
    if (ic1>=self->Csur->Nc) {return Py_BuildValue("i", res);}
    if (N>1) {
        for (ii=0; ii<N; ii++) {
            ic1 = self->Csur->Nc * drand();
            res += extractor_an(self->Csur, ic1, temp);
        }
    } else if (N==1) {
        if (ic1<0) {ic1 = self->Csur->Nc * drand();}
        res = extractor_an(self->Csur, ic1, temp);
    }
    self->K = self->Csur->K;
    self->nl = self->Csur->nl;
    self->M = self->Csur->M;
    self->F = self->Csur->F;
    self->Nc = self->Csur->Nc;
    self->p = self->Csur->p;
    self->surprise = self->Csur->surprise;
    return Py_BuildValue("i", res);
}




static PyObject *Surpriser_subcommuniter_an(Surprise *self, PyObject *args, PyObject *kwds) {
    int i=-1, N=1, res=0, ii;
    double temp=1.;
    /* Parse the input  */
    static char *kwlist[] = {"isc", "N", "T", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iid", kwlist, &i, &N, &temp))
        return 0;

    if (i>=self->Csur->Nc) {return Py_BuildValue("i", 0);}
    
    if (N>1) {
        for (ii=0; ii<N; ii++) {
            i = self->Csur->Nc * drand();
            res += subcommuniter_an(self->Csur, i, temp);
        }
    } else if (N==1) {
        if (i<0) {i = self->Csur->Nc * drand();}
        res = subcommuniter_an(self->Csur, i, temp);
    }
    
    if (res>0) {
        self->K = self->Csur->K;
        self->nl = self->Csur->nl;
        self->M = self->Csur->M;
        self->F = self->Csur->F;
        self->Nc = self->Csur->Nc;
        self->p = self->Csur->p;
        self->surprise = self->Csur->surprise;
    }
    return Py_BuildValue("i", res);
}


static PyObject *Surpriser_subcommunity_exchanger_an(Surprise *self, PyObject *args, PyObject *kwds) {
    int i=-1, N=1, res=0, ii;
    double temp=1.;
    /* Parse the input  */
    static char *kwlist[] = {"isc", "N", "T", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iid", kwlist, &i, &N, &temp))
        return 0;
    
    if ((i>=self->Csur->Nc)|(self->Nc==1)) {return Py_BuildValue("i", 0);}
    
    if (N>1) {
        for (ii=0; ii<N; ii++) {
            i = self->Csur->Nc * drand();
            res += subcommuniter_exchange_an(self->Csur, i, temp);
        }
    } else if (N==1) {
        if (i<0) {i = self->Csur->Nc * drand();}
        res = subcommuniter_exchange_an(self->Csur, i, temp);
    }
    
    if (res>0) {
        self->K = self->Csur->K;
        self->nl = self->Csur->nl;
        self->M = self->Csur->M;
        self->F = self->Csur->F;
        self->Nc = self->Csur->Nc;
        self->p = self->Csur->p;
        self->surprise = self->Csur->surprise;
    }
    return Py_BuildValue("i", res);
}













// *******************************************
/*              Functions                   */
// *******************************************

static PyObject *Function_fact(PyObject *self, PyObject *args) {   
    double res;
    int N;

    // Parse the input
    if (!PyArg_ParseTuple(args, "i", &N))
        return 0;
    
    res = fact(N);
    return Py_BuildValue("d", res);
}

static PyObject *Function_gammas(PyObject *self, PyObject *args) {   
    double res;
    int N, M;

    // Parse the input
    if (!PyArg_ParseTuple(args, "ii", &M, &N))
        return 0;
    
    res = gammas(M, N);
    return Py_BuildValue("d", res);
}

static PyObject *Function_surprise(PyObject *self, PyObject *args) {   
    double res;
    int M, F, n, p;

    // Parse the input
    if (!PyArg_ParseTuple(args, "iiii", &M, &F, &n, &p))
        return 0;
    
    res = surprise(M, F, n, p);
    return Py_BuildValue("d", res);
}

static PyObject *Function_compare(PyObject *self, PyObject *args) {   
    double VI;
    PyObject *Pyli1, *Pyli2;
    int K, i;
    int *li1, *li2;
    int n1=0, n2=0, co1, co2;
    /* Parse the input  */
    if (!PyArg_ParseTuple(args, "OO", &Pyli1, &Pyli2))
        return 0;
    K = (int) PyList_Size(Pyli1);
    if (K!=(int) PyList_Size(Pyli2)) {
        printf("Warning: Lists should be of the same size!\n");
        return Py_BuildValue("");
    }
    /* Reads the Matrix */
    li1 = malloc(sizeof(int)*K);
    li2 = malloc(sizeof(int)*K);
    for (i=0; i<K; i++) {
        co1 = (int) PyLong_AsSsize_t(PyList_GetItem(Pyli1, i));
        co2 = (int) PyLong_AsSsize_t(PyList_GetItem(Pyli2, i));
        *(li1 + i) = co1;
        *(li2 + i) = co2;
        if (co1>n1) {n1 = co1;}
        if (co2>n2) {n2 = co2;}
    }
    
    VI = compare(li1, li2, n1+1, n2+1, K);
    free(li1);
    free(li2);
    return Py_BuildValue("d", VI);
}

static PyObject *Function_embedding(PyObject *self, PyObject *args, PyObject *kwds) {
    int i, j, N, Nc;
    double eps=1.e-10, lamb=2., gamma=-1., adj=0.05, dlim=.1;
    PyObject *Matr;
    PyObject *Coords = Py_BuildValue("[]");
    /* Parse the input  */
    static char *kwlist[] = {"matr", "coords", "gamma", "dlim", "lamb", "adj", "eps", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|Oddddd", kwlist, &Matr, &Coords, &gamma, &dlim, &lamb, &adj, &eps))
        return 0;
    N = (int) PyList_Size(Matr);
    double *cords = malloc(2*N*sizeof(double));
    /* Reads the Matrix */
    double *y = malloc(sizeof(double)*N*N);
    for (i=0; i<N; i++) {
        PyObject *linha = PyList_GetItem(Matr,i);
        for (j=0; j<N; j++) {
            *(y + i*N + j) = (double) PyFloat_AsDouble(PyList_GetItem(linha,j));
        }
    }
    Nc = (int) PyList_Size(Coords);
    if (Nc==0) {
        double mod, ang;
        for (i=0; i<N; i++) {
            mod = 10.*drand();
            ang = 2*3.141592654*drand();
            *(cords + i*2)   = mod*cos(ang);
            *(cords + i*2+1) = mod*sin(ang);
        }
    } else {
        for (i=0; i<N; i++) {
            PyObject *linha = PyList_GetItem(Coords,i);
            *(cords + i*2)   = (double) PyFloat_AsDouble(PyList_GetItem(linha,0));
            *(cords + i*2+1) = (double) PyFloat_AsDouble(PyList_GetItem(linha,1));
        }
    }
    
    minCoords(y, cords, N, gamma, dlim, lamb, adj, eps);
    
    PyObject *resp = PyList_New(N);
    for (i=0;i<N;i++) {
        PyObject *linea = PyList_New(2);
        PyList_SetItem(linea, 0, PyFloat_FromDouble( *(cords+2*i) ) );
        PyList_SetItem(linea, 1, PyFloat_FromDouble( *(cords+2*i+1) ));
        PyList_SetItem(resp, i, linea);
    }

    free(y);
    free(cords);
    return Py_BuildValue("O", resp);
}


static PyObject *Function_ChiGrad(PyObject *self, PyObject *args, PyObject *kwds) {
    int i, j, N=0;
    double gamma=-1., dlim=.1;
    PyObject *Matr, *Coords;
    /* Parse the input  */
    static char *kwlist[] = {"matr", "coords", "gamma", "N", "dlim", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OO|did", kwlist, &Matr, &Coords, &gamma, &N, &dlim))
        return 0;
    if (~N) {
        N = (int) PyList_Size(Matr);
    }
    double *cords = malloc(2*N*sizeof(double));
    /* Reads the Matrix */
    double *y = malloc(sizeof(double)*N*N);
    for (i=0; i<N; i++) {
        PyObject *linha = PyList_GetItem(Matr,i);
        for (j=0; j<N; j++) {
            *(y + i*N + j) = (double) PyFloat_AsDouble(PyList_GetItem(linha,j));
        }
    }
    for (i=0; i<N; i++) {
        PyObject *linha = PyList_GetItem(Coords,i);
        *(cords + i*2)   = (double) PyFloat_AsDouble(PyList_GetItem(linha,0));
        *(cords + i*2+1) = (double) PyFloat_AsDouble(PyList_GetItem(linha,1));
    }

    double *grads= malloc(2*N*sizeof(double));
    double tot=0, chi;
    chi = chigrad(y, cords, N, gamma, dlim, grads, &tot);
    
    PyObject *resp = PyList_New(N);
    for (i=0;i<N;i++) {
        PyObject *linea = PyList_New(2);
        PyList_SetItem(linea, 0, PyFloat_FromDouble( *(grads+2*i) ) );
        PyList_SetItem(linea, 1, PyFloat_FromDouble( *(grads+2*i+1) ));
        PyList_SetItem(resp, i, linea);
    }

    free(y);
    free(cords);
    free(grads);
    return Py_BuildValue("dOd", chi, resp, tot);
}

