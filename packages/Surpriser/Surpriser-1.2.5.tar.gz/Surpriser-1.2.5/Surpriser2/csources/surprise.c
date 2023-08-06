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
#include <string.h>
#include "surprise.h"
#include "randoms.h"

/////////////////////
// Functions and stuff
/////////////////////

double *list_facts = NULL;
int *Nll = NULL;

void reseed(void) {
    if (!Nll) {
        int ii;
        double accu=0.;
        Nll = malloc(sizeof(int));
        *Nll = 10000000;
        list_facts = malloc(sizeof(double)* *Nll);
        *list_facts = 0.;
        for (ii=1; ii<*Nll; ii++) {
            accu += log(1.*ii);
            *(list_facts + ii) = accu;
        }
    } else {
        double accu;
        double *npointer;
        int Nold = *Nll;
        int ii;
        accu = *(list_facts + Nold - 1);
        *Nll += 10000000;
        npointer = malloc(sizeof(double)* *Nll);
        for (ii=0; ii<Nold; ii++) {
            *(npointer + ii) = *(list_facts + ii);
        }
        for (ii=Nold; ii<*Nll; ii++) {
            accu += log(1.*ii);
            *(npointer + ii) = accu;
        }
        free(list_facts);
        list_facts = malloc(sizeof(double)* *Nll);
        for (ii=0; ii<*Nll; ii++) {
            *(list_facts + ii) = *(npointer + ii);
        }
        free(npointer);
    }
}

int isin(int *lista, int N, int ele) {
    int ii;
    for (ii=0; ii<N; ii++) {
        if (*(lista + ii) == ele) {return 1;}
    }
    return 0;
}


double fact(int n) {
    if (n<*Nll) {
        return *(list_facts + n);
    } else {
        while (*Nll<=n) { reseed(); }
        return *(list_facts + n);
    }
}



double gammas(int m, int n) {
    double logc;
    logc = fact(m) - fact(n) - fact(m - n);
    return logc;
}


double surprise(int M, int F, int n, int p) {
    double maa, bla, surp, sur=0.;
    int jj, fin;
    if (M==0) {return sur;}
    if (M<n) {
        fin = M+1;
    } else {
        fin = n+1;
    }
    jj = p;
    bla = gammas(M, jj) + gammas(F-M, n-jj) - gammas(F, n);
    maa = bla;
    for (jj=p+1; jj<fin; jj++) {
        bla = gammas(M, jj) + gammas(F-M, n-jj) - gammas(F, n);
        sur += exp(bla-maa);
    }
    surp = -(log(1.+sur)+maa);
    return surp;
}


double compare(int *lista1, int *lista2, int n1, int n2, int K) {
    double *p1, *p2, num, *p12;
    double H1=0., H2=0.;
    double I=0., pp1, pp2, pp12;
    int ii, jj, kk, i1, i2;
    
    p1 = calloc(n1, sizeof(double));
    for (ii=0; ii<K; ii++) {
        *(p1 + *(lista1 + ii)) += 1./K;
    }
    for (ii=0; ii<n1; ii++) {
        num = *(p1 + ii);
        H1 -= num*log(num);
    }
    p2 = calloc(n2, sizeof(double));
    for (ii=0; ii<K; ii++) {
        *(p2 + *(lista2 + ii)) += 1./K;
    }
    for (ii=0; ii<n2; ii++) {
        num = *(p2 + ii);
        H2 -= num*log(num);
    }
    p12 = calloc(n1*n2, sizeof(double));
            for (kk=0; kk<K; kk++) {
                i1 = *(lista1 + kk);
                i2 = *(lista2 + kk);
                    *(p12 + i1*n2 + i2) += 1./K;
            }
    for (ii=0; ii<n1; ii++) {
        pp1 = *(p1 + ii);
        for (jj=0; jj<n2; jj++) {
            pp2 = *(p2 + jj);
            pp12 = *(p12 + ii*n2 + jj);
            if (pp12>0.) {I += pp12*log(pp12/(pp1*pp2));}
        }
    }
    free(p1);
    free(p2);
    free(p12);
    return H1 + H2 - 2.*I;
}



/////////////////////
// Surpriser stuff
/////////////////////

void generate_supriser(int *matr, int K, int **communities, int *comsizes, Surpriser *sur) {
    int ii, jj, cs, node, ki;
    int M=0, p=0, Nc=0, nl=0, ele;
    
    sur->K = K;
    sur->F = K*(K-1)/2;
    sur->matr = calloc(K*K, sizeof(int));
    sur->partition = calloc(K, sizeof(int)); //
    sur->kis = calloc(K, sizeof(int)); //
    sur->links = malloc(K*sizeof(int*)); //
    sur->comsizes = calloc(K, sizeof(int));
    sur->communities = malloc(K*sizeof(int*));
    // reads M matrix, and kis
    for (ii=0; ii<K; ii++) {
        ki = 0;
        for (jj=0; jj<K;jj++) {
            ele = *(matr + jj*K + ii);
            *(sur->matr + jj*K + ii) = ele;
            nl += ele;
            ki += ele;
        }
        *(sur->kis+ii) = ki; //
        *(sur->links+ii) = malloc(ki*sizeof(int)); //
        ki = 0;
        for (jj=0; jj<K;jj++) {
            ele = *(matr + jj*K + ii);
            if (ele) {
                *(*(sur->links+ii)+ki) = jj; //
                ki++;
            }
        }
    }
    // communities
    if (!communities) {
        for (ii=0; ii<K;ii++) {
            *(sur->comsizes+ii) = 1;
            *(sur->communities+ii) = calloc(K, sizeof(int));
            *(*(sur->communities+ii)) = ii;
            *(sur->partition+ii) = ii; //
        }
        sur->M = M;
        sur->p = p;
        sur->Nc = K;
    } else {
        for (ii=0; ii<K;ii++) {
            cs = *(comsizes+ii);
            if (cs>0) {Nc++;}
            *(sur->comsizes+ii) = cs;
            *(sur->communities+ii) = calloc(K, sizeof(int));
            for (jj=0;jj<cs;jj++) {
                node = *(*(communities+ii)+jj);
                *(*(sur->communities+ii)+jj) = node;
                *(sur->partition+node) = ii; //
            }
            M += cs*(cs-1)/2;
            p += intralinks(sur, ii);            
        }
        sur->M = M;
        sur->p = p;
        sur->Nc = Nc;
    }
    nl /= 2;
    sur->nl = nl;
    sur->surprise = surprise(sur->M, sur->F, sur->nl, sur->p);
}


void clear_surp(Surpriser *sur) {
    int ii;
    for (ii=0; ii<sur->K; ii++) {
        free(*(sur->communities + ii));
    }
    free(sur->communities);
    for (ii=0; ii<sur->K; ii++) {
        free(*(sur->links + ii));
    }
    free(sur->links);
    free(sur->comsizes);
    free(sur->kis);
    free(sur->partition);
    free(sur->matr);
}

int intralinks(Surpriser *sur, int com) {
    int ii, jj, cs;
    int links=0;
    cs = *(sur->comsizes+com);
    for (ii=0; ii<cs; ii++) {
        for (jj=ii+1; jj<cs; jj++) {
            links += *(sur->matr + *(*(sur->communities+com) + jj)*(sur->K) + *(*(sur->communities+com) + ii));
        }
    }
    return links;
}


int intralinks_m(int *matr, int *community, int cs, int N, int *extra) {
    int ii, jj, t1, t2;
    int links=0;
    *extra = 0;
    for (ii=0;ii<N;ii++) {
        t1 = isin(community, cs, ii);
        for (jj=ii+1;jj<N;jj++) {
            t2 = isin(community, cs, jj);
            if ( t1&t2 ) {
                links += *(matr + ii*N + jj);
            } else if (t1|t2) {
                *extra += *(matr + ii*N + jj);
            }
        }
    }
    return links;
}


void show_surpriser(Surpriser *sur){
    printf("< Graph/communities info :\n");
    printf("   Number of nodes      : %d\n", sur->K);
    printf("   Number of links      : %d (%d)\n", sur->nl, sur->F);
    printf("   Number of communities : %d\n", sur->Nc);
    printf("   Number of intralinks : %d (%d)\n", sur->p, sur->M);
    printf("   Surprise             : %f >\n", sur->surprise);
}


void show_communities(Surpriser *sur) {
    int ii, jj, cs;
    for (ii=0; ii<sur->Nc; ii++) {
        cs = *(sur->comsizes+ii);
        printf("community %d (size %d) : ", ii, cs);
        for (jj=0; jj<cs; jj++) {
            printf(" %d,", *(*(sur->communities + ii)+jj));
        }
        printf("\n");
    }
}


void partition(Surpriser *sur, int *par_ret) {
    int ii;
    for (ii=0; ii<sur->K; ii++) {
        *(par_ret + ii) = *(sur->partition+ii);
    }
    /* int ii, jj, cs, elem;
    for (ii=0; ii<sur->Nc; ii++) {
        cs = *(sur->comsizes+ii);
        for (jj=0; jj<cs; jj++) {
            elem = *(*(sur->communities + ii)+jj);
            *(par_ret + elem) = ii;
        }
    }*/
}



int merge(Surpriser *sur, int ic1, int ic2) {
    int cs1, cs2, lcs;
    int dM;//M1, M2, M3;
    int dp=0;
    int ii, jj, i1, i2;
    int toret=0;
    double nsurp;
    if (ic1==ic2) {return toret;}
    cs1 = *(sur->comsizes+ic1);
    cs2 = *(sur->comsizes+ic2);
    //M1 = cs1*(cs1-1)/2;
    //M2 = cs2*(cs2-1)/2;
    //M3 = (cs1+cs2)*(cs1+cs2-1)/2;
    dM = cs1*cs2;
    for (ii=0; ii<cs1; ii++) {
        i1 = *(*(sur->communities + ic1) + ii);
        for (jj=0; jj<cs2; jj++) {
            i2 = *(*(sur->communities + ic2) + jj);
            dp += *(sur->matr + i1* sur->K + i2);
        }
    }
    nsurp = surprise(sur->M+dM, sur->F, sur->nl, sur->p+dp);
    //if (nsurp > sur->surprise) {
        //printf("communities %d and %d being merged! \n", ic1, ic2);
        sur->surprise = nsurp;
        sur->M += dM;
        sur->p += dp;
        lcs = *(sur->comsizes + sur->Nc-1);
        if (ic1<ic2) {
            for (jj=0; jj<cs2; jj++) {
                i2 = *(*(sur->communities + ic2) + jj);
                *(sur->partition+i2) = ic1;
                *(*(sur->communities + ic1) + cs1 + jj) = i2;
                if (jj<lcs) {
                    i2 = *(*(sur->communities + sur->Nc-1) + jj);
                    if (ic2!=sur->Nc-1) {*(sur->partition+i2) = ic2;}
                    *(*(sur->communities + ic2) + jj) = i2;
                    *(*(sur->communities + sur->Nc-1) + jj) = 0;
                }
            }
            for (jj=cs2; jj<lcs; jj++) {
                i2 = *(*(sur->communities + sur->Nc-1) + jj);
                if (ic2!=sur->Nc-1) {*(sur->partition+i2) = ic2;}
                *(*(sur->communities + ic2) + jj) = i2;
                *(*(sur->communities + sur->Nc-1) + jj) = 0;
            }
            *(sur->comsizes + ic1) += cs2;
            *(sur->comsizes + ic2) = *(sur->comsizes + sur->Nc-1);
            *(sur->comsizes + sur->Nc-1) = 0;
        } else {
            for (jj=0; jj<cs1; jj++) {
                i1 = *(*(sur->communities + ic1) + jj);
                *(sur->partition+i1) = ic2;
                *(*(sur->communities + ic2) + cs2 + jj) = i1;
                if (jj<lcs) {
                    i2 = *(*(sur->communities + sur->Nc-1) + jj);
                    if (ic1!=sur->Nc-1) {*(sur->partition+i2) = ic1;}
                    *(*(sur->communities + ic1) + jj) = i2;
                    *(*(sur->communities + sur->Nc-1) + jj) = 0;
                }
            }
            for (jj=cs1; jj<lcs; jj++) {
                i2 = *(*(sur->communities + sur->Nc-1) + jj);
                if (ic1!=sur->Nc-1) {*(sur->partition+i2) = ic1;}
                *(*(sur->communities + ic1) + jj) = i2;
                *(*(sur->communities + sur->Nc-1) + jj) = 0;
            }
            *(sur->comsizes + ic2) += cs1;
            *(sur->comsizes + ic1) = *(sur->comsizes + sur->Nc-1);
            *(sur->comsizes + sur->Nc-1) = 0;
        }
        sur->Nc -= 1;
        toret = 1;
    //}
    return toret;
}




