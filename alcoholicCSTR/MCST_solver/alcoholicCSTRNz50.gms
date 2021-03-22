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
Fin21(m)
Fin22(m)
Fin23(m)
Fin24(m)
Fin25(m)
Fin26(m)
Fin27(m)
Fin28(m)
Fin29(m)
Fin30(m)
Fin31(m)
Fin32(m)
Fin33(m)
Fin34(m)
Fin35(m)
Fin36(m)
Fin37(m)
Fin38(m)
Fin39(m)
Fin40(m)
Fin41(m)
Fin42(m)
Fin43(m)
Fin44(m)
Fin45(m)
Fin46(m)
Fin47(m)
Fin48(m)
Fin49(m)
Fin50(m)

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
Fout21(m)
Fout22(m)
Fout23(m)
Fout24(m)
Fout25(m)
Fout26(m)
Fout27(m)
Fout28(m)
Fout29(m)
Fout30(m)
Fout31(m)
Fout32(m)
Fout33(m)
Fout34(m)
Fout35(m)
Fout36(m)
Fout37(m)
Fout38(m)
Fout39(m)
Fout40(m)
Fout41(m)
Fout42(m)
Fout43(m)
Fout44(m)
Fout45(m)
Fout46(m)
Fout47(m)
Fout48(m)
Fout49(m)
Fout50(m)

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

Fin1(m)$(ord(m) lt 4)..Fin(m)=e=Fin(m+1);
Fin2(m)$((ord(m) gt 4) and (ord(m) lt 8))..Fin(m)=e=Fin(m+1);
Fin3(m)$((ord(m) gt 8) and (ord(m) lt 13))..Fin(m)=e=Fin(m+1);
Fin4(m)$((ord(m) gt 13) and (ord(m) lt 18))..Fin(m)=e=Fin(m+1);
Fin5(m)$((ord(m) gt 18) and (ord(m) lt 23))..Fin(m)=e=Fin(m+1);
Fin6(m)$((ord(m) gt 23) and (ord(m) lt 28))..Fin(m)=e=Fin(m+1);
Fin7(m)$((ord(m) gt 28) and (ord(m) lt 32))..Fin(m)=e=Fin(m+1);
Fin8(m)$((ord(m) gt 32) and (ord(m) lt 37))..Fin(m)=e=Fin(m+1);
Fin9(m)$((ord(m) gt 37) and (ord(m) lt 42))..Fin(m)=e=Fin(m+1);
Fin10(m)$((ord(m) gt 42) and (ord(m) lt 47))..Fin(m)=e=Fin(m+1);
Fin11(m)$((ord(m) gt 47) and (ord(m) lt 52))..Fin(m)=e=Fin(m+1);
Fin12(m)$((ord(m) gt 52) and (ord(m) lt 56))..Fin(m)=e=Fin(m+1);
Fin13(m)$((ord(m) gt 56) and (ord(m) lt 61))..Fin(m)=e=Fin(m+1);
Fin14(m)$((ord(m) gt 61) and (ord(m) lt 66))..Fin(m)=e=Fin(m+1);
Fin15(m)$((ord(m) gt 66) and (ord(m) lt 71))..Fin(m)=e=Fin(m+1);
Fin16(m)$((ord(m) gt 71) and (ord(m) lt 76))..Fin(m)=e=Fin(m+1);
Fin17(m)$((ord(m) gt 76) and (ord(m) lt 81))..Fin(m)=e=Fin(m+1);
Fin18(m)$((ord(m) gt 81) and (ord(m) lt 85))..Fin(m)=e=Fin(m+1);
Fin19(m)$((ord(m) gt 85) and (ord(m) lt 90))..Fin(m)=e=Fin(m+1);
Fin20(m)$((ord(m) gt 90) and (ord(m) lt 95))..Fin(m)=e=Fin(m+1);
Fin21(m)$((ord(m) gt 95) and (ord(m) lt 100))..Fin(m)=e=Fin(m+1);
Fin22(m)$((ord(m) gt 100) and (ord(m) lt 105))..Fin(m)=e=Fin(m+1);
Fin23(m)$((ord(m) gt 105) and (ord(m) lt 109))..Fin(m)=e=Fin(m+1);
Fin24(m)$((ord(m) gt 109) and (ord(m) lt 114))..Fin(m)=e=Fin(m+1);
Fin25(m)$((ord(m) gt 114) and (ord(m) lt 119))..Fin(m)=e=Fin(m+1);
Fin26(m)$((ord(m) gt 119) and (ord(m) lt 124))..Fin(m)=e=Fin(m+1);
Fin27(m)$((ord(m) gt 124) and (ord(m) lt 129))..Fin(m)=e=Fin(m+1);
Fin28(m)$((ord(m) gt 129) and (ord(m) lt 134))..Fin(m)=e=Fin(m+1);
Fin29(m)$((ord(m) gt 134) and (ord(m) lt 138))..Fin(m)=e=Fin(m+1);
Fin30(m)$((ord(m) gt 138) and (ord(m) lt 143))..Fin(m)=e=Fin(m+1);
Fin31(m)$((ord(m) gt 143) and (ord(m) lt 148))..Fin(m)=e=Fin(m+1);
Fin32(m)$((ord(m) gt 148) and (ord(m) lt 153))..Fin(m)=e=Fin(m+1);
Fin33(m)$((ord(m) gt 153) and (ord(m) lt 158))..Fin(m)=e=Fin(m+1);
Fin34(m)$((ord(m) gt 158) and (ord(m) lt 162))..Fin(m)=e=Fin(m+1);
Fin35(m)$((ord(m) gt 162) and (ord(m) lt 167))..Fin(m)=e=Fin(m+1);
Fin36(m)$((ord(m) gt 167) and (ord(m) lt 172))..Fin(m)=e=Fin(m+1);
Fin37(m)$((ord(m) gt 172) and (ord(m) lt 177))..Fin(m)=e=Fin(m+1);
Fin38(m)$((ord(m) gt 177) and (ord(m) lt 182))..Fin(m)=e=Fin(m+1);
Fin39(m)$((ord(m) gt 182) and (ord(m) lt 187))..Fin(m)=e=Fin(m+1);
Fin40(m)$((ord(m) gt 187) and (ord(m) lt 191))..Fin(m)=e=Fin(m+1);
Fin41(m)$((ord(m) gt 191) and (ord(m) lt 196))..Fin(m)=e=Fin(m+1);
Fin42(m)$((ord(m) gt 196) and (ord(m) lt 201))..Fin(m)=e=Fin(m+1);
Fin43(m)$((ord(m) gt 201) and (ord(m) lt 206))..Fin(m)=e=Fin(m+1);
Fin44(m)$((ord(m) gt 206) and (ord(m) lt 211))..Fin(m)=e=Fin(m+1);
Fin45(m)$((ord(m) gt 211) and (ord(m) lt 215))..Fin(m)=e=Fin(m+1);
Fin46(m)$((ord(m) gt 215) and (ord(m) lt 220))..Fin(m)=e=Fin(m+1);
Fin47(m)$((ord(m) gt 220) and (ord(m) lt 225))..Fin(m)=e=Fin(m+1);
Fin48(m)$((ord(m) gt 225) and (ord(m) lt 230))..Fin(m)=e=Fin(m+1);
Fin49(m)$((ord(m) gt 230) and (ord(m) lt 235))..Fin(m)=e=Fin(m+1);
Fin50(m)$((ord(m) gt 235) and (ord(m) lt 240))..Fin(m)=e=Fin(m+1);

