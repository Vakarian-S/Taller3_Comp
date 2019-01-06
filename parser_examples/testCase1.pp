ENT funcion$1[VACUO par$1, VACUO par$2, VACUO par$3]
(
ENT var$1;
ENT var$2;
ENT var$3;
var$1 = 5 + 2;
var$2 = 4 ++ var$1;
REP (
    var$3 = var$3 + var$2;
    MIENTRAS[var$3 LT 50](
        var$4 = var$2 -- var$3;
    )
)
funcion$2[];

)