int merger(Surpriser *sur, int ic1, int ic2) {
    int cs1, cs2, lcs;
    int dM;//M1, M2, M3;
    int dp=0;
    int ii, jj, i1, i2;
    int toret=0;
    double nsurp;
    if (ic1==ic2) {return toret;}
    cs1 = *(sur->comsizes+ic1);
    cs2 = *(sur->comsizes+ic2);
    //M1 = cs1*(cs1-1)/2;
    //M2 = cs2*(cs2-1)/2;
    //M3 = (cs1+cs2)*(cs1+cs2-1)/2;
    dM = cs1*cs2;
    for (ii=0; ii<cs1; ii++) {
        i1 = *(*(sur->communities + ic1) + ii);
        for (jj=0; jj<cs2; jj++) {
            i2 = *(*(sur->communities + ic2) + jj);
            dp += *(sur->matr + i1* sur->K + i2);
        }
    }
    if (dp>0) {
    nsurp = surprise(sur->M+dM, sur->F, sur->nl, sur->p+dp);
    if (nsurp > sur->surprise) {
        //printf("communities %d and %d being merged! \n", ic1, ic2);
        sur->surprise = nsurp;
        sur->M += dM;
        sur->p += dp;
        lcs = *(sur->comsizes + sur->Nc-1);
        if (ic1<ic2) {
            for (jj=0; jj<cs2; jj++) {
                i2 = *(*(sur->communities + ic2) + jj);
                *(sur->partition+i2) = ic1;
                *(*(sur->communities + ic1) + cs1 + jj) = i2;
                if (jj<lcs) {
                    i2 = *(*(sur->communities + sur->Nc-1) + jj);
                    if (ic2!=sur->Nc-1) {*(sur->partition+i2) = ic2;}
                    *(*(sur->communities + ic2) + jj) = i2;
                    *(*(sur->communities + sur->Nc-1) + jj) = 0;
                }
            }
            for (jj=cs2; jj<lcs; jj++) {
                i2 = *(*(sur->communities + sur->Nc-1) + jj);
                if (ic2!=sur->Nc-1) {*(sur->partition+i2) = ic2;}
                *(*(sur->communities + ic2) + jj) = i2;
                *(*(sur->communities + sur->Nc-1) + jj) = 0;
            }
            *(sur->comsizes + ic1) += cs2;
            *(sur->comsizes + ic2) = *(sur->comsizes + sur->Nc-1);
            *(sur->comsizes + sur->Nc-1) = 0;
        } else {
            for (jj=0; jj<cs1; jj++) {
                i1 = *(*(sur->communities + ic1) + jj);
                *(sur->partition+i1) = ic2;
                *(*(sur->communities + ic2) + cs2 + jj) = i1;
                if (jj<lcs) {
                    i2 = *(*(sur->communities + sur->Nc-1) + jj);
                    if (ic1!=sur->Nc-1) {*(sur->partition+i2) = ic1;}
                    *(*(sur->communities + ic1) + jj) = i2;
                    *(*(sur->communities + sur->Nc-1) + jj) = 0;
                }
            }
            for (jj=cs1; jj<lcs; jj++) {
                i2 = *(*(sur->communities + sur->Nc-1) + jj);
                if (ic1!=sur->Nc-1) {*(sur->partition+i2) = ic1;}
                *(*(sur->communities + ic1) + jj) = i2;
                *(*(sur->communities + sur->Nc-1) + jj) = 0;
            }
            *(sur->comsizes + ic2) += cs1;
            *(sur->comsizes + ic1) = *(sur->comsizes + sur->Nc-1);
            *(sur->comsizes + sur->Nc-1) = 0;
        }
        sur->Nc -= 1;
        toret = 1;
    }}
    return toret;
}


int merger2(Surpriser *sur, int ic1) {
    int cs1, cs2, ic2, lcs;
    int dM;//M1, M2, M3;
    int dp=0;
    int ii, jj, i1, i2;
    int toret=0, Mbest=0, dpbest=0, icbest=0, cs2best=0;
    double nsurp, surpbest=0;
    cs1 = *(sur->comsizes+ic1);
    //M1 = cs1*(cs1-1)/2;
    for (ic2=ic1+1; ic2<sur->Nc; ic2++) {
        cs2 = *(sur->comsizes+ic2);
        //M2 = cs2*(cs2-1)/2;
        //M3 = (cs1+cs2)*(cs1+cs2-1)/2;
        dM = cs1*cs2;
        dp = 0;
        if (ic2!=ic1) {
            for (ii=0; ii<cs1; ii++) {
                i1 = *(*(sur->communities + ic1) + ii);
                for (jj=0; jj<cs2; jj++) {
                    i2 = *(*(sur->communities + ic2) + jj);
                    dp += *(sur->matr + i1* sur->K + i2);
                }
            }
            if (dp>0) {
            nsurp = surprise(sur->M+dM, sur->F, sur->nl, sur->p+dp);
            if (nsurp>surpbest) {
                surpbest = nsurp;
                dpbest = dp;
                Mbest = dM;
                icbest = ic2;
                cs2best = cs2;
            }}
        }
    }
    if (surpbest > sur->surprise) {
        nsurp = surpbest;
        dp = dpbest;
        ic2 = icbest;
        cs2 = cs2best;
        //printf("communities %d and %d being merged! \n", ic1, ic2);
        sur->surprise = nsurp;
        sur->M += Mbest;
        sur->p += dp;
        lcs = *(sur->comsizes + sur->Nc-1);
        if (ic1<ic2) {
            for (jj=0; jj<cs2; jj++) {
                i2 = *(*(sur->communities + ic2) + jj);
                *(sur->partition+i2) = ic1;
                *(*(sur->communities + ic1) + cs1 + jj) = i2;
                if (jj<lcs) {
                    i2 = *(*(sur->communities + sur->Nc-1) + jj);
                    if (ic2!=sur->Nc-1) {*(sur->partition+i2) = ic2;}
                    *(*(sur->communities + ic2) + jj) = i2;
                    *(*(sur->communities + sur->Nc-1) + jj) = 0;
                }
            }
            for (jj=cs2; jj<lcs; jj++) {
                i2 = *(*(sur->communities + sur->Nc-1) + jj);
                if (ic2!=sur->Nc-1) {*(sur->partition+i2) = ic2;}
                *(*(sur->communities + ic2) + jj) = i2;
                *(*(sur->communities + sur->Nc-1) + jj) = 0;
            }
            *(sur->comsizes + ic1) += cs2;
            *(sur->comsizes + ic2) = *(sur->comsizes + sur->Nc-1);
            *(sur->comsizes + sur->Nc-1) = 0;
        } else {
            for (jj=0; jj<cs1; jj++) {
                i1 = *(*(sur->communities + ic1) + jj);
                *(sur->partition+i1) = ic2;
                *(*(sur->communities + ic2) + cs2 + jj) = i1;
                if (jj<lcs) {
                    i2 = *(*(sur->communities + sur->Nc-1) + jj);
                    if (ic1!=sur->Nc-1) {*(sur->partition+i2) = ic1;}
                    *(*(sur->communities + ic1) + jj) = i2;
                    *(*(sur->communities + sur->Nc-1) + jj) = 0;
                }
            }
            for (jj=cs1; jj<lcs; jj++) {
                i2 = *(*(sur->communities + sur->Nc-1) + jj);
                if (ic1!=sur->Nc-1) {*(sur->partition+i2) = ic1;}
                *(*(sur->communities + ic1) + jj) = i2;
                *(*(sur->communities + sur->Nc-1) + jj) = 0;
            }
            *(sur->comsizes + ic2) += cs1;
            *(sur->comsizes + ic1) = *(sur->comsizes + sur->Nc-1);
            *(sur->comsizes + sur->Nc-1) = 0;
        }
        sur->Nc -= 1;
        toret = 1;
    }
    return toret;
}


int merger3(Surpriser *sur, int ic1) {
    int cs1, cs2, ic2, lcs;
    int dM;//M1, M2, M3;
    int dp=0;
    int ii, jj, i1, i2;
    int toret=0, Mbest=0, dpbest=0, icbest=0, cs2best=0;
    double nsurp, surpbest=0;
    if ((ic1<0)|(ic1>=sur->Nc)) {return toret;}
    cs1 = *(sur->comsizes+ic1);
    //M1 = cs1*(cs1-1)/2;
    for (ic2=0; ic2<sur->Nc; ic2++) {
        cs2 = *(sur->comsizes+ic2);
        //M2 = cs2*(cs2-1)/2;
        //M3 = (cs1+cs2)*(cs1+cs2-1)/2;
        dM = cs1*cs2;
        dp = 0;
        if (ic2!=ic1) {
            for (ii=0; ii<cs1; ii++) {
                i1 = *(*(sur->communities + ic1) + ii);
                for (jj=0; jj<cs2; jj++) {
                    i2 = *(*(sur->communities + ic2) + jj);
                    dp += *(sur->matr + i1* sur->K + i2);
                }
            }
            if (dp>0) {
            nsurp = surprise(sur->M+dM, sur->F, sur->nl, sur->p+dp);
            if (nsurp>surpbest) {
                surpbest = nsurp;
                dpbest = dp;
                Mbest = dM;
                icbest = ic2;
                cs2best = cs2;
            }}
        }
    }
    if (surpbest > sur->surprise) {
        nsurp = surpbest;
        dp = dpbest;
        ic2 = icbest;
        cs2 = cs2best;
        //printf("communities %d and %d being merged! \n", ic1, ic2);
        sur->surprise = nsurp;
        sur->M += Mbest;
        sur->p += dp;
        lcs = *(sur->comsizes + sur->Nc-1);
        if (ic1<ic2) {
            for (jj=0; jj<cs2; jj++) {
                i2 = *(*(sur->communities + ic2) + jj);
                *(sur->partition+i2) = ic1;
                *(*(sur->communities + ic1) + cs1 + jj) = i2;
                if (jj<lcs) {
                    i2 = *(*(sur->communities + sur->Nc-1) + jj);
                    if (ic2!=sur->Nc-1) {*(sur->partition+i2) = ic2;}
                    *(*(sur->communities + ic2) + jj) = i2;
                    *(*(sur->communities + sur->Nc-1) + jj) = 0;
                }
            }
            for (jj=cs2; jj<lcs; jj++) {
                i2 = *(*(sur->communities + sur->Nc-1) + jj);
                if (ic2!=sur->Nc-1) {*(sur->partition+i2) = ic2;}
                *(*(sur->communities + ic2) + jj) = i2;
                *(*(sur->communities + sur->Nc-1) + jj) = 0;
            }
            *(sur->comsizes + ic1) += cs2;
            *(sur->comsizes + ic2) = *(sur->comsizes + sur->Nc-1);
            *(sur->comsizes + sur->Nc-1) = 0;
        } else {
            for (jj=0; jj<cs1; jj++) {
                i1 = *(*(sur->communities + ic1) + jj);
                *(sur->partition+i1) = ic2;
                *(*(sur->communities + ic2) + cs2 + jj) = i1;
                if (jj<lcs) {
                    i2 = *(*(sur->communities + sur->Nc-1) + jj);
                    if (ic1!=sur->Nc-1) {*(sur->partition+i2) = ic1;}
                    *(*(sur->communities + ic1) + jj) = i2;
                    *(*(sur->communities + sur->Nc-1) + jj) = 0;
                }
            }
            for (jj=cs1; jj<lcs; jj++) {
                i2 = *(*(sur->communities + sur->Nc-1) + jj);
                if (ic1!=sur->Nc-1) {*(sur->partition+i2) = ic1;}
                *(*(sur->communities + ic1) + jj) = i2;
                *(*(sur->communities + sur->Nc-1) + jj) = 0;
            }
            *(sur->comsizes + ic2) += cs1;
            *(sur->comsizes + ic1) = *(sur->comsizes + sur->Nc-1);
            *(sur->comsizes + sur->Nc-1) = 0;
        }
        sur->Nc -= 1;
        toret = 1;
    }
    return toret;
}




void mergerN(Surpriser *sur, int ic1, double *coms) {
    int cs1, cs2, ic2;
    int dM;//M1, M2, M3;
    int dp=0;
    int ii, jj, i1, i2;
    double nsurp;
    //if ((ic1<0)|(ic1>=sur->Nc)) {return toret;}
    cs1 = *(sur->comsizes+ic1);
    //M1 = cs1*(cs1-1)/2;
    for (ic2=0; ic2<sur->Nc; ic2++) {
        cs2 = *(sur->comsizes+ic2);
        //M2 = cs2*(cs2-1)/2;
        //M3 = (cs1+cs2)*(cs1+cs2-1)/2;
        dM= cs1*cs2;
        dp = 0;
        if (ic2!=ic1) {
            for (ii=0; ii<cs1; ii++) {
                i1 = *(*(sur->communities + ic1) + ii);
                for (jj=0; jj<cs2; jj++) {
                    i2 = *(*(sur->communities + ic2) + jj);
                    dp += *(sur->matr + i1* sur->K + i2);
                }
            }
            nsurp = surprise(sur->M+dM, sur->F, sur->nl, sur->p+dp);
            *(coms + ic2) = nsurp-sur->surprise;
        } else {
            *(coms + ic2) = 0.;
        }
    }
}






int extract(Surpriser *sur, int ic1, int ii) {
    int cs1, i1;
    int dp;
    int jj, i2;
    int toret=0;
    double nsurp;
    cs1 = *(sur->comsizes+ic1);
    if (cs1==1) {return toret;}
    //for (ii=0; ii<cs1; ii++) {
        i1 = *(*(sur->communities + ic1) + ii);
        dp = 0;
        for (jj=0; jj<cs1; jj++) {
            i2 = *(*(sur->communities + ic1) + jj);
            dp += *(sur->matr + i1* sur->K + i2);
        }
        nsurp = surprise(sur->M-cs1+1, sur->F, sur->nl, sur->p-dp);
        //if (nsurp > sur->surprise) {
            //printf("Element %d (%d) from community %d being extracted! \n", i1, ii, ic1);
            sur->surprise = nsurp;
            sur->M -= cs1-1;
            sur->p -= dp;
            *(*(sur->communities + ic1) + ii) = *(*(sur->communities + ic1) + cs1-1);
            *(*(sur->communities + ic1) + cs1-1) = 0;
            *(*(sur->communities + sur->Nc)) = i1;
            *(sur->comsizes + ic1) -= 1;
            *(sur->comsizes + sur->Nc) = 1;
            *(sur->partition+i1) = sur->Nc;
            sur->Nc += 1;
            return 1;
        //}
    //}
    //return toret;
}




int extractor(Surpriser *sur, int ic1) {
    int cs1;
    int dp;
    int ii, jj, i1, i2;
    int toret=0;
    double nsurp;
    cs1 = *(sur->comsizes+ic1);
    if (cs1==1) {return toret;}
    for (ii=0; ii<cs1; ii++) {
        i1 = *(*(sur->communities + ic1) + ii);
        dp = 0;
        for (jj=0; jj<cs1; jj++) {
            i2 = *(*(sur->communities + ic1) + jj);
            dp += *(sur->matr + i1* sur->K + i2);
        }
        nsurp = surprise(sur->M-cs1+1, sur->F, sur->nl, sur->p-dp);
        if (nsurp > sur->surprise) {
            //printf("Element %d (%d) from community %d being extracted! \n", i1, ii, ic1);
            i1 = *(*(sur->communities + ic1) + ii);
            sur->surprise = nsurp;
            sur->M -= cs1-1;
            sur->p -= dp;
            *(*(sur->communities + ic1) + ii) = *(*(sur->communities + ic1) + cs1-1);
            *(*(sur->communities + ic1) + cs1-1) = 0;
            *(*(sur->communities + sur->Nc)) = i1;
            *(sur->comsizes + ic1) -= 1;
            *(sur->comsizes + sur->Nc) = 1;
            *(sur->partition+i1) = sur->Nc;
            sur->Nc += 1;
            return 1;
        }
    }
    return toret;
}


