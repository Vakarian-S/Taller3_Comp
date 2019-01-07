VACUO a;
ENT b[ENT c, VACUO d, ENT d](
ENT a;
VACUO a;
)
ENT e[VACUO f, VACUO g](
ENT h;
VACUO a;
h = 2;
a = h = 5;
h + a;
)
ENT e[VACUO f, ENT g](
z;
1;
ret;
)
ENT e[VACUO](
    ENT ida;
    ENT idb;
    SI[ida = idb](
    ida = ida + 4;
    )SINO(
    ida = idb + idc;
    )

    MIENTRAS[1] ida;
)
ENT e[VACUO](
    ENT idc;
    REP(
        ENT idd;
        idc = idd + ide;
    )
    RET idd;
    RET ide;
)
VACUO g[ENT i$1](
    VACUO abc;
    i$2<5> = 5;
    ![i$5];
    ![2];
    ![![i$7] && i$8];
    5 && ![5+i$10];
    5 LT i$100;
    i$50 EQ 100;
)
