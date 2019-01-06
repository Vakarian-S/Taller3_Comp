ENT aNumber1;
ENT aNumber2;
ENT anArray<123>;
VACUO aVariable;
VACUO anotherArray<234>;

VACUO aProcedure1 [VACUO]
(
)

VACUO aProcedure2 [ VACUO]
(
    ;
)

ENT aProcedure3 [ VACUO ]
(
    ; ; ; ; ;
)

ENT aProcedure4 [ ENT a1, VACUO a2, ENT aa1<>, VACUO aa2<> ]
(
)

ENT aProcedure4 [ VACUO aNum1, VACUO aNum2, ENT anArray1<>, VACUO anArray2<> ]
(
)

ENT aProcedure4 [ ENT aNum1, VACUO aNum2, ENT anArray1<> ]
(
)

ENT aProcedure4 [ ENT aNum1, VACUO aNum2, ENT anArray1<>, VACUO anArray2<>, ENT a1 ]
(
    ENT aNum3;
    ENT anArray3<456>;
    VACUO aNum4;
    VACUO anArray4<78>;
    ENT aNum5;
    aNum3 = aNum1;
    aNum2 = aNum3 + 01;
    anArray3<00> = anArray1<02>;
    anArray2<03> = anarray3<04>;
    ; ;
    02 + 03 -- 01 - 21;
    ((()))
    (![01 && ![02] && 01];)
    MIENTRAS [aNum3 LT aNum4]
        ;
    MIENTRAS [aNum3+02 EQ 03++aNum5]
    (
        RET;
    )
    SI [23]
        ;
    SI [aNum5]
        ;
    SINO
        ;
    SI [05++aNum5-04 LT aNum3+02++[aNum5--03 - 07]]
        aNum5 = 03 ++ aNum5;
    SI [[aNum5 - aNum3] ++ [aNum5--03 + 04++aNum3]]
    (
        output[aNum3];
    )
    SINO
    (
        aNum4 = input[];
        RET aNum3;
    )
    RET 05 -- 00;
)


VACUO main [ VACUO ]
(
    ENT aNumber1;
    aProcedure1 [ ];
    aProcedure12 [ ];
    aProcedure1 [ aNumber1 ];
)