int extractor2(Surpriser *sur, int ic1) {
    int cs1;
    int dp, dpbest=0, iibest=0;
    int ii, jj, i1, i2;
    int toret=0;
    double nsurp, surpbest=0;
    cs1 = *(sur->comsizes+ic1);
    if (cs1==1) {return toret;}
    for (ii=0; ii<cs1; ii++) {
        i1 = *(*(sur->communities + ic1) + ii);
        dp = 0;
        for (jj=0; jj<cs1; jj++) {
            i2 = *(*(sur->communities + ic1) + jj);
            dp += *(sur->matr + i1* sur->K + i2);
        }
        nsurp = surprise(sur->M-cs1+1, sur->F, sur->nl, sur->p-dp);
        if (nsurp > surpbest) {
            surpbest = nsurp;
            dpbest = dp;
            iibest = ii;
        }
    }
    if (surpbest > sur->surprise) {
        //printf("Element %d (%d) from community %d being extracted! \n", i1, ii, ic1);
        nsurp = surpbest;
        ii = iibest;
        i1 = *(*(sur->communities + ic1) + ii);
        dp = dpbest;
        sur->surprise = nsurp;
        sur->M -= cs1-1;
        sur->p -= dp;
        *(*(sur->communities + ic1) + ii) = *(*(sur->communities + ic1) + cs1-1);
        *(*(sur->communities + ic1) + cs1-1) = 0;
        *(*(sur->communities + sur->Nc)) = i1;
        *(sur->comsizes + ic1) -= 1;
        *(sur->comsizes + sur->Nc) = 1;
        *(sur->partition+i1) = sur->Nc;
        sur->Nc += 1;
        toret = 1;
    }
    return toret;
}


void extractorN(Surpriser *sur, int ic1, double *elems) {
    int cs1;
    int dp;
    int ii, jj, i1, i2;
    double nsurp;
    cs1 = *(sur->comsizes+ic1);
    //if (cs1==1) {return toret;}
    for (ii=0; ii<cs1; ii++) {
        i1 = *(*(sur->communities + ic1) + ii);
        dp = 0;
        for (jj=0; jj<cs1; jj++) {
            i2 = *(*(sur->communities + ic1) + jj);
            dp += *(sur->matr + i1* sur->K + i2);
        }
        nsurp = surprise(sur->M-cs1+1, sur->F, sur->nl, sur->p-dp);
        *(elems + ii) = nsurp-sur->surprise;
    }
}



int exchanger1(Surpriser *sur, int ic1, int ic2, int ii) {
    int cs1, cs2;
    int dp;
    int jj, i1, i2;
    int toret=0;
    double nsurp;
    cs1 = *(sur->comsizes+ic1);
    cs2 = *(sur->comsizes+ic2);
    if ((cs1==1)|(ic1==ic2)|(ii>=cs1)) {return 0;}
    //for (ii=0; ii<cs1; ii++) {
        i1 = *(*(sur->communities + ic1) + ii);
        dp = 0;
        for (jj=0; jj<cs1; jj++) {
            i2 = *(*(sur->communities + ic1) + jj);
            dp -= *(sur->matr + i1* sur->K + i2);
        }
        for (jj=0; jj<cs2; jj++) {
            i2 = *(*(sur->communities + ic2) + jj);
            dp += *(sur->matr + i1* sur->K + i2);
        }
        nsurp = surprise(sur->M-cs1+1+cs2, sur->F, sur->nl, sur->p+dp);
        if (nsurp > sur->surprise) {
            //printf("Element %d (%d) from community %d being transfered to community %d! \n", i1, ii, ic1, ic2);
            sur->surprise = nsurp;
            sur->M -= cs1-1-cs2;
            sur->p += dp;
            *(*(sur->communities + ic1) + ii) = *(*(sur->communities + ic1) + cs1-1);
            *(*(sur->communities + ic1) + cs1-1) = 0;
            *(*(sur->communities + ic2) + cs2) = i1;
            *(sur->comsizes + ic1) -= 1;
            *(sur->comsizes + ic2) += 1;
            *(sur->partition+i1) = ic2;
            toret = 1;
        }
    //}
    return toret;
}


int exchanger(Surpriser *sur, int ic1, int ic2) {
    int cs1, cs2;
    int dp;
    int ii, jj, i1, i2;
    int toret=0;
    double nsurp;
    cs1 = *(sur->comsizes+ic1);
    cs2 = *(sur->comsizes+ic2);
    if ((cs1==1)|(ic1==ic2)) {return merger(sur, ic1, ic2);}
    for (ii=0; ii<cs1; ii++) {
        i1 = *(*(sur->communities + ic1) + ii);
        dp = 0;
        for (jj=0; jj<cs1; jj++) {
            i2 = *(*(sur->communities + ic1) + jj);
            dp -= *(sur->matr + i1* sur->K + i2);
        }
        for (jj=0; jj<cs2; jj++) {
            i2 = *(*(sur->communities + ic2) + jj);
            dp += *(sur->matr + i1* sur->K + i2);
        }
        nsurp = surprise(sur->M-cs1+1+cs2, sur->F, sur->nl, sur->p+dp);
        if (nsurp > sur->surprise) {
            //printf("Element %d (%d) from community %d being transfered to community %d! \n", i1, ii, ic1, ic2);
            sur->surprise = nsurp;
            sur->M -= cs1-1-cs2;
            sur->p += dp;
            *(*(sur->communities + ic1) + ii) = *(*(sur->communities + ic1) + cs1-1);
            *(*(sur->communities + ic1) + cs1-1) = 0;
            *(*(sur->communities + ic2) + cs2) = i1;
            *(sur->comsizes + ic1) -= 1;
            *(sur->comsizes + ic2) += 1;
            *(sur->partition+i1) = ic2;
            return 1;
        }
    }
    return toret;
}


int exchanger2(Surpriser *sur, int ic1) {
    int cs1, cs2;
    int dp;
    int ii, jj, i1, i2, ic2;
    int toret=0;
    int icbest=0, iexbest=0, dpbest=0, Mbest=0, iibest=0, dm=0, csbest=0;
    double nsurp, surpbest=0.;
    cs1 = *(sur->comsizes+ic1);
    if (cs1==1) {return 0;}
    for (ic2=ic1+1; ic2<sur->Nc; ic2++) {
        cs2 = *(sur->comsizes+ic2);
        for (ii=0; ii<cs1; ii++) {
            i1 = *(*(sur->communities + ic1) + ii);
            dp = 0;
            for (jj=0; jj<cs1; jj++) {
                i2 = *(*(sur->communities + ic1) + jj);
                dp -= *(sur->matr + i1* sur->K + i2);
            }
            for (jj=0; jj<cs2; jj++) {
                i2 = *(*(sur->communities + ic2) + jj);
                dp += *(sur->matr + i1* sur->K + i2);
            }
            nsurp = surprise(sur->M-cs1+1+cs2, sur->F, sur->nl, sur->p+dp);
            if (nsurp > surpbest) {
                //printf("Element %d (%d) from community %d being transfered to community %d! \n", i1, ii, ic1, ic2);
                surpbest = nsurp;
                Mbest = cs1-1-cs2;
                dpbest = dp;
                iexbest = i1;
                icbest = ic2;
                iibest = ii;
                csbest = cs2;
            }
        }
    }
    if (surpbest > sur->surprise) {
        //printf("Element %d (%d) from community %d being transfered to community %d! \n", i1, ii, ic1, ic2);
        nsurp = surpbest;
        dm = Mbest;
        dp = dpbest;
        i1 = iexbest;
        ic2 = icbest;
        cs2 = csbest;
        ii = iibest;
        sur->surprise = nsurp;
        sur->M -= dm;
        sur->p += dp;
        *(*(sur->communities + ic1) + ii) = *(*(sur->communities + ic1) + cs1-1);
        *(*(sur->communities + ic1) + cs1-1) = 0;
        *(*(sur->communities + ic2) + cs2) = i1;
        *(sur->comsizes + ic1) -= 1;
        *(sur->comsizes + ic2) += 1;
        *(sur->partition+i1) = ic2;
        toret = 1;
    }
    return toret;
}


int exchanger3(Surpriser *sur, int ic1) {
    int cs1, cs2;
    int dp;
    int ii, jj, i1, i2, ic2;
    int toret=0;
    int icbest=0, iexbest=0, dpbest=0, Mbest=0, iibest=0, dm=0, csbest=0;
    double nsurp, surpbest=0.;
    cs1 = *(sur->comsizes+ic1);
    if (cs1==1) {return toret;}
    for (ic2=0; ic2<sur->Nc; ic2++) {
        if (ic2!=ic1) {
            cs2 = *(sur->comsizes+ic2);
            for (ii=0; ii<cs1; ii++) {
                i1 = *(*(sur->communities + ic1) + ii);
                dp = 0;
                for (jj=0; jj<cs1; jj++) {
                    i2 = *(*(sur->communities + ic1) + jj);
                    dp -= *(sur->matr + i1* sur->K + i2);
                }
                for (jj=0; jj<cs2; jj++) {
                    i2 = *(*(sur->communities + ic2) + jj);
                    dp += *(sur->matr + i1* sur->K + i2);
                }
                nsurp = surprise(sur->M-cs1+1+cs2, sur->F, sur->nl, sur->p+dp);
                if (nsurp > surpbest) {
                    //printf("Element %d (%d) from community %d being transfered to community %d! \n", i1, ii, ic1, ic2);
                    surpbest = nsurp;
                    Mbest = cs1-1-cs2;
                    dpbest = dp;
                    iexbest = i1;
                    icbest = ic2;
                    iibest = ii;
                    csbest = cs2;
                }
            }
        }
    }
    if (surpbest > sur->surprise) {
        //printf("Element %d (%d) from community %d being transfered to community %d! \n", i1, ii, ic1, ic2);
        nsurp = surpbest;
        dm = Mbest;
        dp = dpbest;
        i1 = iexbest;
        ic2 = icbest;
        cs2 = csbest;
        ii = iibest;
        sur->surprise = nsurp;
        sur->M -= dm;
        sur->p += dp;
        *(*(sur->communities + ic1) + ii) = *(*(sur->communities + ic1) + cs1-1);
        *(*(sur->communities + ic1) + cs1-1) = 0;
        *(*(sur->communities + ic2) + cs2) = i1;
        *(sur->comsizes + ic1) -= 1;
        *(sur->comsizes + ic2) += 1;
        *(sur->partition+i1) = ic2;
        toret = 1;
    }
    return toret;
}


int exchanger0(Surpriser *sur, int ic1) {
    int cs1, cs2;
    int dp, dm=0;
    int ii, jj, i1, i2, ic2;
    int toret=-1;
    double nsurp;
    cs1 = *(sur->comsizes+ic1);
    if (cs1==1) {return toret;}
    for (ic2=0; ic2<sur->Nc; ic2++) {
        if (ic2!=ic1) {
            cs2 = *(sur->comsizes+ic2);
            for (ii=0; ii<cs1; ii++) {
                i1 = *(*(sur->communities + ic1) + ii);
                dp = 0;
                for (jj=0; jj<cs1; jj++) {
                    i2 = *(*(sur->communities + ic1) + jj);
                    dp -= *(sur->matr + i1* sur->K + i2);
                }
                for (jj=0; jj<cs2; jj++) {
                    i2 = *(*(sur->communities + ic2) + jj);
                    dp += *(sur->matr + i1* sur->K + i2);
                }
                nsurp = surprise(sur->M-cs1+1+cs2, sur->F, sur->nl, sur->p+dp);
                if (nsurp == sur->surprise) {
                    sur->M -= dm;
                    sur->p += dp;
                    *(*(sur->communities + ic1) + ii) = *(*(sur->communities + ic1) + cs1-1);
                    *(*(sur->communities + ic1) + cs1-1) = 0;
                    *(*(sur->communities + ic2) + cs2) = i1;
                    *(sur->comsizes + ic1) -= 1;
                    *(sur->comsizes + ic2) += 1;
                    *(sur->partition+i1) = ic2;
                    return ic2;
                }
            }
        }
    }
    return toret;
}


void exchangerN(Surpriser *sur, int ic1, int ic2, double *elems) {
    int cs1, cs2;
    int dp;
    int ii, jj, i1, i2;
    double nsurp;
    cs1 = *(sur->comsizes+ic1);
    cs2 = *(sur->comsizes+ic2);
    //if (cs1==1) {return toret;}
    for (ii=0; ii<cs1; ii++) {
        i1 = *(*(sur->communities + ic1) + ii);
        dp = 0;
        for (jj=0; jj<cs1; jj++) {
            i2 = *(*(sur->communities + ic1) + jj);
            dp -= *(sur->matr + i1* sur->K + i2);
        }
        for (jj=0; jj<cs2; jj++) {
            i2 = *(*(sur->communities + ic2) + jj);
            dp += *(sur->matr + i1* sur->K + i2);
        }
        nsurp = surprise(sur->M-cs1+1+cs2, sur->F, sur->nl, sur->p+dp);
        *(elems + ii) = nsurp-sur->surprise;
    }
}