Fout1(m)$(ord(m) lt 4)..Fout(m)=e=Fout(m+1);
Fout2(m)$((ord(m) gt 4) and (ord(m) lt 8))..Fout(m)=e=Fout(m+1);
Fout3(m)$((ord(m) gt 8) and (ord(m) lt 13))..Fout(m)=e=Fout(m+1);
Fout4(m)$((ord(m) gt 13) and (ord(m) lt 18))..Fout(m)=e=Fout(m+1);
Fout5(m)$((ord(m) gt 18) and (ord(m) lt 23))..Fout(m)=e=Fout(m+1);
Fout6(m)$((ord(m) gt 23) and (ord(m) lt 28))..Fout(m)=e=Fout(m+1);
Fout7(m)$((ord(m) gt 28) and (ord(m) lt 32))..Fout(m)=e=Fout(m+1);
Fout8(m)$((ord(m) gt 32) and (ord(m) lt 37))..Fout(m)=e=Fout(m+1);
Fout9(m)$((ord(m) gt 37) and (ord(m) lt 42))..Fout(m)=e=Fout(m+1);
Fout10(m)$((ord(m) gt 42) and (ord(m) lt 47))..Fout(m)=e=Fout(m+1);
Fout11(m)$((ord(m) gt 47) and (ord(m) lt 52))..Fout(m)=e=Fout(m+1);
Fout12(m)$((ord(m) gt 52) and (ord(m) lt 56))..Fout(m)=e=Fout(m+1);
Fout13(m)$((ord(m) gt 56) and (ord(m) lt 61))..Fout(m)=e=Fout(m+1);
Fout14(m)$((ord(m) gt 61) and (ord(m) lt 66))..Fout(m)=e=Fout(m+1);
Fout15(m)$((ord(m) gt 66) and (ord(m) lt 71))..Fout(m)=e=Fout(m+1);
Fout16(m)$((ord(m) gt 71) and (ord(m) lt 76))..Fout(m)=e=Fout(m+1);
Fout17(m)$((ord(m) gt 76) and (ord(m) lt 81))..Fout(m)=e=Fout(m+1);
Fout18(m)$((ord(m) gt 81) and (ord(m) lt 85))..Fout(m)=e=Fout(m+1);
Fout19(m)$((ord(m) gt 85) and (ord(m) lt 90))..Fout(m)=e=Fout(m+1);
Fout20(m)$((ord(m) gt 90) and (ord(m) lt 95))..Fout(m)=e=Fout(m+1);
Fout21(m)$((ord(m) gt 95) and (ord(m) lt 100))..Fout(m)=e=Fout(m+1);
Fout22(m)$((ord(m) gt 100) and (ord(m) lt 105))..Fout(m)=e=Fout(m+1);
Fout23(m)$((ord(m) gt 105) and (ord(m) lt 109))..Fout(m)=e=Fout(m+1);
Fout24(m)$((ord(m) gt 109) and (ord(m) lt 114))..Fout(m)=e=Fout(m+1);
Fout25(m)$((ord(m) gt 114) and (ord(m) lt 119))..Fout(m)=e=Fout(m+1);
Fout26(m)$((ord(m) gt 119) and (ord(m) lt 124))..Fout(m)=e=Fout(m+1);
Fout27(m)$((ord(m) gt 124) and (ord(m) lt 129))..Fout(m)=e=Fout(m+1);
Fout28(m)$((ord(m) gt 129) and (ord(m) lt 134))..Fout(m)=e=Fout(m+1);
Fout29(m)$((ord(m) gt 134) and (ord(m) lt 138))..Fout(m)=e=Fout(m+1);
Fout30(m)$((ord(m) gt 138) and (ord(m) lt 143))..Fout(m)=e=Fout(m+1);
Fout31(m)$((ord(m) gt 143) and (ord(m) lt 148))..Fout(m)=e=Fout(m+1);
Fout32(m)$((ord(m) gt 148) and (ord(m) lt 153))..Fout(m)=e=Fout(m+1);
Fout33(m)$((ord(m) gt 153) and (ord(m) lt 158))..Fout(m)=e=Fout(m+1);
Fout34(m)$((ord(m) gt 158) and (ord(m) lt 162))..Fout(m)=e=Fout(m+1);
Fout35(m)$((ord(m) gt 162) and (ord(m) lt 167))..Fout(m)=e=Fout(m+1);
Fout36(m)$((ord(m) gt 167) and (ord(m) lt 172))..Fout(m)=e=Fout(m+1);
Fout37(m)$((ord(m) gt 172) and (ord(m) lt 177))..Fout(m)=e=Fout(m+1);
Fout38(m)$((ord(m) gt 177) and (ord(m) lt 182))..Fout(m)=e=Fout(m+1);
Fout39(m)$((ord(m) gt 182) and (ord(m) lt 187))..Fout(m)=e=Fout(m+1);
Fout40(m)$((ord(m) gt 187) and (ord(m) lt 191))..Fout(m)=e=Fout(m+1);
Fout41(m)$((ord(m) gt 191) and (ord(m) lt 196))..Fout(m)=e=Fout(m+1);
Fout42(m)$((ord(m) gt 196) and (ord(m) lt 201))..Fout(m)=e=Fout(m+1);
Fout43(m)$((ord(m) gt 201) and (ord(m) lt 206))..Fout(m)=e=Fout(m+1);
Fout44(m)$((ord(m) gt 206) and (ord(m) lt 211))..Fout(m)=e=Fout(m+1);
Fout45(m)$((ord(m) gt 211) and (ord(m) lt 215))..Fout(m)=e=Fout(m+1);
Fout46(m)$((ord(m) gt 215) and (ord(m) lt 220))..Fout(m)=e=Fout(m+1);
Fout47(m)$((ord(m) gt 220) and (ord(m) lt 225))..Fout(m)=e=Fout(m+1);
Fout48(m)$((ord(m) gt 225) and (ord(m) lt 230))..Fout(m)=e=Fout(m+1);
Fout49(m)$((ord(m) gt 230) and (ord(m) lt 235))..Fout(m)=e=Fout(m+1);
Fout50(m)$((ord(m) gt 235) and (ord(m) lt 240))..Fout(m)=e=Fout(m+1);

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