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

typedef struct _SurpriserTag {
    int K;
    int M;
    int F;
    int nl;
    int p;
    int *matr;
    int *partition;
    int *kis;
    int **links;
    int **communities;
    int *comsizes;
    int Nc;
    double surprise;
} Surpriser;
////////////////////
/////////////////
// Functions
//////////////////
////////////////////
void reseed(void); // Stores things
double fact(int n); // returns the logarithm of the factorial
double gammas(int m, int n); // return the logarithm of the combination of m elements n by n.
double surprise(int M, int F, int n, int p); // evaluates the surprise
int isin(int *lista, int N, int ele); // says if element ele is in pointer lista
double compare(int *lista1, int *lista2, int n1, int n2, int K); // Variation of information between lists
/////////////////
///////////////
// Surpriser
//////////////
/////////////////
//
// stuff
//
void generate_supriser(int *matr, int K, int **communities, int *comsizes, Surpriser *sur); // Creates the surpriser object from matrix
void clear_surp(Surpriser *sur); // Clears memory (deletes the object)
int intralinks(Surpriser *sur, int com); // number of internal links in a community
int intralinks_m(int *matr, int *community, int cs, int N, int *extra); // number of internal links in a community
void show_surpriser(Surpriser *sur); // Shows information
void show_communities(Surpriser *sur); // Shows communities
void partition(Surpriser *sur, int *par_ret); // Creates the partition list
//
// Basic algo
//
int merger(Surpriser *sur, int ic1, int ic2); // Tries to merge communities
int merger2(Surpriser *sur, int ic1); // Merges a community to its best match (ordered)
int merger3(Surpriser *sur, int ic1); // Merges a community to its best match (not ordered)
void mergerN(Surpriser *sur, int ic1, double *coms); // Returns all possible changes in surprise
int extractor(Surpriser *sur, int ic1); // Tries to extract an element from the community
int extractor2(Surpriser *sur, int ic1); // Tries to extract an element from the community the best
void extractorN(Surpriser *sur, int ic1, double *elems); // Returns all possible changes in surprise
int exchanger1(Surpriser *sur, int ic1, int ic2, int ii); // Tries to exchange an element between two communities
int exchanger0(Surpriser *sur, int ic1); // Tries to exchange an element between a community if no chenge in s. Returns ic2
int exchanger(Surpriser *sur, int ic1, int ic2); // Tries to exchange an element between two communities
int exchanger2(Surpriser *sur, int ic1); // Tries to exchange an element between a community and its best match (ordered)
int exchanger3(Surpriser *sur, int ic1); // Tries to exchange an element between a community and its best match (not ordered)
void exchangerN(Surpriser *sur, int ic1, int ic2, double *elems); // Returns all possible changes in surprise
int merge(Surpriser *sur, int ic1, int ic2); // Merges two communities
int extract(Surpriser *sur, int ic1, int ii); // Extracts an element from the community
int exchange(Surpriser *sur, int ic1, int ic2, int ii); // Exchanges an element between two communities
void stepper1(Surpriser *sur, int *k1, int *k2, int *k3, int *k4, int *k5, int *k6); // Tries all merges, exchanges and extractions possible loop per com
void stepper2(Surpriser *sur, int *k1, int *k2, int *k3, int *k4, int *k5, int *k6); // Tries all merges, exchanges and extractions possible exaustion each
void stepper3(Surpriser *sur, int *k1, int *k2, int *k3); // Tries all merges, exchanges and extractions possible like 1, no subcoms
void stepper4(Surpriser *sur, int *k1, int *k2, int *k3); // Tries all merges, exchanges and extractions possible like 2, no subcoms
void stepper5(Surpriser *sur, int *k1, int *k2, int *k3, int *k4, int *k5, int *k6); // Tries all merges, exchanges and extractions possible exaustion each
void stepper6(Surpriser *sur, int *k1, int *k2, int *k3); // Tries all merges, exchanges and extractions possible like 5, no subcoms
void stepper0(Surpriser *sur, int *k1, int *k2); // changes that do not affect surprise value
void stepper0nsc(Surpriser *sur, int *k1); // changes that do not affect surprise value
void stepperD(Surpriser *sur, int *k1, int *k2, int *k3, int *k4, int *k5); // uses the graph structure
void stepperD2(Surpriser *sur, int *k1, int *k2, int *k3); // uses the graph structure
//
// Subcommunites and slicers
//
int subcommuniter(Surpriser *sur, int ic); // Finds communities inside communities and tries to extract them.
int subcommuniterN(Surpriser *sur, int ic, double *elems); // Returns all possible changes in surprise
int subcommunited(Surpriser *sur, int ic, int iex); // Finds communities inside communities and tries to extracts a given one.
int subcommuniter_exchange(Surpriser *sur, int ic); // Finds communities inside communities and tries to exchange them.
int subcommuniter_exchange0(Surpriser *sur, int ic); // Finds communities inside communities exchanges if no ds=0
int subcommuniter_exchange2(Surpriser *sur, int ic, int mm); // Finds communities inside communities and tries to exchange them to a given one.
int subcommuniter_exchange3(Surpriser *sur, int ic); // Finds communities inside communities and tries to exchange the first.
int subcommuniter_exchanged(Surpriser *sur, int ic, int mm, int iex); // Finds communities inside communities and exchange a given one.
int subcommuniter_exchangeN(Surpriser *sur, int ic, int mm, double *subc); // Returns all possible changes in surprise
//int subcommuniter_merger(Surpriser *sur, int ic1, int ic2); // Finds communities inside communities and tries to extract them to a given one.
int subcommuniter_ret(Surpriser *sur, int ic, Surpriser *ssur); // Finds communities inside communities, tries to extract them and stores the new pointer
void subcommunity(Surpriser *sur, int ic, Surpriser *ssur); // Finds communities inside communities and stores the new pointer
//
// Anealing
//
int megastep(Surpriser *sur, double T, int K); // montecarlo step
int megastepNSC(Surpriser *sur, double T, int K); // montecarlo step without subcoms
int merger_an(Surpriser *sur, int ic1, int ic2, double temp); // Tries to merge communities
int exchanger_an(Surpriser *sur, int ic1, int ic2, double temp); // Tries to exchange an element between two communities
int extractor_an(Surpriser *sur, int ic1, double temp); // Tries to extract an element from the community
int subcommuniter_an(Surpriser *sur, int ic, double temp); // Finds communities inside communities and tries to extract them.
int subcommuniter_exchange_an(Surpriser *sur, int ic, double temp); // Finds communities inside communities and tries to extract them.
//
// Embedding
//
double dist(double *p1, double *p2);
double chigrad(double *matr, double *coords, int N, double gamma, double dlim, double *grads, double *tot);
void minCoords(double *matr, double *coords, int N, double gamma, double dlim, double lambda, double adj, double eps);