int exchange(Surpriser *sur, int ic1, int ic2, int ii) {
    int cs1, cs2;
    int dp;
    int jj, i1, i2;
    double nsurp;
    cs1 = *(sur->comsizes+ic1);
    cs2 = *(sur->comsizes+ic2);
    if ((cs1==1)|(ic1==ic2)) {return merge(sur, ic1, ic2);}
    //for (ii=0; ii<cs1; ii++) {
        i1 = *(*(sur->communities + ic1) + ii);
        dp = 0;
        for (jj=0; jj<cs1; jj++) {
            i2 = *(*(sur->communities + ic1) + jj);
            dp -= *(sur->matr + i1* sur->K + i2);
        }
        for (jj=0; jj<cs2; jj++) {
            i2 = *(*(sur->communities + ic2) + jj);
            dp += *(sur->matr + i1* sur->K + i2);
        }
        nsurp = surprise(sur->M-cs1+1+cs2, sur->F, sur->nl, sur->p+dp);
        //if (nsurp > sur->surprise) {
            //printf("Element %d (%d) from community %d being transfered to community %d! \n", i1, ii, ic1, ic2);
            sur->surprise = nsurp;
            sur->M -= cs1-1-cs2;
            sur->p += dp;
            *(*(sur->communities + ic1) + ii) = *(*(sur->communities + ic1) + cs1-1);
            *(*(sur->communities + ic1) + cs1-1) = 0;
            *(*(sur->communities + ic2) + cs2) = i1;
            *(sur->comsizes + ic1) -= 1;
            *(sur->comsizes + ic2) += 1;
            *(sur->partition+i1) = ic2;
            return 1;
        //}
    //}
    //return toret;
}



int megastep(Surpriser *sur, double T, int K) {
    // montecarlo step
    int ii, ic1, ic2, kk=0;
    for (ii=0; ii<K; ii++) {
        ic1 = drand() * sur->Nc;
        ic2 = drand() * sur->Nc;
        while ((ic1==ic2)&(sur->Nc>1)) {ic2 = drand() * sur->Nc;}
        kk += merger_an(sur, ic1, ic2, T);
        ic1 = drand() * sur->Nc;
        ic2 = drand() * sur->Nc;
        while ((ic1==ic2)&(sur->Nc>1)) {ic2 = drand() * sur->Nc;}
        kk += exchanger_an(sur, ic1, ic2, T);
        ic1 = drand() * sur->Nc;
        kk += extractor_an(sur, ic1, T);
        ic1 = drand() * sur->Nc;
        kk += subcommuniter_an(sur, ic1, T);
        ic1 = drand() * sur->Nc;
        kk += subcommuniter_exchange_an(sur, ic1, T);
    }
    return kk;
}



int megastepNSC(Surpriser *sur, double T, int K) {
    // montecarlo step
    int ii, ic1, ic2, kk=0;
    for (ii=0; ii<K; ii++) {
        ic1 = drand() * sur->Nc;
        ic2 = drand() * sur->Nc;
        while ((ic1==ic2)&(sur->Nc>1)) {ic2 = drand() * sur->Nc;}
        kk += merger_an(sur, ic1, ic2, T);
        ic1 = drand() * sur->Nc;
        ic2 = drand() * sur->Nc;
        while ((ic1==ic2)&(sur->Nc>1)) {ic2 = drand() * sur->Nc;}
        kk += exchanger_an(sur, ic1, ic2, T);
        ic1 = drand() * sur->Nc;
        kk += extractor_an(sur, ic1, T);
    }
    return kk;
}



int subcommuniter(Surpriser *sur, int ic) {
    int cs, i1, i2, ir;
    int k1, k2, k3, k4, k5;//, k6;
    int scs, dp, cs2;
    int ii, jj, kk, ll;
    int toret=0, dpbest=0, iibest=0, scsbest=0;
    double nsurp, surpbest=0.;
    cs = *(sur -> comsizes + ic);
    if (cs<4) {return 0;}//extractor2(sur, ic);}
    Surpriser *ssur=malloc(sizeof(Surpriser));
    int *y;
    y = calloc(cs * cs, sizeof(int));
    for (ii=0; ii<cs; ii++) {
        i1 = *(*(sur->communities + ic) + ii);
        for (jj=ii+1; jj<cs; jj++) {
            i2 = *(*(sur->communities + ic) + jj);
            *(y + ii*cs + jj) = *(sur->matr + i1* sur->K + i2);
            *(y + jj*cs + ii) = *(sur->matr + i1* sur->K + i2);
        }
    }
    generate_supriser(y, cs, NULL, NULL, ssur);
    stepperD(ssur, &k1, &k2, &k3, &k4, &k5);//, &k6);
    for (ii=0; ii<ssur->Nc; ii++) { // community from ssur beeing tested
        scs = *(ssur->comsizes + ii);
        if (scs>1) {
            dp = 0;
            for (jj=0; jj<ssur->Nc; jj++) { // sums connections between ii and all other communities
                if (ii!=jj) {
                    cs2 = *(ssur->comsizes + jj);
                    for (kk=0; kk<scs; kk++) {
                        i1 = *(*(ssur->communities + ii) + kk);
                        for (ll=0; ll<cs2; ll++) {
                            i2 = *(*(ssur->communities + jj) + ll);
                            dp += *(ssur->matr + i1*ssur->K + i2);
                        }
                    }
                }
            }
            nsurp = surprise(sur->M-scs*(cs-scs), sur->F, sur->nl, sur->p-dp);
            if (nsurp > surpbest) {
                surpbest = nsurp;
                iibest = ii;
                dpbest = dp;
                scsbest = scs;
            }
        }
    }
    if (surpbest > sur->surprise) {
        //printf("community %d (%d) from community %d being extracted! \n", ii, ii, ic1);
        nsurp = surpbest;
        scs = scsbest;
        ii = iibest;
        dp = dpbest;
        sur->surprise = nsurp;
        sur->M -= scs*(cs-scs);
        sur->p -= dp;
        for (jj=0; jj<scs; jj++) {// New community
            i1 = *(*(ssur->communities + ii) + jj);
            ir = *(*(sur->communities + ic) + i1);
            *(*(sur->communities + sur->Nc) + jj) = ir;
            *(*(ssur->communities + ii) + jj) = ir;
            *(sur->partition+ir) = sur->Nc;
        }
        for (jj=0; jj<scs; jj++) {// fixes old com
            ir = *(*(ssur->communities + ii) + jj);
            for (kk=0; kk<cs; kk++) {// fixes ic community
                i2 = *(*(sur->communities + ic) + kk);
                if (i2==ir) {
                    *(*(sur->communities + ic) + kk) = *(*(sur->communities + ic) + cs-1-jj);
                    *(*(sur->communities + ic) + cs-1-jj) = 0;
                    //cs -= 1;
                    break;
                }
            }
        }
        *(sur->comsizes + ic) -= scs;
        *(sur->comsizes + sur->Nc) = scs;
        sur->Nc += 1;
        toret = 1;
    }
    clear_surp(ssur);
    free(ssur);
    free(y);
    return toret;
}





int subcommuniterN(Surpriser *sur, int ic, double *elems) {
    int cs, i1, i2;
    int k1, k2, k3, k4, k5;//, k6;
    int scs, dp, cs2;
    int ii, jj, kk, ll;
    int toret=0;
    double nsurp;
    cs = *(sur -> comsizes + ic);
    //if (cs<4) {return 0;}//extractor2(sur, ic);}
    Surpriser *ssur=malloc(sizeof(Surpriser));
    int *y;
    y = calloc(cs * cs, sizeof(int));
    for (ii=0; ii<cs; ii++) {
        i1 = *(*(sur->communities + ic) + ii);
        for (jj=ii+1; jj<cs; jj++) {
            i2 = *(*(sur->communities + ic) + jj);
            *(y + ii*cs + jj) = *(sur->matr + i1* sur->K + i2);
            *(y + jj*cs + ii) = *(sur->matr + i1* sur->K + i2);
        }
    }
    generate_supriser(y, cs, NULL, NULL, ssur);
    stepperD(ssur, &k1, &k2, &k3, &k4, &k5);//, &k6);
    for (ii=0; ii<ssur->Nc; ii++) { // community from ssur beeing tested
        scs = *(ssur->comsizes + ii);
        //if (scs>1) {
            dp = 0;
            for (jj=0; jj<ssur->Nc; jj++) { // sums connections between ii and all other communities
                if (ii!=jj) {
                    cs2 = *(ssur->comsizes + jj);
                    for (kk=0; kk<scs; kk++) {
                        i1 = *(*(ssur->communities + ii) + kk);
                        for (ll=0; ll<cs2; ll++) {
                            i2 = *(*(ssur->communities + jj) + ll);
                            dp += *(ssur->matr + i1*ssur->K + i2);
                        }
                    }
                }
            }
            nsurp = surprise(sur->M-scs*(cs-scs), sur->F, sur->nl, sur->p-dp);
            *(elems + ii) = nsurp-sur->surprise;
        //}
    }
    toret = ssur->Nc;
    clear_surp(ssur);
    free(ssur);
    free(y);
    return toret;
}




int subcommunited(Surpriser *sur, int ic, int iex) {
    int cs, i1, i2, ir;
    int k1, k2, k3, k4, k5;//, k6;
    int scs, dp, cs2;
    int ii, jj, kk, ll;
    int toret=0, dpbest=0, iibest=0, scsbest=0;
    double nsurp, surpbest=0.;
    cs = *(sur -> comsizes + ic);
    if (cs<4) {return 0;}//extract(sur, ic, iex);}
    Surpriser *ssur=malloc(sizeof(Surpriser));
    int *y;
    y = calloc(cs * cs, sizeof(int));
    for (ii=0; ii<cs; ii++) {
        i1 = *(*(sur->communities + ic) + ii);
        for (jj=ii+1; jj<cs; jj++) {
            i2 = *(*(sur->communities + ic) + jj);
            *(y + ii*cs + jj) = *(sur->matr + i1* sur->K + i2);
            *(y + jj*cs + ii) = *(sur->matr + i1* sur->K + i2);
        }
    }
    generate_supriser(y, cs, NULL, NULL, ssur);
    stepperD(ssur, &k1, &k2, &k3, &k4, &k5);//, &k6);
    //for (ii=0; ii<ssur->Nc; ii++) { // community from ssur beeing tested
    ii = iex;
    if ( (ii<0) | (ii>=ssur->Nc) ) {clear_surp(ssur);
                                    free(ssur);
                                    free(y);
                                    return toret;
        }
        scs = *(ssur->comsizes + ii);
        //if (scs>1) {
            dp = 0;
            for (jj=0; jj<ssur->Nc; jj++) { // sums connections between ii and all other communities
                if (ii!=jj) {
                    cs2 = *(ssur->comsizes + jj);
                    for (kk=0; kk<scs; kk++) {
                        i1 = *(*(ssur->communities + ii) + kk);
                        for (ll=0; ll<cs2; ll++) {
                            i2 = *(*(ssur->communities + jj) + ll);
                            dp += *(ssur->matr + i1*ssur->K + i2);
                        }
                    }
                }
            }
            nsurp = surprise(sur->M-scs*(cs-scs), sur->F, sur->nl, sur->p-dp);
            //if (nsurp > surpbest) {
                surpbest = nsurp;
                iibest = ii;
                dpbest = dp;
                scsbest = scs;
            //}
        //}
    //}
    //if (surpbest > sur->surprise) {
        //printf("community %d (%d) from community %d being extracted! \n", ii, ii, ic1);
        nsurp = surpbest;
        scs = scsbest;
        ii = iibest;
        dp = dpbest;
        sur->surprise = nsurp;
        sur->M -= scs*(cs-scs);
        sur->p -= dp;
        for (jj=0; jj<scs; jj++) {// New community
            i1 = *(*(ssur->communities + ii) + jj);
            ir = *(*(sur->communities + ic) + i1);
            *(*(sur->communities + sur->Nc) + jj) = ir;
            *(*(ssur->communities + ii) + jj) = ir;
            *(sur->partition+ir) = sur->Nc;
        }
        for (jj=0; jj<scs; jj++) {// fixes old com
            ir = *(*(ssur->communities + ii) + jj);
            for (kk=0; kk<cs; kk++) {// fixes ic community
                i2 = *(*(sur->communities + ic) + kk);
                if (i2==ir) {
                    *(*(sur->communities + ic) + kk) = *(*(sur->communities + ic) + cs-1-jj);
                    *(*(sur->communities + ic) + cs-1-jj) = 0;
                    //cs -= 1;
                    break;
                }
            }
        }
        *(sur->comsizes + ic) -= scs;
        *(sur->comsizes + sur->Nc) = scs;
        sur->Nc += 1;
        toret = 1;
    //}
    clear_surp(ssur);
    free(ssur);
    free(y);
    return toret;
}






