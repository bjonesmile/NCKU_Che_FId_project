option optcr=0;
sets
m/1*240/;
parameters
Pm/100/
Ks/10/
Ycs/0.07/
Yps/0.44/
vertex(m)
vertexT(m)
;

$if not set gdxincname $abort 'no include file name for data file provided'
$gdxin %gdxincname%
$load vertex vertexT
$gdxin

positive variables
FI
S(m)
Sa(m)
C(m)
P(m)
V(m)
Fin(m)
Fout(m)
mu(m)
mu0(m)
T(m)
;
variables
z;
equations
eq1(m)
eq2(m)
eq3(m)
eq4(m)
eq11(m)
eq12(m)

uncertanSa(m)
uncertanT(m)

Fin1(m)
Fin2(m)
Fin3(m)
Fin4(m)
Fin5(m)
Fin6(m)
Fin7(m)
Fin8(m)
Fin9(m)
Fin10(m)
Fin11(m)
Fin12(m)
Fin13(m)
Fin14(m)
Fin15(m)
Fin16(m)
Fin17(m)
Fin18(m)
Fin19(m)
Fin20(m)
Fout1(m)
Fout2(m)
Fout3(m)
Fout4(m)
Fout5(m)
Fout6(m)
Fout7(m)
Fout8(m)
Fout9(m)
Fout10(m)
Fout11(m)
Fout12(m)
Fout13(m)
Fout14(m)
Fout15(m)
Fout16(m)
Fout17(m)
Fout18(m)
Fout19(m)
Fout20(m)

obj;

eq1(m)$(ord(m) lt 240)..S(m+1)-S(m)=e=1/2*(-1/Ycs*mu(m)*C(m)+Fin(m)*Sa(m)/V(m)-Fout(m)*S(m)/V(m)
                                           -1/Ycs*mu(m+1)*C(m+1)+Fin(m+1)*Sa(m+1)/V(m+1)-Fout(m+1)*S(m+1)/V(m+1));
eq2(m)$(ord(m) lt 240)..C(m+1)-C(m)=e=1/2*(mu(m)*C(m)-Fout(m)*C(m)/V(m)
                                          +mu(m+1)*C(m+1)-Fout(m+1)*C(m+1)/V(m+1));
eq3(m)$(ord(m) lt 240)..P(m+1)-P(m)=e=1/2*(Yps/Ycs*mu(m)*C(m)-Fout(m)*P(m)/V(m)
                                          +Yps/Ycs*mu(m+1)*C(m+1)-Fout(m+1)*P(m+1)/V(m+1));
eq4(m)$(ord(m) lt 240)..V(m+1)-V(m)=e=1/2*(Fin(m)-Fout(m)
                                          +Fin(m+1)-Fout(m+1));
eq11(m)..mu(m)=e=mu0(m)*S(m)/(Ks+Sa(m))*(1-P(m)/Pm);
eq12(m)..mu0(m)=e=-0.000049205*(T(m)**4)+0.00569477*(T(m)**3)-0.24584*(T(m)**2)+4.7132*T(m)-33.435;

uncertanT(m) .. T(m)=e=(30+5*FI*vertexT(m));
uncertanSa(m) .. Sa(m)=e=(100+20*FI*vertex(m));


Fin1(m)$(ord(m) lt 12)..Fin(m)=e=Fin(m+1);
Fin2(m)$((ord(m) gt 12) and (ord(m) lt 24))..Fin(m)=e=Fin(m+1);
Fin3(m)$((ord(m) gt 24) and (ord(m) lt 36))..Fin(m)=e=Fin(m+1);
Fin4(m)$((ord(m) gt 36) and (ord(m) lt 48))..Fin(m)=e=Fin(m+1);
Fin5(m)$((ord(m) gt 48) and (ord(m) lt 60))..Fin(m)=e=Fin(m+1);
Fin6(m)$((ord(m) gt 60) and (ord(m) lt 72))..Fin(m)=e=Fin(m+1);
Fin7(m)$((ord(m) gt 72) and (ord(m) lt 84))..Fin(m)=e=Fin(m+1);
Fin8(m)$((ord(m) gt 84) and (ord(m) lt 96))..Fin(m)=e=Fin(m+1);
Fin9(m)$((ord(m) gt 96) and (ord(m) lt 108))..Fin(m)=e=Fin(m+1);
Fin10(m)$((ord(m) gt 108) and (ord(m) lt 120))..Fin(m)=e=Fin(m+1);
Fin11(m)$((ord(m) gt 120) and (ord(m) lt 132))..Fin(m)=e=Fin(m+1);
Fin12(m)$((ord(m) gt 132) and (ord(m) lt 144))..Fin(m)=e=Fin(m+1);
Fin13(m)$((ord(m) gt 144) and (ord(m) lt 156))..Fin(m)=e=Fin(m+1);
Fin14(m)$((ord(m) gt 156) and (ord(m) lt 168))..Fin(m)=e=Fin(m+1);
Fin15(m)$((ord(m) gt 168) and (ord(m) lt 180))..Fin(m)=e=Fin(m+1);
Fin16(m)$((ord(m) gt 180) and (ord(m) lt 192))..Fin(m)=e=Fin(m+1);
Fin17(m)$((ord(m) gt 192) and (ord(m) lt 204))..Fin(m)=e=Fin(m+1);
Fin18(m)$((ord(m) gt 204) and (ord(m) lt 216))..Fin(m)=e=Fin(m+1);
Fin19(m)$((ord(m) gt 216) and (ord(m) lt 228))..Fin(m)=e=Fin(m+1);
Fin20(m)$((ord(m) gt 228) and (ord(m) lt 240))..Fin(m)=e=Fin(m+1);