int subcommuniter_ret(Surpriser *sur, int ic, Surpriser *ssur) {
    int cs, i1, i2, ir;
    int k1, k2, k3, k4, k5;//, k6;
    int scs, dp, cs2;
    int *y;
    int ii, jj, kk, ll;
    int toret=0, dpbest=0, iibest=0, scsbest=0;
    double nsurp, surpbest=0.;
    cs = *(sur -> comsizes + ic);
    if (cs<4) {
        int k;
        k = extractor2(sur, ic);
        if (k) {return -1;} else {return -2;}
    }
    y = calloc(cs * cs, sizeof(int));
    for (ii=0; ii<cs; ii++) {
        i1 = *(*(sur->communities + ic) + ii);
        for (jj=ii+1; jj<cs; jj++) {
            i2 = *(*(sur->communities + ic) + jj);
            *(y + ii*cs + jj) = *(sur->matr + i1* sur->K + i2);
            *(y + jj*cs + ii) = *(sur->matr + i1* sur->K + i2);
        }
    }
    generate_supriser(y, cs, NULL, NULL, ssur);
    stepperD(ssur, &k1, &k2, &k3, &k4, &k5);//, &k6);
    for (ii=0; ii<ssur->Nc; ii++) { // community from ssur beeing tested
        scs = *(ssur->comsizes + ii);
        if (scs>1) {
            dp = 0;
            for (jj=0; jj<ssur->Nc; jj++) { // sums connections between ii and all other communities
                if (ii!=jj) {
                    cs2 = *(ssur->comsizes + jj);
                    for (kk=0; kk<scs; kk++) {
                        i1 = *(*(ssur->communities + ii) + kk);
                        for (ll=0; ll<cs2; ll++) {
                            i2 = *(*(ssur->communities + jj) + ll);
                            dp += *(ssur->matr + i1*ssur->K + i2);
                        }
                    }
                }
            }
            nsurp = surprise(sur->M-scs*(cs-scs), sur->F, sur->nl, sur->p-dp);
            if (nsurp > surpbest) {
                surpbest = nsurp;
                iibest = ii;
                dpbest = dp;
                scsbest = scs;
            }
        }
    }
    if (surpbest > sur->surprise) {
        //printf("community %d (%d) from community %d being extracted! \n", ii, ii, ic1);
        nsurp = surpbest;
        scs = scsbest;
        ii = iibest;
        dp = dpbest;
        sur->surprise = nsurp;
        sur->M -= scs*(cs-scs);
        sur->p -= dp;
        for (jj=0; jj<scs; jj++) {// New community
            i1 = *(*(ssur->communities + ii) + jj);
            ir = *(*(sur->communities + ic) + i1);
            *(*(sur->communities + sur->Nc) + jj) = ir;
            *(*(ssur->communities + ii) + jj) = ir;
            *(sur->partition+ir) = sur->Nc;
        }
        for (jj=0; jj<scs; jj++) {// fixes old com
            ir = *(*(ssur->communities + ii) + jj);
            for (kk=0; kk<cs; kk++) {// fixes ic community
                i2 = *(*(sur->communities + ic) + kk);
                if (i2==ir) {
                    *(*(sur->communities + ic) + kk) = *(*(sur->communities + ic) + cs-1-jj);
                    *(*(sur->communities + ic) + cs-1-jj) = 0;
                    //cs -= 1;
                    break;
                }
            }
        }
        *(sur->comsizes + ic) -= scs;
        *(sur->comsizes + sur->Nc) = scs;
        sur->Nc += 1;
        toret = 1;
    }
    free(y);
    return toret;
}



void subcommunity(Surpriser *sur, int ic, Surpriser *ssur) {
    int cs, i1, i2;
    int k1, k2, k3, k4, k5;//, k6;
    int *y;
    int ii, jj;
    cs = *(sur -> comsizes + ic);
    y = calloc(cs * cs, sizeof(int));
    for (ii=0; ii<cs; ii++) {
        i1 = *(*(sur->communities + ic) + ii);
        for (jj=ii+1; jj<cs; jj++) {
            i2 = *(*(sur->communities + ic) + jj);
            *(y + ii*cs + jj) = *(sur->matr + i1* sur->K + i2);
            *(y + jj*cs + ii) = *(sur->matr + i1* sur->K + i2);
        }
    }
    generate_supriser(y, cs, NULL, NULL, ssur);
    stepperD(ssur, &k1, &k2, &k3, &k4, &k5);//, &k6);
    free(y);
}






int subcommuniter_exchange0(Surpriser *sur, int ic) {
    int cs, i1, i2, ir, ibc;
    int k1, k2, k3, k4, k5;//, k6;
    int scs, dp, dps, cs2, dm, toret=-1;
    int bcs;
    int ii, jj, kk, ll, mm;
    double nsurp;
    cs = *(sur -> comsizes + ic);
    if ((cs<4)|(sur->Nc==1)) {return toret;}//exchanger3(sur, ic);}
    Surpriser *ssur=malloc(sizeof(Surpriser));
    int *y;
    y = calloc(cs * cs, sizeof(int));
    for (ii=0; ii<cs; ii++) {
        i1 = *(*(sur->communities + ic) + ii);
        for (jj=ii+1; jj<cs; jj++) {
            i2 = *(*(sur->communities + ic) + jj);
            *(y + ii*cs + jj) = *(sur->matr + i1* sur->K + i2);
            *(y + jj*cs + ii) = *(sur->matr + i1* sur->K + i2);
        }
    }
    generate_supriser(y, cs, NULL, NULL, ssur);
    stepperD(ssur, &k1, &k2, &k3, &k4, &k5);//, &k6);
    for (ii=0; ii<ssur->Nc; ii++) { // community from ssur beeing tested
        scs = *(ssur->comsizes + ii);
        if (scs>1) {
            dps = 0;
            for (jj=0; jj<ssur->Nc; jj++) { // sums connections between ii and all other communities
                if (ii!=jj) {
                    cs2 = *(ssur->comsizes + jj);
                    for (kk=0; kk<scs; kk++) {
                        i1 = *(*(ssur->communities + ii) + kk);
                        for (ll=0; ll<cs2; ll++) {
                            i2 = *(*(ssur->communities + jj) + ll);
                            dps += *(ssur->matr + i1*ssur->K + i2);
                        }
                    }
                }
            }
            for (mm=0; mm<sur->Nc; mm++) {// loop in sur communities
                if (mm!=ic) {
                    bcs = *(sur->comsizes + mm);
                    dp = -dps;
                    for (jj=0; jj<bcs; jj++) { // sums connections between ii and other community
                        ibc = *(*(sur->communities + mm) + jj);
                        for (kk=0; kk<scs; kk++) {
                            i1 = *(*(sur->communities + ic) + *(*(ssur->communities + ii) + kk));
                            dp += *(sur->matr + ibc*sur->K + i1);
                        }
                    }
                    dm = -scs*(cs-scs) + scs*bcs;
                    nsurp = surprise(sur->M+dm, sur->F, sur->nl, sur->p+dp);
                    if (nsurp == sur->surprise) {
                        //sur->surprise = nsurp;
                        sur->M += dm;
                        sur->p += dp;
                        for (jj=0; jj<scs; jj++) {// community migrates
                            i1 = *(*(ssur->communities + ii) + jj);
                            ir = *(*(sur->communities + ic) + i1);
                            *(*(sur->communities + mm) + jj + bcs) = ir;
                            *(*(ssur->communities + ii) + jj) = ir;
                            *(sur->partition+ir) = mm;
                        }
                        for (jj=0; jj<scs; jj++) {// fixes old com
                            ir = *(*(ssur->communities + ii) + jj);
                            for (kk=0; kk<cs; kk++) {// fixes ic community
                                i2 = *(*(sur->communities + ic) + kk);
                                if (i2==ir) {
                                    *(*(sur->communities + ic) + kk) = *(*(sur->communities + ic) + cs-1-jj);
                                    *(*(sur->communities + ic) + cs-1-jj) = 0;
                                    //cs -= 1;
                                    break;
                                }
                            }
                        }
                        *(sur->comsizes + ic) -= scs;
                        *(sur->comsizes + mm) += scs;
                        clear_surp(ssur);
                        free(ssur);
                        free(y);
                        return mm;
                    }
                }
            }
        }
    }
    clear_surp(ssur);
    free(ssur);
    free(y);
    return toret;
}




int subcommuniter_exchange(Surpriser *sur, int ic) {
    int cs, i1, i2, ir, ibc;
    int k1, k2, k3, k4, k5;//, k6;
    int scs, dp, dps, cs2, dm, toret=0;
    int bcs, mmbest=0, dpbest=0, icbest=0, dmbest=0, scsbest=0, bcsbest=0;
    int ii, jj, kk, ll, mm;
    double nsurp, surpbest=0.;
    cs = *(sur -> comsizes + ic);
    if ((cs<4)|(sur->Nc==1)) {return 0;}//exchanger3(sur, ic);}
    Surpriser *ssur=malloc(sizeof(Surpriser));
    int *y;
    y = calloc(cs * cs, sizeof(int));
    for (ii=0; ii<cs; ii++) {
        i1 = *(*(sur->communities + ic) + ii);
        for (jj=ii+1; jj<cs; jj++) {
            i2 = *(*(sur->communities + ic) + jj);
            *(y + ii*cs + jj) = *(sur->matr + i1* sur->K + i2);
            *(y + jj*cs + ii) = *(sur->matr + i1* sur->K + i2);
        }
    }
    generate_supriser(y, cs, NULL, NULL, ssur);
    stepperD(ssur, &k1, &k2, &k3, &k4, &k5);//, &k6);
    for (ii=0; ii<ssur->Nc; ii++) { // community from ssur beeing tested
        scs = *(ssur->comsizes + ii);
        if (scs>1) {
            dps = 0;
            for (jj=0; jj<ssur->Nc; jj++) { // sums connections between ii and all other communities
                if (ii!=jj) {
                    cs2 = *(ssur->comsizes + jj);
                    for (kk=0; kk<scs; kk++) {
                        i1 = *(*(ssur->communities + ii) + kk);
                        for (ll=0; ll<cs2; ll++) {
                            i2 = *(*(ssur->communities + jj) + ll);
                            dps += *(ssur->matr + i1*ssur->K + i2);
                        }
                    }
                }
            }
            for (mm=0; mm<sur->Nc; mm++) {// loop in sur communities
                if (mm!=ic) {
                    bcs = *(sur->comsizes + mm);
                    dp = -dps;
                    for (jj=0; jj<bcs; jj++) { // sums connections between ii and other community
                        ibc = *(*(sur->communities + mm) + jj);
                        for (kk=0; kk<scs; kk++) {
                            i1 = *(*(sur->communities + ic) + *(*(ssur->communities + ii) + kk));
                            dp += *(sur->matr + ibc*sur->K + i1);
                        }
                    }
                    dm = -scs*(cs-scs) + scs*bcs;
                    nsurp = surprise(sur->M+dm, sur->F, sur->nl, sur->p+dp);
                    if (nsurp > surpbest) {
                        surpbest = nsurp;
                        mmbest = mm;
                        dpbest = dp;
                        icbest = ii;
                        dmbest = dm;
                        scsbest = scs;
                        bcsbest = bcs;
                    }
                }
            }
        }
    }
    if (surpbest > sur->surprise) {
        //printf("community %d (%d) from community %d being sent to %d! \n", ii, ii, ic1, mm);
        nsurp = surpbest;
        mm = mmbest;
        dp = dpbest;
        ii = icbest;
        dm = dmbest;
        scs = scsbest;
        bcs = bcsbest;
        sur->surprise = nsurp;
        sur->M += dm;
        sur->p += dp;
        for (jj=0; jj<scs; jj++) {// community migrates
            i1 = *(*(ssur->communities + ii) + jj);
            ir = *(*(sur->communities + ic) + i1);
            *(*(sur->communities + mm) + jj + bcs) = ir;
            *(*(ssur->communities + ii) + jj) = ir;
            *(sur->partition+ir) = mm;
        }
        for (jj=0; jj<scs; jj++) {// fixes old com
            ir = *(*(ssur->communities + ii) + jj);
            for (kk=0; kk<cs; kk++) {// fixes ic community
                i2 = *(*(sur->communities + ic) + kk);
                if (i2==ir) {
                    *(*(sur->communities + ic) + kk) = *(*(sur->communities + ic) + cs-1-jj);
                    *(*(sur->communities + ic) + cs-1-jj) = 0;
                    //cs -= 1;
                    break;
                }
            }
        }
        *(sur->comsizes + ic) -= scs;
        *(sur->comsizes + mm) += scs;
        toret = 1;
    }
    clear_surp(ssur);
    free(ssur);
    free(y);
    return toret;
}




int subcommuniter_exchange2(Surpriser *sur, int ic, int mm) {
    int cs, i1, i2, ir, ibc;
    int k1, k2, k3, k4, k5;//, k6;
    int scs, dp, dps, cs2, dm, toret=0;
    int bcs, dpbest=0, icbest=0, dmbest=0, scsbest=0, bcsbest=0;
    int ii, jj, kk, ll;
    double nsurp, surpbest=0.;
    cs = *(sur -> comsizes + ic);
    if ((cs<4)|(sur->Nc==1)|(ic==mm)) {return 0;}//exchanger3(sur, ic);}
    Surpriser *ssur=malloc(sizeof(Surpriser));
    int *y;
    y = calloc(cs * cs, sizeof(int));
    for (ii=0; ii<cs; ii++) {
        i1 = *(*(sur->communities + ic) + ii);
        for (jj=ii+1; jj<cs; jj++) {
            i2 = *(*(sur->communities + ic) + jj);
            *(y + ii*cs + jj) = *(sur->matr + i1* sur->K + i2);
            *(y + jj*cs + ii) = *(sur->matr + i1* sur->K + i2);
        }
    }
    generate_supriser(y, cs, NULL, NULL, ssur);
    stepperD(ssur, &k1, &k2, &k3, &k4, &k5);//, &k6);
    for (ii=0; ii<ssur->Nc; ii++) { // community from ssur beeing tested
        scs = *(ssur->comsizes + ii);
        if (scs>1) {
            dps = 0;
            for (jj=0; jj<ssur->Nc; jj++) { // sums connections between ii and all other communities
                if (ii!=jj) {
                    cs2 = *(ssur->comsizes + jj);
                    for (kk=0; kk<scs; kk++) {
                        i1 = *(*(ssur->communities + ii) + kk);
                        for (ll=0; ll<cs2; ll++) {
                            i2 = *(*(ssur->communities + jj) + ll);
                            dps += *(ssur->matr + i1*ssur->K + i2);
                        }
                    }
                }
            }
            //for (mm=0; mm<sur->Nc; mm++) {// loop in sur communities
                //if (mm!=ic) {
                    bcs = *(sur->comsizes + mm);
                    dp = -dps;
                    for (jj=0; jj<bcs; jj++) { // sums connections between ii and other community
                        ibc = *(*(sur->communities + mm) + jj);
                        for (kk=0; kk<scs; kk++) {
                            i1 = *(*(sur->communities + ic) + *(*(ssur->communities + ii) + kk));
                            dp += *(sur->matr + ibc*sur->K + i1);
                        }
                    }
                    dm = -scs*(cs-scs) + scs*bcs;
                    nsurp = surprise(sur->M+dm, sur->F, sur->nl, sur->p+dp);
                    if (nsurp > surpbest) {
                        surpbest = nsurp;
                        dpbest = dp;
                        icbest = ii;
                        dmbest = dm;
                        scsbest = scs;
                        bcsbest = bcs;
                    }
                //}
            //}
        }
    }
    if (surpbest > sur->surprise) {
        //printf("community %d (%d) from community %d being sent to %d! \n", ii, ii, ic1, mm);
        nsurp = surpbest;
        dp = dpbest;
        ii = icbest;
        dm = dmbest;
        scs = scsbest;
        bcs = bcsbest;
        sur->surprise = nsurp;
        sur->M += dm;
        sur->p += dp;
        for (jj=0; jj<scs; jj++) {// community migrates
            i1 = *(*(ssur->communities + ii) + jj);
            ir = *(*(sur->communities + ic) + i1);
            *(*(sur->communities + mm) + jj + bcs) = ir;
            *(*(ssur->communities + ii) + jj) = ir;
            *(sur->partition+ir) = mm;
        }
        for (jj=0; jj<scs; jj++) {// fixes old com
            ir = *(*(ssur->communities + ii) + jj);
            for (kk=0; kk<cs; kk++) {// fixes ic community
                i2 = *(*(sur->communities + ic) + kk);
                if (i2==ir) {
                    *(*(sur->communities + ic) + kk) = *(*(sur->communities + ic) + cs-1-jj);
                    *(*(sur->communities + ic) + cs-1-jj) = 0;
                    //cs -= 1;
                    break;
                }
            }
        }
        *(sur->comsizes + ic) -= scs;
        *(sur->comsizes + mm) += scs;
        toret = 1;
    }
    clear_surp(ssur);
    free(ssur);
    free(y);
    return toret;
}





int subcommuniter_exchange3(Surpriser *sur, int ic) {
    int cs, i1, i2, ir, ibc;
    int k1, k2, k3, k4, k5;//, k6;
    int scs, dp, dps, cs2, dm, toret=0;
    int bcs;
    int ii, jj, kk, ll, mm;
    double nsurp;
    cs = *(sur -> comsizes + ic);
    if ((cs<4)|(sur->Nc==1)) {return 0;}//exchanger3(sur, ic);}
    Surpriser *ssur=malloc(sizeof(Surpriser));
    int *y;
    y = calloc(cs * cs, sizeof(int));
    for (ii=0; ii<cs; ii++) {
        i1 = *(*(sur->communities + ic) + ii);
        for (jj=ii+1; jj<cs; jj++) {
            i2 = *(*(sur->communities + ic) + jj);
            *(y + ii*cs + jj) = *(sur->matr + i1* sur->K + i2);
            *(y + jj*cs + ii) = *(sur->matr + i1* sur->K + i2);
        }
    }
    generate_supriser(y, cs, NULL, NULL, ssur);
    stepperD(ssur, &k1, &k2, &k3, &k4, &k5);//, &k6);
    for (ii=0; ii<ssur->Nc; ii++) { // community from ssur beeing tested
        scs = *(ssur->comsizes + ii);
        if (scs>1) {
            dps = 0;
            for (jj=0; jj<ssur->Nc; jj++) { // sums connections between ii and all other communities
                if (ii!=jj) {
                    cs2 = *(ssur->comsizes + jj);
                    for (kk=0; kk<scs; kk++) {
                        i1 = *(*(ssur->communities + ii) + kk);
                        for (ll=0; ll<cs2; ll++) {
                            i2 = *(*(ssur->communities + jj) + ll);
                            dps += *(ssur->matr + i1*ssur->K + i2);
                        }
                    }
                }
            }
            for (mm=0; mm<sur->Nc; mm++) {// loop in sur communities
                if (mm!=ic) {
                    bcs = *(sur->comsizes + mm);
                    dp = -dps;
                    for (jj=0; jj<bcs; jj++) { // sums connections between ii and other community
                        ibc = *(*(sur->communities + mm) + jj);
                        for (kk=0; kk<scs; kk++) {
                            i1 = *(*(sur->communities + ic) + *(*(ssur->communities + ii) + kk));
                            dp += *(sur->matr + ibc*sur->K + i1);
                        }
                    }
                    dm = -scs*(cs-scs) + scs*bcs;
                    nsurp = surprise(sur->M+dm, sur->F, sur->nl, sur->p+dp);
                    if (nsurp > sur->surprise) {
                        sur->surprise = nsurp;
                        sur->M += dm;
                        sur->p += dp;
                        for (jj=0; jj<scs; jj++) {// community migrates
                            i1 = *(*(ssur->communities + ii) + jj);
                            ir = *(*(sur->communities + ic) + i1);
                            *(*(sur->communities + mm) + jj + bcs) = ir;
                            *(*(ssur->communities + ii) + jj) = ir;
                            *(sur->partition+ir) = mm;
                        }
                        for (jj=0; jj<scs; jj++) {// fixes old com
                            ir = *(*(ssur->communities + ii) + jj);
                            for (kk=0; kk<cs; kk++) {// fixes ic community
                                i2 = *(*(sur->communities + ic) + kk);
                                if (i2==ir) {
                                    *(*(sur->communities + ic) + kk) = *(*(sur->communities + ic) + cs-1-jj);
                                    *(*(sur->communities + ic) + cs-1-jj) = 0;
                                    //cs -= 1;
                                    break;
                                }
                            }
                        }
                        *(sur->comsizes + ic) -= scs;
                        *(sur->comsizes + mm) += scs;
                        toret = 1;
                        clear_surp(ssur);
                        free(ssur);
                        free(y);
                        return toret;
                    }
                }
            }
        }
    }
    clear_surp(ssur);
    free(ssur);
    free(y);
    return toret;
}










int subcommuniter_exchanged(Surpriser *sur, int ic, int mm, int iex) {
    int cs, i1, i2, ir, ibc;
    int k1, k2, k3, k4, k5;//, k6;
    int scs, dp, dps, cs2, dm, toret=0;
    int bcs;
    int ii, jj, kk, ll;
    double nsurp;
    cs = *(sur -> comsizes + ic);
    if ((cs<4)|(ic==mm)) {return 0;}//exchange(sur, ic, mm, iex);}
    Surpriser *ssur=malloc(sizeof(Surpriser));
    int *y;
    y = calloc(cs * cs, sizeof(int));
    for (ii=0; ii<cs; ii++) {
        i1 = *(*(sur->communities + ic) + ii);
        for (jj=ii+1; jj<cs; jj++) {
            i2 = *(*(sur->communities + ic) + jj);
            *(y + ii*cs + jj) = *(sur->matr + i1* sur->K + i2);
            *(y + jj*cs + ii) = *(sur->matr + i1* sur->K + i2);
        }
    }
    generate_supriser(y, cs, NULL, NULL, ssur);
    stepperD(ssur, &k1, &k2, &k3, &k4, &k5);//, &k6);
    scs = *(ssur->comsizes + iex);
    dps = 0;
    for (jj=0; jj<ssur->Nc; jj++) { // sums connections between iex and all other communities
        if (iex!=jj) {
            cs2 = *(ssur->comsizes + jj);
            for (kk=0; kk<scs; kk++) {
                i1 = *(*(ssur->communities + iex) + kk);
                for (ll=0; ll<cs2; ll++) {
                    i2 = *(*(ssur->communities + jj) + ll);
                    dps += *(ssur->matr + i1*ssur->K + i2);
                }
            }
        }
    }
    if (mm!=ic) {
        bcs = *(sur->comsizes + mm);
        dp = -dps;
        for (jj=0; jj<bcs; jj++) { // sums connections between iex and other community
            ibc = *(*(sur->communities + mm) + jj);
            for (kk=0; kk<scs; kk++) {
                i1 = *(*(sur->communities + ic) + *(*(ssur->communities + iex) + kk));
                dp += *(sur->matr + ibc*sur->K + i1);
            }
        }
        dm = -scs*(cs-scs) + scs*bcs;
        nsurp = surprise(sur->M+dm, sur->F, sur->nl, sur->p+dp);
        //if (nsurp > surpbest) {
        //}
        toret = 1;
    }
    if (toret) {
        ii = iex;
        //printf("community %d (%d) from community %d being sent to %d! \n", ii, ii, ic1, mm);
        sur->surprise = nsurp;
        sur->M += dm;
        sur->p += dp;
        for (jj=0; jj<scs; jj++) {// community migrates
            i1 = *(*(ssur->communities + ii) + jj);
            ir = *(*(sur->communities + ic) + i1);
            *(*(sur->communities + mm) + jj + bcs) = ir;
            *(*(ssur->communities + ii) + jj) = ir;
            *(sur->partition+ir) = mm;
        }
        for (jj=0; jj<scs; jj++) {// fixes old com
            ir = *(*(ssur->communities + ii) + jj);
            for (kk=0; kk<cs; kk++) {// fixes ic community
                i2 = *(*(sur->communities + ic) + kk);
                if (i2==ir) {
                    *(*(sur->communities + ic) + kk) = *(*(sur->communities + ic) + cs-1-jj);
                    *(*(sur->communities + ic) + cs-1-jj) = 0;
                    //cs -= 1;
                    break;
                }
            }
        }
        *(sur->comsizes + ic) -= scs;
        *(sur->comsizes + mm) += scs;
        toret = 1;
    }
    clear_surp(ssur);
    free(ssur);
    free(y);
    return toret;
}


int subcommuniter_exchangeN(Surpriser *sur, int ic, int mm, double *subc) {
    int cs, i1, i2, ibc;
    int k1, k2, k3, k4, k5;//, k6;
    int scs, dp, dps, cs2, dm;
    int bcs, toret;
    int ii, jj, kk, ll;
    double nsurp;
    cs = *(sur -> comsizes + ic);
    //if (cs<4) {return exchangerN(sur, ic, mm, subc, eps);}
    Surpriser *ssur=malloc(sizeof(Surpriser));
    int *y;
    y = calloc(cs * cs, sizeof(int));
    for (ii=0; ii<cs; ii++) {
        i1 = *(*(sur->communities + ic) + ii);
        for (jj=ii+1; jj<cs; jj++) {
            i2 = *(*(sur->communities + ic) + jj);
            *(y + ii*cs + jj) = *(sur->matr + i1* sur->K + i2);
            *(y + jj*cs + ii) = *(sur->matr + i1* sur->K + i2);
        }
    }
    generate_supriser(y, cs, NULL, NULL, ssur);
    stepperD(ssur, &k1, &k2, &k3, &k4, &k5);//, &k6);
    toret = ssur->Nc;
    for (ii=0; ii<ssur->Nc; ii++) { // community from ssur beeing tested
        scs = *(ssur->comsizes + ii);
        //if (scs>1) {
            dps = 0;
            for (jj=0; jj<ssur->Nc; jj++) { // sums connections between ii and all other communities
                if (ii!=jj) {
                    cs2 = *(ssur->comsizes + jj);
                    for (kk=0; kk<scs; kk++) {
                        i1 = *(*(ssur->communities + ii) + kk);
                        for (ll=0; ll<cs2; ll++) {
                            i2 = *(*(ssur->communities + jj) + ll);
                            dps += *(ssur->matr + i1*ssur->K + i2);
                        }
                    }
                }
            }
            if (mm!=ic) {
                bcs = *(sur->comsizes + mm);
                dp = -dps;
                for (jj=0; jj<bcs; jj++) { // sums connections between ii and other community
                    ibc = *(*(sur->communities + mm) + jj);
                    for (kk=0; kk<scs; kk++) {
                        i1 = *(*(sur->communities + ic) + *(*(ssur->communities + ii) + kk));
                        dp += *(sur->matr + ibc*sur->K + i1);
                    }
                }
                dm = -scs*(cs-scs) + scs*bcs;
                nsurp = surprise(sur->M+dm, sur->F, sur->nl, sur->p+dp);
                *(subc + ii) = nsurp-sur->surprise;
            } else {toret=0;}
        //}
    }
    clear_surp(ssur);
    free(ssur);
    free(y);
    return toret;
}





void stepper1(Surpriser *sur, int *k1, int *k2, int *k3, int *k4, int *k5, int *k6) {
    int ii;
    int kk1, kk2, kk3, kk4, kk5, kk6;
    int cont=1;
    *k1 = 0;
    *k2 = 0;
    *k3 = 0;
    *k4 = 0;
    *k5 = 0;
    *k6 = 0;
    while (cont) {
        kk1 = 0; //extractions
        kk2 = 0; //exchanges
        kk3 = 0; //merges
        kk4 = 0; //subcoms extract
        kk5 = 0; //subcoms exchange
        kk6 = 0; //subcoms merge
        for (ii=0; ii<sur->Nc; ii++) {
            kk3 += merger3(sur, ii);
            while (extractor2(sur, ii)) {kk1 += 1;}
            while (subcommuniter(sur, ii)) {kk4 += 1;}
            while (exchanger3(sur, ii)) {kk2 += 1;}
            while (subcommuniter_exchange(sur, ii)) {kk5 += 1;}
            /*for (jj=ii+1; jj<sur->Nc; jj++) {
                kk6 += subcommuniter_merger(sur, ii, jj);
            }*/
        }
        *k1 += kk1;
        *k2 += kk2;
        *k3 += kk3;
        *k4 += kk4;
        *k5 += kk5;
        *k6 += kk6;
        if (kk1+kk2+kk3+kk4+kk5+kk6==0) {cont=0;}
    }
}


void stepper2(Surpriser *sur, int *k1, int *k2, int *k3, int *k4, int *k5, int *k6) {
    int ii;
    int kk1, kk2, kk3, kk4, kk5, kk6;
    int cont=1;
    *k1 = 0;
    *k2 = 0;
    *k3 = 0;
    *k4 = 0;
    *k5 = 0;
    *k6 = 0;
    while (cont) {
        kk1 = 0; //extractions
        kk2 = 0; //exchanges
        kk3 = 0; //merges
        kk4 = 0; //subcoms extract
        kk5 = 0; //subcoms exchange
        kk6 = 0; //subcoms merge
        for (ii=0; ii<sur->Nc; ii++) {
            while (extractor2(sur, ii)) {kk1 += 1;}
        }
        for (ii=0; ii<sur->Nc; ii++) {
            while (subcommuniter(sur, ii)) {kk4 += 1;}
        }
        for (ii=0; ii<sur->Nc; ii++) {
            while (exchanger3(sur, ii)) {kk2 += 1;}
        }
        for (ii=0; ii<sur->Nc; ii++) {
            while (subcommuniter_exchange(sur, ii)) {kk5 += 1;}
        }
        for (ii=0; ii<sur->Nc; ii++) {
            while (merger3(sur, ii)) {kk3 += 1;}
        }
        /*for (ii=0; ii<sur->Nc; ii++) {
            for (jj=ii+1; jj<sur->Nc; jj++) {
                kk6 += subcommuniter_merger(sur, ii, jj);
            }
        }*/
        *k1 += kk1;
        *k2 += kk2;
        *k3 += kk3;
        *k4 += kk4;
        *k5 += kk5;
        *k6 += kk6;
        if (kk1+kk2+kk3+kk4+kk5+kk6==0) {cont=0;}
    }
}