Fout1(m)$(ord(m) lt 12)..Fout(m)=e=Fout(m+1);
Fout2(m)$((ord(m) gt 12) and (ord(m) lt 24))..Fout(m)=e=Fout(m+1);
Fout3(m)$((ord(m) gt 24) and (ord(m) lt 32))..Fout(m)=e=Fout(m+1);
Fout4(m)$((ord(m) gt 36) and (ord(m) lt 48))..Fout(m)=e=Fout(m+1);
Fout5(m)$((ord(m) gt 48) and (ord(m) lt 60))..Fout(m)=e=Fout(m+1);
Fout6(m)$((ord(m) gt 60) and (ord(m) lt 72))..Fout(m)=e=Fout(m+1);
Fout7(m)$((ord(m) gt 72) and (ord(m) lt 84))..Fout(m)=e=Fout(m+1);
Fout8(m)$((ord(m) gt 84) and (ord(m) lt 96))..Fout(m)=e=Fout(m+1);
Fout9(m)$((ord(m) gt 96) and (ord(m) lt 108))..Fout(m)=e=Fout(m+1);
Fout10(m)$((ord(m) gt 108) and (ord(m) lt 120))..Fout(m)=e=Fout(m+1);
Fout11(m)$((ord(m) gt 120) and (ord(m) lt 132))..Fout(m)=e=Fout(m+1);
Fout12(m)$((ord(m) gt 132) and (ord(m) lt 144))..Fout(m)=e=Fout(m+1);
Fout13(m)$((ord(m) gt 144) and (ord(m) lt 156))..Fout(m)=e=Fout(m+1);
Fout14(m)$((ord(m) gt 156) and (ord(m) lt 168))..Fout(m)=e=Fout(m+1);
Fout15(m)$((ord(m) gt 168) and (ord(m) lt 180))..Fout(m)=e=Fout(m+1);
Fout16(m)$((ord(m) gt 180) and (ord(m) lt 192))..Fout(m)=e=Fout(m+1);
Fout17(m)$((ord(m) gt 192) and (ord(m) lt 204))..Fout(m)=e=Fout(m+1);
Fout18(m)$((ord(m) gt 204) and (ord(m) lt 216))..Fout(m)=e=Fout(m+1);
Fout19(m)$((ord(m) gt 216) and (ord(m) lt 228))..Fout(m)=e=Fout(m+1);
Fout20(m)$((ord(m) gt 228) and (ord(m) lt 240))..Fout(m)=e=Fout(m+1);
Fin.up(m)=0.5;
Fin.lo(m)=0;
Fout.up(m)=0.5;
Fout.lo(m)=0.05;

obj..z=e=FI;

FI.lo= 0;
FI.up= 1.0;
S.lo(m)= 0.5;
C.lo(m)= 0;
P.lo(m)= 40;
V.lo(m)= 1.5;
S.up(m)= 100;
C.up(m)= 8;
P.up(m)= 100;
V.up(m)= 3;
S.fx('1')=4.5;
C.fx('1')=5;
P.fx('1')=70;
V.fx('1')=2.0;

model tank /all/;

Scalar ms 'model status', ss 'solve status' ;
solve tank using MINLP maximizing z;
ms=tank.modelstat; ss=tank.solvestat;