void stepper3(Surpriser *sur, int *k1, int *k2, int *k3) {
    int ii;
    int kk1, kk2, kk3;
    int cont=1;
    *k1 = 0;
    *k2 = 0;
    *k3 = 0;
    while (cont) {
        kk1 = 0; //extractions
        kk2 = 0; //exchanges
        kk3 = 0; //merges
        for (ii=0; ii<sur->Nc; ii++) {
            kk3 += merger3(sur, ii);
            while (extractor2(sur, ii)) {kk1 += 1;}
            while (exchanger3(sur, ii)) {kk2 += 1;}
        }
        *k1 += kk1;
        *k2 += kk2;
        *k3 += kk3;
        if (kk1+kk2+kk3==0) {cont=0;}
    }
}


void stepper4(Surpriser *sur, int *k1, int *k2, int *k3) {
    int ii;
    int kk1, kk2, kk3;
    int cont=1;
    *k1 = 0;
    *k2 = 0;
    *k3 = 0;
    while (cont) {
        kk1 = 0; //extractions
        kk2 = 0; //exchanges
        kk3 = 0; //merges
        for (ii=0; ii<sur->Nc; ii++) {
            while (extractor2(sur, ii)) {kk1 += 1;}
        }
        for (ii=0; ii<sur->Nc; ii++) {
            while (exchanger3(sur, ii)) {kk2 += 1;}
        }
        for (ii=0; ii<sur->Nc; ii++) {
            while (merger3(sur, ii)) {kk3 += 1;}
        }
        *k1 += kk1;
        *k2 += kk2;
        *k3 += kk3;
        if (kk1+kk2+kk3==0) {cont=0;}
    }
}



void stepper5(Surpriser *sur, int *k1, int *k2, int *k3, int *k4, int *k5, int *k6) {
    int ii;
    int kk1, kk2, kk3, kk4, kk5, kk6;
    int cont=1;
    *k1 = 0;
    *k2 = 0;
    *k3 = 0;
    *k4 = 0;
    *k5 = 0;
    *k6 = 0;
    while (cont) {
        kk1 = 0; //extractions
        kk2 = 0; //exchanges
        kk3 = 0; //merges
        kk4 = 0; //subcoms extract
        kk5 = 0; //subcoms exchange
        kk6 = 0; //subcoms merge
        for (ii=0; ii<sur->Nc; ii++) {
            while (merger3(sur, ii)) {kk3 += 1;}
        }
        for (ii=0; ii<sur->Nc; ii++) {
            while (extractor2(sur, ii)) {kk1 += 1;}
        }
        for (ii=0; ii<sur->Nc; ii++) {
            while (exchanger3(sur, ii)) {kk2 += 1;}
        }
        /*for (ii=0; ii<sur->Nc; ii++) {
            for (jj=ii+1; jj<sur->Nc; jj++) {
                kk6 += subcommuniter_merger(sur, ii, jj);
            }
        }*/
        for (ii=0; ii<sur->Nc; ii++) {
            while (subcommuniter(sur, ii)) {kk4 += 1;}
        }
        for (ii=0; ii<sur->Nc; ii++) {
            while (subcommuniter_exchange(sur, ii)) {kk5 += 1;}
        }
        *k1 += kk1;
        *k2 += kk2;
        *k3 += kk3;
        *k4 += kk4;
        *k5 += kk5;
        *k6 += kk6;
        if (kk1+kk2+kk3+kk4+kk5+kk6==0) {cont=0;}
    }
}




void stepper6(Surpriser *sur, int *k1, int *k2, int *k3) {
    int ii;
    int kk1, kk2, kk3;
    int cont=1;
    *k1 = 0;
    *k2 = 0;
    *k3 = 0;
    while (cont) {
        kk1 = 0; //extractions
        kk2 = 0; //exchanges
        kk3 = 0; //merges
        for (ii=0; ii<sur->Nc; ii++) {
            while (merger3(sur, ii)) {kk3 += 1;}
        }
        for (ii=0; ii<sur->Nc; ii++) {
            while (extractor2(sur, ii)) {kk1 += 1;}
        }
        for (ii=0; ii<sur->Nc; ii++) {
            while (exchanger3(sur, ii)) {kk2 += 1;}
        }
        *k1 += kk1;
        *k2 += kk2;
        *k3 += kk3;
        if (kk1+kk2+kk3==0) {cont=0;}
    }
}


void stepperD(Surpriser *sur, int *k1, int *k2, int *k3, int *k4, int *k5) {
    int ii, jj, kk, ki, i1, i2;
    int kk1, kk2, kk3, kk4, kk5;
    int cs, ci;
    int cont=1;
    //int cons[sur->K], cmax, cim=-1;
    *k1 = 0;
    *k2 = 0;
    *k3 = 0;
    *k4 = 0;
    *k5 = 0;
    while (cont) {
        kk1 = 0; //extractions
        kk2 = 0; //exchanges
        kk3 = 0; //merges
        kk4 = 0; //subcoms extract
        kk5 = 0; //subcoms exchange
        // sort communities before loop (probably not)
        for (ii=0; ii<sur->Nc; ii++) { // loop in communities
            cs = *(sur->comsizes+ii);
            for (jj=0; jj<cs; jj++) { // loop in community nodes
                i1 = *(*(sur->communities+ii) + jj);
                ki = *(sur->kis+i1);
                for (kk=0; kk<ki; kk++) { // loop in its connections
                    i2 = *(*(sur->links+i1)+kk);
                    ci = *(sur->partition+i2);
                    if (ci!=ii) {
                        if ((ii<ci)&(merger(sur, ii, ci))) { //merges
                            kk3 += 1;
                        } else if (exchanger1(sur, ii, ci, jj)) { // exchanges
                            kk2 +=1;
                        }
                    }
                }
            }
            if (kk2+kk3>0) {
                while (extractor2(sur, ii)) {kk1 += 1;} // extractions
                while (subcommuniter(sur, ii)) {kk4 += 1;} // subcommunity extractions
            }
            //
            // Subcommunities exchanges
            //
            if (kk1+kk2+kk3+kk4>0) {
                while (subcommuniter_exchange(sur, ii)) {kk5 += 1;}
                //kk5 += subcommuniter_exchange(sur, ii);
            }
        }
        *k1 += kk1;
        *k2 += kk2;
        *k3 += kk3;
        *k4 += kk4;
        *k5 += kk5;
        if (kk1+kk2+kk3+kk4+kk5==0) {cont=0;}
    }
}


void stepper0(Surpriser *sur, int *k1, int *k2) {
    int ii, jj;
    int exchs[sur->Nc];
    int subexchs[sur->Nc];
    *k1 = 0;
    *k2 = 0;
    for (ii=0; ii<sur->Nc; ii++) {exchs[ii] = 0;}
    for (ii=0; ii<sur->Nc; ii++) {subexchs[ii] = 0;}
    for (ii=0; ii<sur->Nc; ii++) {
        if (exchs[ii]==0) {
            jj = exchanger0(sur, ii);
            if (jj!=-1) {
                //printf("  community %d and %d\n", ii, jj);
                exchs[ii] = 1;
                exchs[jj] = 1;
                *k1 += 1;
            }
        }
        if (subexchs[ii]==0) {
            jj = subcommuniter_exchange0(sur, ii);
            if (jj!=-1) {
                //printf("sscommunity %d and %d\n", ii, jj);
                subexchs[ii] = 1;
                subexchs[jj] = 1;
                *k2 += 1;
            }
        }
    }
}


void stepper0nsc(Surpriser *sur, int *k1) {
    int ii, jj;
    int exchs[sur->Nc];
    *k1 = 0;
    for (ii=0; ii<sur->Nc; ii++) {exchs[ii] = 0;}
    for (ii=0; ii<sur->Nc; ii++) {
        if (exchs[ii]==0) {
            jj = exchanger0(sur, ii);
            if (jj!=-1) {
                //printf("  community %d and %d\n", ii, jj);
                exchs[ii] = 1;
                exchs[jj] = 1;
                *k1 += 1;
            }
        }
    }
}



void stepperD2(Surpriser *sur, int *k1, int *k2, int *k3) {
    int ii, jj, kk, ki, i1, i2;
    int kk1, kk2, kk3;
    int cs, ci;
    int cont=1;
    *k1 = 0;
    *k2 = 0;
    *k3 = 0;
    while (cont) {
        kk1 = 0; //extractions
        kk2 = 0; //exchanges
        kk3 = 0; //merges
        for (ii=0; ii<sur->Nc; ii++) { // loop in communities
            cs = *(sur->comsizes+ii);
            for (jj=0; jj<cs; jj++) {
                i1 = *(*(sur->communities+ii) + jj);
                ki = *(sur->kis+i1);
                for (kk=0; kk<ki; kk++) {
                    i2 = *(*(sur->links+i1)+kk);
                    ci = *(sur->partition+i2);
                    if (exchanger1(sur, ii, ci, jj)) {
                        kk2 +=1;
                    } else if ((ii<ci)&(merger(sur, ii, ci))) {
                        kk3 += 1;
                    }
                }
            }
            while (extractor2(sur, ii)) {kk1 += 1;}
        }
        *k1 += kk1;
        *k2 += kk2;
        *k3 += kk3;
        if (kk1+kk2+kk3==0) {cont=0;}
    }
}







/////







//////////


int merger_an(Surpriser *sur, int ic1, int ic2, double temp) {
    int cs1, cs2, lcs;
    int M1, M2, M3;
    int dp=0;
    int ii, jj, i1, i2;
    int toret=0;
    double nsurp;
    if (ic1==ic2) {return toret;}
    cs1 = *(sur->comsizes+ic1);
    cs2 = *(sur->comsizes+ic2);
    M1 = cs1*(cs1-1)/2;
    M2 = cs2*(cs2-1)/2;
    M3 = (cs1+cs2)*(cs1+cs2-1)/2;
    for (ii=0; ii<cs1; ii++) {
        i1 = *(*(sur->communities + ic1) + ii);
        for (jj=0; jj<cs2; jj++) {
            i2 = *(*(sur->communities + ic2) + jj);
            dp += *(sur->matr + i1* sur->K + i2);
        }
    }
    nsurp = surprise(sur->M-M1-M2+M3, sur->F, sur->nl, sur->p+dp);
    if ( (nsurp > sur->surprise) | (exp(-(sur->surprise - nsurp)/temp) > drand()) ) {
        //printf("communities %d and %d being merged! \n", ic1, ic2);
        sur->surprise = nsurp;
        sur->M += M3-M1-M2;
        sur->p += dp;
        lcs = *(sur->comsizes + sur->Nc-1);
        if (ic1<ic2) {
            for (jj=0; jj<cs2; jj++) {
                i2 = *(*(sur->communities + ic2) + jj);
                *(sur->partition+i2) = ic1;
                *(*(sur->communities + ic1) + cs1 + jj) = i2;
                if (jj<lcs) {
                    i2 = *(*(sur->communities + sur->Nc-1) + jj);
                    if (ic2!=sur->Nc-1) {*(sur->partition+i2) = ic2;}
                    *(*(sur->communities + ic2) + jj) = i2;
                    *(*(sur->communities + sur->Nc-1) + jj) = 0;
                }
            }
            for (jj=cs2; jj<lcs; jj++) {
                i2 = *(*(sur->communities + sur->Nc-1) + jj);
                if (ic2!=sur->Nc-1) {*(sur->partition+i2) = ic2;}
                *(*(sur->communities + ic2) + jj) = i2;
                *(*(sur->communities + sur->Nc-1) + jj) = 0;
            }
            *(sur->comsizes + ic1) += cs2;
            *(sur->comsizes + ic2) = *(sur->comsizes + sur->Nc-1);
            *(sur->comsizes + sur->Nc-1) = 0;
        } else {
            for (jj=0; jj<cs1; jj++) {
                i1 = *(*(sur->communities + ic1) + jj);
                *(sur->partition+i1) = ic2;
                *(*(sur->communities + ic2) + cs2 + jj) = i1;
                if (jj<lcs) {
                    i2 = *(*(sur->communities + sur->Nc-1) + jj);
                    if (ic1!=sur->Nc-1) {*(sur->partition+i2) = ic1;}
                    *(*(sur->communities + ic1) + jj) = i2;
                    *(*(sur->communities + sur->Nc-1) + jj) = 0;
                }
            }
            for (jj=cs1; jj<lcs; jj++) {
                i2 = *(*(sur->communities + sur->Nc-1) + jj);
                if (ic1!=sur->Nc-1) {*(sur->partition+i2) = ic1;}
                *(*(sur->communities + ic1) + jj) = i2;
                *(*(sur->communities + sur->Nc-1) + jj) = 0;
            }
            *(sur->comsizes + ic2) += cs1;
            *(sur->comsizes + ic1) = *(sur->comsizes + sur->Nc-1);
            *(sur->comsizes + sur->Nc-1) = 0;
        }
        sur->Nc -= 1;
        toret = 1;
    }
    return toret;
}




int exchanger_an(Surpriser *sur, int ic1, int ic2, double temp) {
    int cs1, cs2;
    int dp;
    int ii, jj, i1, i2;
    int toret=0;
    double nsurp;
    cs1 = *(sur->comsizes+ic1);
    cs2 = *(sur->comsizes+ic2);
    if ((cs1==1)|(ic1==ic2)) {return toret;}
    //for (ii=0; ii<cs1; ii++) {
    ii = cs1*drand();
        i1 = *(*(sur->communities + ic1) + ii);
        dp = 0;
        for (jj=0; jj<cs1; jj++) {
            i2 = *(*(sur->communities + ic1) + jj);
            dp -= *(sur->matr + i1* sur->K + i2);
        }
        for (jj=0; jj<cs2; jj++) {
            i2 = *(*(sur->communities + ic2) + jj);
            dp += *(sur->matr + i1* sur->K + i2);
        }
        nsurp = surprise(sur->M-cs1+1+cs2, sur->F, sur->nl, sur->p+dp);
        if ( (nsurp > sur->surprise) | (exp(-(sur->surprise - nsurp)/temp) > drand()) ) {
            //printf("Element %d (%d) from community %d being transfered to community %d! \n", i1, ii, ic1, ic2);
            sur->surprise = nsurp;
            sur->M -= cs1-1-cs2;
            sur->p += dp;
            *(*(sur->communities + ic1) + ii) = *(*(sur->communities + ic1) + cs1-1);
            *(*(sur->communities + ic1) + cs1-1) = 0;
            *(*(sur->communities + ic2) + cs2) = i1;
            *(sur->comsizes + ic1) -= 1;
            *(sur->comsizes + ic2) += 1;
            *(sur->partition+i1) = ic2;
            toret = 1;
        }
    //}
    return toret;
}

int extractor_an(Surpriser *sur, int ic1, double temp) {
    int cs1;
    int dp;
    int ii, jj, i1, i2;
    int toret=0;
    double nsurp;
    cs1 = *(sur->comsizes+ic1);
    if (cs1==1) {return toret;}
    //for (ii=0; ii<cs1; ii++) {
    ii = cs1*drand();
        i1 = *(*(sur->communities + ic1) + ii);
        dp = 0;
        for (jj=0; jj<cs1; jj++) {
            i2 = *(*(sur->communities + ic1) + jj);
            dp += *(sur->matr + i1* sur->K + i2);
        }
        nsurp = surprise(sur->M-cs1+1, sur->F, sur->nl, sur->p-dp);
        if ( (nsurp > sur->surprise) | (exp(-(sur->surprise - nsurp)/temp) > drand()) ) {
            //printf("Element %d (%d) from community %d being extracted! \n", i1, ii, ic1);
            sur->surprise = nsurp;
            sur->M -= cs1-1;
            sur->p -= dp;
            *(*(sur->communities + ic1) + ii) = *(*(sur->communities + ic1) + cs1-1);
            *(*(sur->communities + ic1) + cs1-1) = 0;
            *(*(sur->communities + sur->Nc)) = i1;
            *(sur->comsizes + ic1) -= 1;
            *(sur->comsizes + sur->Nc) = 1;
            *(sur->partition+i1) = sur->Nc;
            sur->Nc += 1;
            toret = 1;
        }
    //}
    return toret;
}


int subcommuniter_an(Surpriser *sur, int ic, double temp) {
    int cs, i1, i2, ir;
    int k1, k2, k3, k4, k5, k6;
    int scs, dp, cs2;
    int ii, jj, kk, ll;
    int toret=0;
    double nsurp;
    cs = *(sur -> comsizes + ic);
    if (cs<4) {return toret;}
    Surpriser *ssur=malloc(sizeof(Surpriser));
    int *y;
    y = calloc(cs * cs, sizeof(int));
    for (ii=0; ii<cs; ii++) {
        i1 = *(*(sur->communities + ic) + ii);
        for (jj=ii+1; jj<cs; jj++) {
            i2 = *(*(sur->communities + ic) + jj);
            *(y + ii*cs + jj) = *(sur->matr + i1* sur->K + i2);
            *(y + jj*cs + ii) = *(sur->matr + i1* sur->K + i2);
        }
    }
    generate_supriser(y, cs, NULL, NULL, ssur);
    stepper1(ssur, &k1, &k2, &k3, &k4, &k5, &k6);
    ii = ssur->Nc * drand();
    //for (ii=0; ii<ssur->Nc; ii++) { // community from ssur beeing tested
        scs = *(ssur->comsizes + ii);
        if (scs>1) {
            dp = 0;
            for (jj=0; jj<ssur->Nc; jj++) { // sums connections between ii and all other communities
                if (ii!=jj) {
                    cs2 = *(ssur->comsizes + jj);
                    for (kk=0; kk<scs; kk++) {
                        i1 = *(*(ssur->communities + ii) + kk);
                        for (ll=0; ll<cs2; ll++) {
                            i2 = *(*(ssur->communities + jj) + ll);
                            dp += *(ssur->matr + i1*ssur->K + i2);
                        }
                    }
                }
            }
            nsurp = surprise(sur->M-scs*(cs-scs), sur->F, sur->nl, sur->p-dp);
    //}
    if ( (nsurp > sur->surprise) | (exp(-(sur->surprise - nsurp)/temp) > drand()) ) {
        //printf("community %d (%d) from community %d being extracted! \n", ii, ii, ic1);
        sur->surprise = nsurp;
        sur->M -= scs*(cs-scs);
        sur->p -= dp;
        for (jj=0; jj<scs; jj++) {// New community
            i1 = *(*(ssur->communities + ii) + jj);
            ir = *(*(sur->communities + ic) + i1);
            *(*(sur->communities + sur->Nc) + jj) = ir;
            *(*(ssur->communities + ii) + jj) = ir;
            *(sur->partition+ir) = sur->Nc;
        }
        for (jj=0; jj<scs; jj++) {// fixes old com
            ir = *(*(ssur->communities + ii) + jj);
            for (kk=0; kk<cs; kk++) {// fixes ic community
                i2 = *(*(sur->communities + ic) + kk);
                if (i2==ir) {
                    *(*(sur->communities + ic) + kk) = *(*(sur->communities + ic) + cs-1-jj);
                    *(*(sur->communities + ic) + cs-1-jj) = 0;
                    //cs -= 1;
                    break;
                }
            }
        }
        *(sur->comsizes + ic) -= scs;
        *(sur->comsizes + sur->Nc) = scs;
        sur->Nc += 1;
        toret = 1;
    }
        }
    clear_surp(ssur);
    free(ssur);
    free(y);
    return toret;
}

int subcommuniter_exchange_an(Surpriser *sur, int ic, double temp) {
    int cs, i1, i2, ir, ibc;
    int k1, k2, k3, k4, k5, k6;
    int scs, dp, dps, cs2, dm, toret=0;
    int bcs;
    int ii, jj, kk, ll, mm;
    double nsurp;
    cs = *(sur -> comsizes + ic);
    if (cs<4) {return toret;}
    Surpriser *ssur=malloc(sizeof(Surpriser));
    int *y;
    y = calloc(cs * cs, sizeof(int));
    for (ii=0; ii<cs; ii++) {
        i1 = *(*(sur->communities + ic) + ii);
        for (jj=ii+1; jj<cs; jj++) {
            i2 = *(*(sur->communities + ic) + jj);
            *(y + ii*cs + jj) = *(sur->matr + i1* sur->K + i2);
            *(y + jj*cs + ii) = *(sur->matr + i1* sur->K + i2);
        }
    }
    generate_supriser(y, cs, NULL, NULL, ssur);
    stepper1(ssur, &k1, &k2, &k3, &k4, &k5, &k6);
    ii = ssur->Nc * drand();
    //for (ii=0; ii<ssur->Nc; ii++) { // community from ssur beeing tested
        scs = *(ssur->comsizes + ii);
        if (scs>1) {
            dps = 0;
            for (jj=0; jj<ssur->Nc; jj++) { // sums connections between ii and all other communities
                if (ii!=jj) {
                    cs2 = *(ssur->comsizes + jj);
                    for (kk=0; kk<scs; kk++) {
                        i1 = *(*(ssur->communities + ii) + kk);
                        for (ll=0; ll<cs2; ll++) {
                            i2 = *(*(ssur->communities + jj) + ll);
                            dps += *(ssur->matr + i1*ssur->K + i2);
                        }
                    }
                }
            }
            mm = sur->Nc * drand();
            //for (mm=0; mm<sur->Nc; mm++) {// loop in sur communities
                if (mm!=ic) {
                    bcs = *(sur->comsizes + mm);
                    dp = -dps;
                    for (jj=0; jj<bcs; jj++) { // sums connections between ii and other community
                        ibc = *(*(sur->communities + mm) + jj);
                        for (kk=0; kk<scs; kk++) {
                            i1 = *(*(sur->communities + ic) + *(*(ssur->communities + ii) + kk));
                            dp += *(sur->matr + ibc*sur->K + i1);
                        }
                    }
                    dm = -scs*(cs-scs) + scs*bcs;
                    nsurp = surprise(sur->M+dm, sur->F, sur->nl, sur->p+dp);
            //}
    //}
    if ( (nsurp > sur->surprise) | (exp(-(sur->surprise - nsurp)/temp) > drand()) ) {
        //printf("community %d (%d) from community %d being sent to %d! \n", ii, ii, ic1, mm);
        sur->surprise = nsurp;
        sur->M += dm;
        sur->p += dp;
        for (jj=0; jj<scs; jj++) {// community migrates
            i1 = *(*(ssur->communities + ii) + jj);
            ir = *(*(sur->communities + ic) + i1);
            *(*(sur->communities + mm) + jj + bcs) = ir;
            *(*(ssur->communities + ii) + jj) = ir;
            *(sur->partition+ir) = mm;
        }
        for (jj=0; jj<scs; jj++) {// fixes old com
            ir = *(*(ssur->communities + ii) + jj);
            for (kk=0; kk<cs; kk++) {// fixes ic community
                i2 = *(*(sur->communities + ic) + kk);
                if (i2==ir) {
                    *(*(sur->communities + ic) + kk) = *(*(sur->communities + ic) + cs-1-jj);
                    *(*(sur->communities + ic) + cs-1-jj) = 0;
                    //cs -= 1;
                    break;
                }
            }
        }
        *(sur->comsizes + ic) -= scs;
        *(sur->comsizes + mm) += scs;
        toret = 1;
                }
        }
    }
    clear_surp(ssur);
    free(ssur);
    free(y);
    return toret;
}


//
// Embedding
//

double dist(double *p1, double *p2) {
    return sqrt( (*p1-*p2) * (*p1-*p2) + (*(p1+1)-*(p2+1)) * (*(p1+1)-*(p2+1)) );
}


double chigrad(double *matr, double *coords, int N, double gamma, double dlim, double *grads, double *tot) {
    double chi=0., M, ddd;
    int ii, jj;
    for (ii=0; ii<N; ii++) {
        *(grads+2*ii) = 0.;
        *(grads+2*ii+1) = 0.;
    }
    *tot = 0.;
    for (ii=0; ii<N; ii++) {
        for (jj=ii+1; jj<N; jj++) {
            M = *(matr + ii*N + jj);
            if (M<dlim) {
                ddd = dist(coords+ii*2, coords+jj*2);
                chi += pow(M, gamma)*(M-ddd)*(M-ddd);
                *(grads + ii*2)     += -2.*(pow(M, gamma+1) / ddd - pow(M, gamma)) * (*(coords+ii*2) - *(coords+jj*2));
                *(grads + ii*2 + 1) += -2.*(pow(M, gamma+1) / ddd - pow(M, gamma)) * (*(coords+ii*2+1) - *(coords+jj*2+1));
            }
        }
        *tot += *(grads + ii*2) * *(grads + ii*2) + *(grads + ii*2+1) * *(grads + ii*2+1);
    }
    *tot = sqrt(*tot);
    return chi;
}




void minCoords(double *matr, double *coords, int N, double gamma, double dlim, double lamb, double adj, double eps) {
    double *grads=malloc(2*N*sizeof(double));
    double *ngrads=malloc(2*N*sizeof(double));
    double *ncoords=malloc(2*N*sizeof(double));
    double tot, ntot, chi, nchi;
    int ii, ins=0;
    
    chi = chigrad(matr, coords, N, gamma, dlim, grads, &tot);
    for (ii=0; ii<N; ii++) {
        *(ncoords+ii*2)   = *(coords+ii*2) - lamb* *(grads+ii*2)/tot ;
        *(ncoords+ii*2+1) = *(coords+ii*2+1) - lamb* *(grads+ii*2+1)/tot ;
    }
    nchi = chigrad(matr, ncoords, N, gamma, dlim, ngrads, &ntot);
    while ( (tot/(2*N) > eps) & (ins<5000) & (lamb>1.e-18) ) {
        //print lamb, norm
        if (nchi<chi) {  // accepted
            for (ii=0; ii<N; ii++) {
                *(grads+ii*2)   = *(ngrads+ii*2) ;
                *(grads+ii*2+1) = *(ngrads+ii*2+1) ;
            }
            for (ii=0; ii<N; ii++) {
                *(coords+ii*2)   = *(ncoords+ii*2) ;
                *(coords+ii*2+1) = *(ncoords+ii*2+1) ;
            }
            chi = nchi;
            tot = ntot;
            lamb *= 1.+adj;
            //adj *= (1.+adj/3.);
            //printf("down, %f, %f, %f\n", tot, lamb, tot*lamb);
            ins=0;
        } else {
            lamb *= 1.-1.1*adj;
            if (lamb<0.) {lamb=0.01*adj*drand();}
            ins+=1;
            //adj *= (1.-adj/3.);
            //printf("  up, %f, %f, %f\n", tot, lamb, tot*lamb);
        }
        for (ii=0; ii<N; ii++) {
            *(ncoords+ii*2) = *(coords+ii*2) - lamb* *(grads+ii*2)/tot ;
            *(ncoords+ii*2+1) = *(coords+ii*2+1) - lamb* *(grads+ii*2+1)/tot ;
        }
        nchi = chigrad(matr, ncoords, N, gamma, dlim, ngrads, &ntot);
    }
    free(grads);
    free(ngrads);
    free(ncoords);
}




