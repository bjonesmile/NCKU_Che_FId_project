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
Fin51(m)
Fin52(m)
Fin53(m)
Fin54(m)
Fin55(m)
Fin56(m)
Fin57(m)
Fin58(m)
Fin59(m)
Fin60(m)
Fin61(m)
Fin62(m)
Fin63(m)
Fin64(m)
Fin65(m)
Fin66(m)
Fin67(m)
Fin68(m)
Fin69(m)
Fin70(m)
Fin71(m)
Fin72(m)
Fin73(m)
Fin74(m)
Fin75(m)
Fin76(m)
Fin77(m)
Fin78(m)
Fin79(m)
Fin80(m)
Fin81(m)
Fin82(m)
Fin83(m)
Fin84(m)
Fin85(m)
Fin86(m)
Fin87(m)
Fin88(m)
Fin89(m)
Fin90(m)
Fin91(m)
Fin92(m)
Fin93(m)
Fin94(m)
Fin95(m)
Fin96(m)
Fin97(m)
Fin98(m)
Fin99(m)
Fin100(m)
Fin101(m)
Fin102(m)
Fin103(m)
Fin104(m)
Fin105(m)
Fin106(m)
Fin107(m)
Fin108(m)
Fin109(m)
Fin110(m)
Fin111(m)
Fin112(m)
Fin113(m)
Fin114(m)
Fin115(m)
Fin116(m)
Fin117(m)
Fin118(m)
Fin119(m)
Fin120(m)
Fin121(m)
Fin122(m)
Fin123(m)
Fin124(m)
Fin125(m)
Fin126(m)
Fin127(m)
Fin128(m)
Fin129(m)
Fin130(m)
Fin131(m)
Fin132(m)
Fin133(m)
Fin134(m)
Fin135(m)
Fin136(m)
Fin137(m)
Fin138(m)
Fin139(m)
Fin140(m)
Fin141(m)
Fin142(m)
Fin143(m)
Fin144(m)
Fin145(m)
Fin146(m)
Fin147(m)
Fin148(m)
Fin149(m)
Fin150(m)
Fin151(m)
Fin152(m)
Fin153(m)
Fin154(m)
Fin155(m)
Fin156(m)
Fin157(m)
Fin158(m)
Fin159(m)
Fin160(m)
Fin161(m)
Fin162(m)
Fin163(m)
Fin164(m)
Fin165(m)
Fin166(m)
Fin167(m)
Fin168(m)
Fin169(m)
Fin170(m)
Fin171(m)
Fin172(m)
Fin173(m)
Fin174(m)
Fin175(m)
Fin176(m)
Fin177(m)
Fin178(m)
Fin179(m)
Fin180(m)
Fin181(m)
Fin182(m)
Fin183(m)
Fin184(m)
Fin185(m)
Fin186(m)
Fin187(m)
Fin188(m)
Fin189(m)
Fin190(m)
Fin191(m)
Fin192(m)
Fin193(m)
Fin194(m)
Fin195(m)
Fin196(m)
Fin197(m)
Fin198(m)
Fin199(m)
Fin200(m)
Fin201(m)
Fin202(m)
Fin203(m)
Fin204(m)
Fin205(m)
Fin206(m)
Fin207(m)
Fin208(m)
Fin209(m)
Fin210(m)
Fin211(m)
Fin212(m)
Fin213(m)
Fin214(m)
Fin215(m)
Fin216(m)
Fin217(m)
Fin218(m)
Fin219(m)
Fin220(m)
Fin221(m)
Fin222(m)
Fin223(m)
Fin224(m)
Fin225(m)
Fin226(m)
Fin227(m)
Fin228(m)
Fin229(m)
Fin230(m)
Fin231(m)
Fin232(m)
Fin233(m)
Fin234(m)
Fin235(m)
Fin236(m)
Fin237(m)
Fin238(m)
Fin239(m)
Fin240(m)

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
Fout51(m)
Fout52(m)
Fout53(m)
Fout54(m)
Fout55(m)
Fout56(m)
Fout57(m)
Fout58(m)
Fout59(m)
Fout60(m)
Fout61(m)
Fout62(m)
Fout63(m)
Fout64(m)
Fout65(m)
Fout66(m)
Fout67(m)
Fout68(m)
Fout69(m)
Fout70(m)
Fout71(m)
Fout72(m)
Fout73(m)
Fout74(m)
Fout75(m)
Fout76(m)
Fout77(m)
Fout78(m)
Fout79(m)
Fout80(m)
Fout81(m)
Fout82(m)
Fout83(m)
Fout84(m)
Fout85(m)
Fout86(m)
Fout87(m)
Fout88(m)
Fout89(m)
Fout90(m)
Fout91(m)
Fout92(m)
Fout93(m)
Fout94(m)
Fout95(m)
Fout96(m)
Fout97(m)
Fout98(m)
Fout99(m)
Fout100(m)
Fout101(m)
Fout102(m)
Fout103(m)
Fout104(m)
Fout105(m)
Fout106(m)
Fout107(m)
Fout108(m)
Fout109(m)
Fout110(m)
Fout111(m)
Fout112(m)
Fout113(m)
Fout114(m)
Fout115(m)
Fout116(m)
Fout117(m)
Fout118(m)
Fout119(m)
Fout120(m)
Fout121(m)
Fout122(m)
Fout123(m)
Fout124(m)
Fout125(m)
Fout126(m)
Fout127(m)
Fout128(m)
Fout129(m)
Fout130(m)
Fout131(m)
Fout132(m)
Fout133(m)
Fout134(m)
Fout135(m)
Fout136(m)
Fout137(m)
Fout138(m)
Fout139(m)
Fout140(m)
Fout141(m)
Fout142(m)
Fout143(m)
Fout144(m)
Fout145(m)
Fout146(m)
Fout147(m)
Fout148(m)
Fout149(m)
Fout150(m)
Fout151(m)
Fout152(m)
Fout153(m)
Fout154(m)
Fout155(m)
Fout156(m)
Fout157(m)
Fout158(m)
Fout159(m)
Fout160(m)
Fout161(m)
Fout162(m)
Fout163(m)
Fout164(m)
Fout165(m)
Fout166(m)
Fout167(m)
Fout168(m)
Fout169(m)
Fout170(m)
Fout171(m)
Fout172(m)
Fout173(m)
Fout174(m)
Fout175(m)
Fout176(m)
Fout177(m)
Fout178(m)
Fout179(m)
Fout180(m)
Fout181(m)
Fout182(m)
Fout183(m)
Fout184(m)
Fout185(m)
Fout186(m)
Fout187(m)
Fout188(m)
Fout189(m)
Fout190(m)
Fout191(m)
Fout192(m)
Fout193(m)
Fout194(m)
Fout195(m)
Fout196(m)
Fout197(m)
Fout198(m)
Fout199(m)
Fout200(m)
Fout201(m)
Fout202(m)
Fout203(m)
Fout204(m)
Fout205(m)
Fout206(m)
Fout207(m)
Fout208(m)
Fout209(m)
Fout210(m)
Fout211(m)
Fout212(m)
Fout213(m)
Fout214(m)
Fout215(m)
Fout216(m)
Fout217(m)
Fout218(m)
Fout219(m)
Fout220(m)
Fout221(m)
Fout222(m)
Fout223(m)
Fout224(m)
Fout225(m)
Fout226(m)
Fout227(m)
Fout228(m)
Fout229(m)
Fout230(m)
Fout231(m)
Fout232(m)
Fout233(m)
Fout234(m)
Fout235(m)
Fout236(m)
Fout237(m)
Fout238(m)
Fout239(m)
Fout240(m)

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

Fin1(m)$(ord(m) lt 1)..Fin(m)=e=Fin(m+1);
Fin2(m)$((ord(m) gt 1) and (ord(m) lt 2))..Fin(m)=e=Fin(m+1);
Fin3(m)$((ord(m) gt 2) and (ord(m) lt 3))..Fin(m)=e=Fin(m+1);
Fin4(m)$((ord(m) gt 3) and (ord(m) lt 4))..Fin(m)=e=Fin(m+1);
Fin5(m)$((ord(m) gt 4) and (ord(m) lt 5))..Fin(m)=e=Fin(m+1);
Fin6(m)$((ord(m) gt 5) and (ord(m) lt 6))..Fin(m)=e=Fin(m+1);
Fin7(m)$((ord(m) gt 6) and (ord(m) lt 7))..Fin(m)=e=Fin(m+1);
Fin8(m)$((ord(m) gt 7) and (ord(m) lt 8))..Fin(m)=e=Fin(m+1);
Fin9(m)$((ord(m) gt 8) and (ord(m) lt 9))..Fin(m)=e=Fin(m+1);
Fin10(m)$((ord(m) gt 9) and (ord(m) lt 10))..Fin(m)=e=Fin(m+1);
Fin11(m)$((ord(m) gt 10) and (ord(m) lt 11))..Fin(m)=e=Fin(m+1);
Fin12(m)$((ord(m) gt 11) and (ord(m) lt 12))..Fin(m)=e=Fin(m+1);
Fin13(m)$((ord(m) gt 12) and (ord(m) lt 13))..Fin(m)=e=Fin(m+1);
Fin14(m)$((ord(m) gt 13) and (ord(m) lt 14))..Fin(m)=e=Fin(m+1);
Fin15(m)$((ord(m) gt 14) and (ord(m) lt 15))..Fin(m)=e=Fin(m+1);
Fin16(m)$((ord(m) gt 15) and (ord(m) lt 16))..Fin(m)=e=Fin(m+1);
Fin17(m)$((ord(m) gt 16) and (ord(m) lt 17))..Fin(m)=e=Fin(m+1);
Fin18(m)$((ord(m) gt 17) and (ord(m) lt 18))..Fin(m)=e=Fin(m+1);
Fin19(m)$((ord(m) gt 18) and (ord(m) lt 19))..Fin(m)=e=Fin(m+1);
Fin20(m)$((ord(m) gt 19) and (ord(m) lt 20))..Fin(m)=e=Fin(m+1);
Fin21(m)$((ord(m) gt 20) and (ord(m) lt 21))..Fin(m)=e=Fin(m+1);
Fin22(m)$((ord(m) gt 21) and (ord(m) lt 22))..Fin(m)=e=Fin(m+1);
Fin23(m)$((ord(m) gt 22) and (ord(m) lt 23))..Fin(m)=e=Fin(m+1);
Fin24(m)$((ord(m) gt 23) and (ord(m) lt 24))..Fin(m)=e=Fin(m+1);
Fin25(m)$((ord(m) gt 24) and (ord(m) lt 25))..Fin(m)=e=Fin(m+1);
Fin26(m)$((ord(m) gt 25) and (ord(m) lt 26))..Fin(m)=e=Fin(m+1);
Fin27(m)$((ord(m) gt 26) and (ord(m) lt 27))..Fin(m)=e=Fin(m+1);
Fin28(m)$((ord(m) gt 27) and (ord(m) lt 28))..Fin(m)=e=Fin(m+1);
Fin29(m)$((ord(m) gt 28) and (ord(m) lt 29))..Fin(m)=e=Fin(m+1);
Fin30(m)$((ord(m) gt 29) and (ord(m) lt 30))..Fin(m)=e=Fin(m+1);
Fin31(m)$((ord(m) gt 30) and (ord(m) lt 31))..Fin(m)=e=Fin(m+1);
Fin32(m)$((ord(m) gt 31) and (ord(m) lt 32))..Fin(m)=e=Fin(m+1);
Fin33(m)$((ord(m) gt 32) and (ord(m) lt 33))..Fin(m)=e=Fin(m+1);
Fin34(m)$((ord(m) gt 33) and (ord(m) lt 34))..Fin(m)=e=Fin(m+1);
Fin35(m)$((ord(m) gt 34) and (ord(m) lt 35))..Fin(m)=e=Fin(m+1);
Fin36(m)$((ord(m) gt 35) and (ord(m) lt 36))..Fin(m)=e=Fin(m+1);
Fin37(m)$((ord(m) gt 36) and (ord(m) lt 37))..Fin(m)=e=Fin(m+1);
Fin38(m)$((ord(m) gt 37) and (ord(m) lt 38))..Fin(m)=e=Fin(m+1);
Fin39(m)$((ord(m) gt 38) and (ord(m) lt 39))..Fin(m)=e=Fin(m+1);
Fin40(m)$((ord(m) gt 39) and (ord(m) lt 40))..Fin(m)=e=Fin(m+1);
Fin41(m)$((ord(m) gt 40) and (ord(m) lt 41))..Fin(m)=e=Fin(m+1);
Fin42(m)$((ord(m) gt 41) and (ord(m) lt 42))..Fin(m)=e=Fin(m+1);
Fin43(m)$((ord(m) gt 42) and (ord(m) lt 43))..Fin(m)=e=Fin(m+1);
Fin44(m)$((ord(m) gt 43) and (ord(m) lt 44))..Fin(m)=e=Fin(m+1);
Fin45(m)$((ord(m) gt 44) and (ord(m) lt 45))..Fin(m)=e=Fin(m+1);
Fin46(m)$((ord(m) gt 45) and (ord(m) lt 46))..Fin(m)=e=Fin(m+1);
Fin47(m)$((ord(m) gt 46) and (ord(m) lt 47))..Fin(m)=e=Fin(m+1);
Fin48(m)$((ord(m) gt 47) and (ord(m) lt 48))..Fin(m)=e=Fin(m+1);
Fin49(m)$((ord(m) gt 48) and (ord(m) lt 49))..Fin(m)=e=Fin(m+1);
Fin50(m)$((ord(m) gt 49) and (ord(m) lt 50))..Fin(m)=e=Fin(m+1);
Fin51(m)$((ord(m) gt 50) and (ord(m) lt 51))..Fin(m)=e=Fin(m+1);
Fin52(m)$((ord(m) gt 51) and (ord(m) lt 52))..Fin(m)=e=Fin(m+1);
Fin53(m)$((ord(m) gt 52) and (ord(m) lt 53))..Fin(m)=e=Fin(m+1);
Fin54(m)$((ord(m) gt 53) and (ord(m) lt 54))..Fin(m)=e=Fin(m+1);
Fin55(m)$((ord(m) gt 54) and (ord(m) lt 55))..Fin(m)=e=Fin(m+1);
Fin56(m)$((ord(m) gt 55) and (ord(m) lt 56))..Fin(m)=e=Fin(m+1);
Fin57(m)$((ord(m) gt 56) and (ord(m) lt 57))..Fin(m)=e=Fin(m+1);
Fin58(m)$((ord(m) gt 57) and (ord(m) lt 58))..Fin(m)=e=Fin(m+1);
Fin59(m)$((ord(m) gt 58) and (ord(m) lt 59))..Fin(m)=e=Fin(m+1);
Fin60(m)$((ord(m) gt 59) and (ord(m) lt 60))..Fin(m)=e=Fin(m+1);
Fin61(m)$((ord(m) gt 60) and (ord(m) lt 61))..Fin(m)=e=Fin(m+1);
Fin62(m)$((ord(m) gt 61) and (ord(m) lt 62))..Fin(m)=e=Fin(m+1);
Fin63(m)$((ord(m) gt 62) and (ord(m) lt 63))..Fin(m)=e=Fin(m+1);
Fin64(m)$((ord(m) gt 63) and (ord(m) lt 64))..Fin(m)=e=Fin(m+1);
Fin65(m)$((ord(m) gt 64) and (ord(m) lt 65))..Fin(m)=e=Fin(m+1);
Fin66(m)$((ord(m) gt 65) and (ord(m) lt 66))..Fin(m)=e=Fin(m+1);
Fin67(m)$((ord(m) gt 66) and (ord(m) lt 67))..Fin(m)=e=Fin(m+1);
Fin68(m)$((ord(m) gt 67) and (ord(m) lt 68))..Fin(m)=e=Fin(m+1);
Fin69(m)$((ord(m) gt 68) and (ord(m) lt 69))..Fin(m)=e=Fin(m+1);
Fin70(m)$((ord(m) gt 69) and (ord(m) lt 70))..Fin(m)=e=Fin(m+1);
Fin71(m)$((ord(m) gt 70) and (ord(m) lt 71))..Fin(m)=e=Fin(m+1);
Fin72(m)$((ord(m) gt 71) and (ord(m) lt 72))..Fin(m)=e=Fin(m+1);
Fin73(m)$((ord(m) gt 72) and (ord(m) lt 73))..Fin(m)=e=Fin(m+1);
Fin74(m)$((ord(m) gt 73) and (ord(m) lt 74))..Fin(m)=e=Fin(m+1);
Fin75(m)$((ord(m) gt 74) and (ord(m) lt 75))..Fin(m)=e=Fin(m+1);
Fin76(m)$((ord(m) gt 75) and (ord(m) lt 76))..Fin(m)=e=Fin(m+1);
Fin77(m)$((ord(m) gt 76) and (ord(m) lt 77))..Fin(m)=e=Fin(m+1);
Fin78(m)$((ord(m) gt 77) and (ord(m) lt 78))..Fin(m)=e=Fin(m+1);
Fin79(m)$((ord(m) gt 78) and (ord(m) lt 79))..Fin(m)=e=Fin(m+1);
Fin80(m)$((ord(m) gt 79) and (ord(m) lt 80))..Fin(m)=e=Fin(m+1);
Fin81(m)$((ord(m) gt 80) and (ord(m) lt 81))..Fin(m)=e=Fin(m+1);
Fin82(m)$((ord(m) gt 81) and (ord(m) lt 82))..Fin(m)=e=Fin(m+1);
Fin83(m)$((ord(m) gt 82) and (ord(m) lt 83))..Fin(m)=e=Fin(m+1);
Fin84(m)$((ord(m) gt 83) and (ord(m) lt 84))..Fin(m)=e=Fin(m+1);
Fin85(m)$((ord(m) gt 84) and (ord(m) lt 85))..Fin(m)=e=Fin(m+1);
Fin86(m)$((ord(m) gt 85) and (ord(m) lt 86))..Fin(m)=e=Fin(m+1);
Fin87(m)$((ord(m) gt 86) and (ord(m) lt 87))..Fin(m)=e=Fin(m+1);
Fin88(m)$((ord(m) gt 87) and (ord(m) lt 88))..Fin(m)=e=Fin(m+1);
Fin89(m)$((ord(m) gt 88) and (ord(m) lt 89))..Fin(m)=e=Fin(m+1);
Fin90(m)$((ord(m) gt 89) and (ord(m) lt 90))..Fin(m)=e=Fin(m+1);
Fin91(m)$((ord(m) gt 90) and (ord(m) lt 91))..Fin(m)=e=Fin(m+1);
Fin92(m)$((ord(m) gt 91) and (ord(m) lt 92))..Fin(m)=e=Fin(m+1);
Fin93(m)$((ord(m) gt 92) and (ord(m) lt 93))..Fin(m)=e=Fin(m+1);
Fin94(m)$((ord(m) gt 93) and (ord(m) lt 94))..Fin(m)=e=Fin(m+1);
Fin95(m)$((ord(m) gt 94) and (ord(m) lt 95))..Fin(m)=e=Fin(m+1);
Fin96(m)$((ord(m) gt 95) and (ord(m) lt 96))..Fin(m)=e=Fin(m+1);
Fin97(m)$((ord(m) gt 96) and (ord(m) lt 97))..Fin(m)=e=Fin(m+1);
Fin98(m)$((ord(m) gt 97) and (ord(m) lt 98))..Fin(m)=e=Fin(m+1);
Fin99(m)$((ord(m) gt 98) and (ord(m) lt 99))..Fin(m)=e=Fin(m+1);
Fin100(m)$((ord(m) gt 99) and (ord(m) lt 100))..Fin(m)=e=Fin(m+1);
Fin101(m)$((ord(m) gt 100) and (ord(m) lt 101))..Fin(m)=e=Fin(m+1);
Fin102(m)$((ord(m) gt 101) and (ord(m) lt 102))..Fin(m)=e=Fin(m+1);
Fin103(m)$((ord(m) gt 102) and (ord(m) lt 103))..Fin(m)=e=Fin(m+1);
Fin104(m)$((ord(m) gt 103) and (ord(m) lt 104))..Fin(m)=e=Fin(m+1);
Fin105(m)$((ord(m) gt 104) and (ord(m) lt 105))..Fin(m)=e=Fin(m+1);
Fin106(m)$((ord(m) gt 105) and (ord(m) lt 106))..Fin(m)=e=Fin(m+1);
Fin107(m)$((ord(m) gt 106) and (ord(m) lt 107))..Fin(m)=e=Fin(m+1);
Fin108(m)$((ord(m) gt 107) and (ord(m) lt 108))..Fin(m)=e=Fin(m+1);
Fin109(m)$((ord(m) gt 108) and (ord(m) lt 109))..Fin(m)=e=Fin(m+1);
Fin110(m)$((ord(m) gt 109) and (ord(m) lt 110))..Fin(m)=e=Fin(m+1);
Fin111(m)$((ord(m) gt 110) and (ord(m) lt 111))..Fin(m)=e=Fin(m+1);
Fin112(m)$((ord(m) gt 111) and (ord(m) lt 112))..Fin(m)=e=Fin(m+1);
Fin113(m)$((ord(m) gt 112) and (ord(m) lt 113))..Fin(m)=e=Fin(m+1);
Fin114(m)$((ord(m) gt 113) and (ord(m) lt 114))..Fin(m)=e=Fin(m+1);
Fin115(m)$((ord(m) gt 114) and (ord(m) lt 115))..Fin(m)=e=Fin(m+1);
Fin116(m)$((ord(m) gt 115) and (ord(m) lt 116))..Fin(m)=e=Fin(m+1);
Fin117(m)$((ord(m) gt 116) and (ord(m) lt 117))..Fin(m)=e=Fin(m+1);
Fin118(m)$((ord(m) gt 117) and (ord(m) lt 118))..Fin(m)=e=Fin(m+1);
Fin119(m)$((ord(m) gt 118) and (ord(m) lt 119))..Fin(m)=e=Fin(m+1);
Fin120(m)$((ord(m) gt 119) and (ord(m) lt 120))..Fin(m)=e=Fin(m+1);
Fin121(m)$((ord(m) gt 120) and (ord(m) lt 121))..Fin(m)=e=Fin(m+1);
Fin122(m)$((ord(m) gt 121) and (ord(m) lt 122))..Fin(m)=e=Fin(m+1);
Fin123(m)$((ord(m) gt 122) and (ord(m) lt 123))..Fin(m)=e=Fin(m+1);
Fin124(m)$((ord(m) gt 123) and (ord(m) lt 124))..Fin(m)=e=Fin(m+1);
Fin125(m)$((ord(m) gt 124) and (ord(m) lt 125))..Fin(m)=e=Fin(m+1);
Fin126(m)$((ord(m) gt 125) and (ord(m) lt 126))..Fin(m)=e=Fin(m+1);
Fin127(m)$((ord(m) gt 126) and (ord(m) lt 127))..Fin(m)=e=Fin(m+1);
Fin128(m)$((ord(m) gt 127) and (ord(m) lt 128))..Fin(m)=e=Fin(m+1);
Fin129(m)$((ord(m) gt 128) and (ord(m) lt 129))..Fin(m)=e=Fin(m+1);
Fin130(m)$((ord(m) gt 129) and (ord(m) lt 130))..Fin(m)=e=Fin(m+1);
Fin131(m)$((ord(m) gt 130) and (ord(m) lt 131))..Fin(m)=e=Fin(m+1);
Fin132(m)$((ord(m) gt 131) and (ord(m) lt 132))..Fin(m)=e=Fin(m+1);
Fin133(m)$((ord(m) gt 132) and (ord(m) lt 133))..Fin(m)=e=Fin(m+1);
Fin134(m)$((ord(m) gt 133) and (ord(m) lt 134))..Fin(m)=e=Fin(m+1);
Fin135(m)$((ord(m) gt 134) and (ord(m) lt 135))..Fin(m)=e=Fin(m+1);
Fin136(m)$((ord(m) gt 135) and (ord(m) lt 136))..Fin(m)=e=Fin(m+1);
Fin137(m)$((ord(m) gt 136) and (ord(m) lt 137))..Fin(m)=e=Fin(m+1);
Fin138(m)$((ord(m) gt 137) and (ord(m) lt 138))..Fin(m)=e=Fin(m+1);
Fin139(m)$((ord(m) gt 138) and (ord(m) lt 139))..Fin(m)=e=Fin(m+1);
Fin140(m)$((ord(m) gt 139) and (ord(m) lt 140))..Fin(m)=e=Fin(m+1);
Fin141(m)$((ord(m) gt 140) and (ord(m) lt 141))..Fin(m)=e=Fin(m+1);
Fin142(m)$((ord(m) gt 141) and (ord(m) lt 142))..Fin(m)=e=Fin(m+1);
Fin143(m)$((ord(m) gt 142) and (ord(m) lt 143))..Fin(m)=e=Fin(m+1);
Fin144(m)$((ord(m) gt 143) and (ord(m) lt 144))..Fin(m)=e=Fin(m+1);
Fin145(m)$((ord(m) gt 144) and (ord(m) lt 145))..Fin(m)=e=Fin(m+1);
Fin146(m)$((ord(m) gt 145) and (ord(m) lt 146))..Fin(m)=e=Fin(m+1);
Fin147(m)$((ord(m) gt 146) and (ord(m) lt 147))..Fin(m)=e=Fin(m+1);
Fin148(m)$((ord(m) gt 147) and (ord(m) lt 148))..Fin(m)=e=Fin(m+1);
Fin149(m)$((ord(m) gt 148) and (ord(m) lt 149))..Fin(m)=e=Fin(m+1);
Fin150(m)$((ord(m) gt 149) and (ord(m) lt 150))..Fin(m)=e=Fin(m+1);
Fin151(m)$((ord(m) gt 150) and (ord(m) lt 151))..Fin(m)=e=Fin(m+1);
Fin152(m)$((ord(m) gt 151) and (ord(m) lt 152))..Fin(m)=e=Fin(m+1);
Fin153(m)$((ord(m) gt 152) and (ord(m) lt 153))..Fin(m)=e=Fin(m+1);
Fin154(m)$((ord(m) gt 153) and (ord(m) lt 154))..Fin(m)=e=Fin(m+1);
Fin155(m)$((ord(m) gt 154) and (ord(m) lt 155))..Fin(m)=e=Fin(m+1);
Fin156(m)$((ord(m) gt 155) and (ord(m) lt 156))..Fin(m)=e=Fin(m+1);
Fin157(m)$((ord(m) gt 156) and (ord(m) lt 157))..Fin(m)=e=Fin(m+1);
Fin158(m)$((ord(m) gt 157) and (ord(m) lt 158))..Fin(m)=e=Fin(m+1);
Fin159(m)$((ord(m) gt 158) and (ord(m) lt 159))..Fin(m)=e=Fin(m+1);
Fin160(m)$((ord(m) gt 159) and (ord(m) lt 160))..Fin(m)=e=Fin(m+1);
Fin161(m)$((ord(m) gt 160) and (ord(m) lt 161))..Fin(m)=e=Fin(m+1);
Fin162(m)$((ord(m) gt 161) and (ord(m) lt 162))..Fin(m)=e=Fin(m+1);
Fin163(m)$((ord(m) gt 162) and (ord(m) lt 163))..Fin(m)=e=Fin(m+1);
Fin164(m)$((ord(m) gt 163) and (ord(m) lt 164))..Fin(m)=e=Fin(m+1);
Fin165(m)$((ord(m) gt 164) and (ord(m) lt 165))..Fin(m)=e=Fin(m+1);
Fin166(m)$((ord(m) gt 165) and (ord(m) lt 166))..Fin(m)=e=Fin(m+1);
Fin167(m)$((ord(m) gt 166) and (ord(m) lt 167))..Fin(m)=e=Fin(m+1);
Fin168(m)$((ord(m) gt 167) and (ord(m) lt 168))..Fin(m)=e=Fin(m+1);
Fin169(m)$((ord(m) gt 168) and (ord(m) lt 169))..Fin(m)=e=Fin(m+1);
Fin170(m)$((ord(m) gt 169) and (ord(m) lt 170))..Fin(m)=e=Fin(m+1);
Fin171(m)$((ord(m) gt 170) and (ord(m) lt 171))..Fin(m)=e=Fin(m+1);
Fin172(m)$((ord(m) gt 171) and (ord(m) lt 172))..Fin(m)=e=Fin(m+1);
Fin173(m)$((ord(m) gt 172) and (ord(m) lt 173))..Fin(m)=e=Fin(m+1);
Fin174(m)$((ord(m) gt 173) and (ord(m) lt 174))..Fin(m)=e=Fin(m+1);
Fin175(m)$((ord(m) gt 174) and (ord(m) lt 175))..Fin(m)=e=Fin(m+1);
Fin176(m)$((ord(m) gt 175) and (ord(m) lt 176))..Fin(m)=e=Fin(m+1);
Fin177(m)$((ord(m) gt 176) and (ord(m) lt 177))..Fin(m)=e=Fin(m+1);
Fin178(m)$((ord(m) gt 177) and (ord(m) lt 178))..Fin(m)=e=Fin(m+1);
Fin179(m)$((ord(m) gt 178) and (ord(m) lt 179))..Fin(m)=e=Fin(m+1);
Fin180(m)$((ord(m) gt 179) and (ord(m) lt 180))..Fin(m)=e=Fin(m+1);
Fin181(m)$((ord(m) gt 180) and (ord(m) lt 181))..Fin(m)=e=Fin(m+1);
Fin182(m)$((ord(m) gt 181) and (ord(m) lt 182))..Fin(m)=e=Fin(m+1);
Fin183(m)$((ord(m) gt 182) and (ord(m) lt 183))..Fin(m)=e=Fin(m+1);
Fin184(m)$((ord(m) gt 183) and (ord(m) lt 184))..Fin(m)=e=Fin(m+1);
Fin185(m)$((ord(m) gt 184) and (ord(m) lt 185))..Fin(m)=e=Fin(m+1);
Fin186(m)$((ord(m) gt 185) and (ord(m) lt 186))..Fin(m)=e=Fin(m+1);
Fin187(m)$((ord(m) gt 186) and (ord(m) lt 187))..Fin(m)=e=Fin(m+1);
Fin188(m)$((ord(m) gt 187) and (ord(m) lt 188))..Fin(m)=e=Fin(m+1);
Fin189(m)$((ord(m) gt 188) and (ord(m) lt 189))..Fin(m)=e=Fin(m+1);
Fin190(m)$((ord(m) gt 189) and (ord(m) lt 190))..Fin(m)=e=Fin(m+1);
Fin191(m)$((ord(m) gt 190) and (ord(m) lt 191))..Fin(m)=e=Fin(m+1);
Fin192(m)$((ord(m) gt 191) and (ord(m) lt 192))..Fin(m)=e=Fin(m+1);
Fin193(m)$((ord(m) gt 192) and (ord(m) lt 193))..Fin(m)=e=Fin(m+1);
Fin194(m)$((ord(m) gt 193) and (ord(m) lt 194))..Fin(m)=e=Fin(m+1);
Fin195(m)$((ord(m) gt 194) and (ord(m) lt 195))..Fin(m)=e=Fin(m+1);
Fin196(m)$((ord(m) gt 195) and (ord(m) lt 196))..Fin(m)=e=Fin(m+1);
Fin197(m)$((ord(m) gt 196) and (ord(m) lt 197))..Fin(m)=e=Fin(m+1);
Fin198(m)$((ord(m) gt 197) and (ord(m) lt 198))..Fin(m)=e=Fin(m+1);
Fin199(m)$((ord(m) gt 198) and (ord(m) lt 199))..Fin(m)=e=Fin(m+1);
Fin200(m)$((ord(m) gt 199) and (ord(m) lt 200))..Fin(m)=e=Fin(m+1);
Fin201(m)$((ord(m) gt 200) and (ord(m) lt 201))..Fin(m)=e=Fin(m+1);
Fin202(m)$((ord(m) gt 201) and (ord(m) lt 202))..Fin(m)=e=Fin(m+1);
Fin203(m)$((ord(m) gt 202) and (ord(m) lt 203))..Fin(m)=e=Fin(m+1);
Fin204(m)$((ord(m) gt 203) and (ord(m) lt 204))..Fin(m)=e=Fin(m+1);
Fin205(m)$((ord(m) gt 204) and (ord(m) lt 205))..Fin(m)=e=Fin(m+1);
Fin206(m)$((ord(m) gt 205) and (ord(m) lt 206))..Fin(m)=e=Fin(m+1);
Fin207(m)$((ord(m) gt 206) and (ord(m) lt 207))..Fin(m)=e=Fin(m+1);
Fin208(m)$((ord(m) gt 207) and (ord(m) lt 208))..Fin(m)=e=Fin(m+1);
Fin209(m)$((ord(m) gt 208) and (ord(m) lt 209))..Fin(m)=e=Fin(m+1);
Fin210(m)$((ord(m) gt 209) and (ord(m) lt 210))..Fin(m)=e=Fin(m+1);
Fin211(m)$((ord(m) gt 210) and (ord(m) lt 211))..Fin(m)=e=Fin(m+1);
Fin212(m)$((ord(m) gt 211) and (ord(m) lt 212))..Fin(m)=e=Fin(m+1);
Fin213(m)$((ord(m) gt 212) and (ord(m) lt 213))..Fin(m)=e=Fin(m+1);
Fin214(m)$((ord(m) gt 213) and (ord(m) lt 214))..Fin(m)=e=Fin(m+1);
Fin215(m)$((ord(m) gt 214) and (ord(m) lt 215))..Fin(m)=e=Fin(m+1);
Fin216(m)$((ord(m) gt 215) and (ord(m) lt 216))..Fin(m)=e=Fin(m+1);
Fin217(m)$((ord(m) gt 216) and (ord(m) lt 217))..Fin(m)=e=Fin(m+1);
Fin218(m)$((ord(m) gt 217) and (ord(m) lt 218))..Fin(m)=e=Fin(m+1);
Fin219(m)$((ord(m) gt 218) and (ord(m) lt 219))..Fin(m)=e=Fin(m+1);
Fin220(m)$((ord(m) gt 219) and (ord(m) lt 220))..Fin(m)=e=Fin(m+1);
Fin221(m)$((ord(m) gt 220) and (ord(m) lt 221))..Fin(m)=e=Fin(m+1);
Fin222(m)$((ord(m) gt 221) and (ord(m) lt 222))..Fin(m)=e=Fin(m+1);
Fin223(m)$((ord(m) gt 222) and (ord(m) lt 223))..Fin(m)=e=Fin(m+1);
Fin224(m)$((ord(m) gt 223) and (ord(m) lt 224))..Fin(m)=e=Fin(m+1);
Fin225(m)$((ord(m) gt 224) and (ord(m) lt 225))..Fin(m)=e=Fin(m+1);
Fin226(m)$((ord(m) gt 225) and (ord(m) lt 226))..Fin(m)=e=Fin(m+1);
Fin227(m)$((ord(m) gt 226) and (ord(m) lt 227))..Fin(m)=e=Fin(m+1);
Fin228(m)$((ord(m) gt 227) and (ord(m) lt 228))..Fin(m)=e=Fin(m+1);
Fin229(m)$((ord(m) gt 228) and (ord(m) lt 229))..Fin(m)=e=Fin(m+1);
Fin230(m)$((ord(m) gt 229) and (ord(m) lt 230))..Fin(m)=e=Fin(m+1);
Fin231(m)$((ord(m) gt 230) and (ord(m) lt 231))..Fin(m)=e=Fin(m+1);
Fin232(m)$((ord(m) gt 231) and (ord(m) lt 232))..Fin(m)=e=Fin(m+1);
Fin233(m)$((ord(m) gt 232) and (ord(m) lt 233))..Fin(m)=e=Fin(m+1);
Fin234(m)$((ord(m) gt 233) and (ord(m) lt 234))..Fin(m)=e=Fin(m+1);
Fin235(m)$((ord(m) gt 234) and (ord(m) lt 235))..Fin(m)=e=Fin(m+1);
Fin236(m)$((ord(m) gt 235) and (ord(m) lt 236))..Fin(m)=e=Fin(m+1);
Fin237(m)$((ord(m) gt 236) and (ord(m) lt 237))..Fin(m)=e=Fin(m+1);
Fin238(m)$((ord(m) gt 237) and (ord(m) lt 238))..Fin(m)=e=Fin(m+1);
Fin239(m)$((ord(m) gt 238) and (ord(m) lt 239))..Fin(m)=e=Fin(m+1);
Fin240(m)$((ord(m) gt 239) and (ord(m) lt 240))..Fin(m)=e=Fin(m+1);

Fout1(m)$(ord(m) lt 1)..Fout(m)=e=Fout(m+1);
Fout2(m)$((ord(m) gt 1) and (ord(m) lt 2))..Fout(m)=e=Fout(m+1);
Fout3(m)$((ord(m) gt 2) and (ord(m) lt 3))..Fout(m)=e=Fout(m+1);
Fout4(m)$((ord(m) gt 3) and (ord(m) lt 4))..Fout(m)=e=Fout(m+1);
Fout5(m)$((ord(m) gt 4) and (ord(m) lt 5))..Fout(m)=e=Fout(m+1);
Fout6(m)$((ord(m) gt 5) and (ord(m) lt 6))..Fout(m)=e=Fout(m+1);
Fout7(m)$((ord(m) gt 6) and (ord(m) lt 7))..Fout(m)=e=Fout(m+1);
Fout8(m)$((ord(m) gt 7) and (ord(m) lt 8))..Fout(m)=e=Fout(m+1);
Fout9(m)$((ord(m) gt 8) and (ord(m) lt 9))..Fout(m)=e=Fout(m+1);
Fout10(m)$((ord(m) gt 9) and (ord(m) lt 10))..Fout(m)=e=Fout(m+1);
Fout11(m)$((ord(m) gt 10) and (ord(m) lt 11))..Fout(m)=e=Fout(m+1);
Fout12(m)$((ord(m) gt 11) and (ord(m) lt 12))..Fout(m)=e=Fout(m+1);
Fout13(m)$((ord(m) gt 12) and (ord(m) lt 13))..Fout(m)=e=Fout(m+1);
Fout14(m)$((ord(m) gt 13) and (ord(m) lt 14))..Fout(m)=e=Fout(m+1);
Fout15(m)$((ord(m) gt 14) and (ord(m) lt 15))..Fout(m)=e=Fout(m+1);
Fout16(m)$((ord(m) gt 15) and (ord(m) lt 16))..Fout(m)=e=Fout(m+1);
Fout17(m)$((ord(m) gt 16) and (ord(m) lt 17))..Fout(m)=e=Fout(m+1);
Fout18(m)$((ord(m) gt 17) and (ord(m) lt 18))..Fout(m)=e=Fout(m+1);
Fout19(m)$((ord(m) gt 18) and (ord(m) lt 19))..Fout(m)=e=Fout(m+1);
Fout20(m)$((ord(m) gt 19) and (ord(m) lt 20))..Fout(m)=e=Fout(m+1);
Fout21(m)$((ord(m) gt 20) and (ord(m) lt 21))..Fout(m)=e=Fout(m+1);
Fout22(m)$((ord(m) gt 21) and (ord(m) lt 22))..Fout(m)=e=Fout(m+1);
Fout23(m)$((ord(m) gt 22) and (ord(m) lt 23))..Fout(m)=e=Fout(m+1);
Fout24(m)$((ord(m) gt 23) and (ord(m) lt 24))..Fout(m)=e=Fout(m+1);
Fout25(m)$((ord(m) gt 24) and (ord(m) lt 25))..Fout(m)=e=Fout(m+1);
Fout26(m)$((ord(m) gt 25) and (ord(m) lt 26))..Fout(m)=e=Fout(m+1);
Fout27(m)$((ord(m) gt 26) and (ord(m) lt 27))..Fout(m)=e=Fout(m+1);
Fout28(m)$((ord(m) gt 27) and (ord(m) lt 28))..Fout(m)=e=Fout(m+1);
Fout29(m)$((ord(m) gt 28) and (ord(m) lt 29))..Fout(m)=e=Fout(m+1);
Fout30(m)$((ord(m) gt 29) and (ord(m) lt 30))..Fout(m)=e=Fout(m+1);
Fout31(m)$((ord(m) gt 30) and (ord(m) lt 31))..Fout(m)=e=Fout(m+1);
Fout32(m)$((ord(m) gt 31) and (ord(m) lt 32))..Fout(m)=e=Fout(m+1);
Fout33(m)$((ord(m) gt 32) and (ord(m) lt 33))..Fout(m)=e=Fout(m+1);
Fout34(m)$((ord(m) gt 33) and (ord(m) lt 34))..Fout(m)=e=Fout(m+1);
Fout35(m)$((ord(m) gt 34) and (ord(m) lt 35))..Fout(m)=e=Fout(m+1);
Fout36(m)$((ord(m) gt 35) and (ord(m) lt 36))..Fout(m)=e=Fout(m+1);
Fout37(m)$((ord(m) gt 36) and (ord(m) lt 37))..Fout(m)=e=Fout(m+1);
Fout38(m)$((ord(m) gt 37) and (ord(m) lt 38))..Fout(m)=e=Fout(m+1);
Fout39(m)$((ord(m) gt 38) and (ord(m) lt 39))..Fout(m)=e=Fout(m+1);
Fout40(m)$((ord(m) gt 39) and (ord(m) lt 40))..Fout(m)=e=Fout(m+1);
Fout41(m)$((ord(m) gt 40) and (ord(m) lt 41))..Fout(m)=e=Fout(m+1);
Fout42(m)$((ord(m) gt 41) and (ord(m) lt 42))..Fout(m)=e=Fout(m+1);
Fout43(m)$((ord(m) gt 42) and (ord(m) lt 43))..Fout(m)=e=Fout(m+1);
Fout44(m)$((ord(m) gt 43) and (ord(m) lt 44))..Fout(m)=e=Fout(m+1);
Fout45(m)$((ord(m) gt 44) and (ord(m) lt 45))..Fout(m)=e=Fout(m+1);
Fout46(m)$((ord(m) gt 45) and (ord(m) lt 46))..Fout(m)=e=Fout(m+1);
Fout47(m)$((ord(m) gt 46) and (ord(m) lt 47))..Fout(m)=e=Fout(m+1);
Fout48(m)$((ord(m) gt 47) and (ord(m) lt 48))..Fout(m)=e=Fout(m+1);
Fout49(m)$((ord(m) gt 48) and (ord(m) lt 49))..Fout(m)=e=Fout(m+1);
Fout50(m)$((ord(m) gt 49) and (ord(m) lt 50))..Fout(m)=e=Fout(m+1);
Fout51(m)$((ord(m) gt 50) and (ord(m) lt 51))..Fout(m)=e=Fout(m+1);
Fout52(m)$((ord(m) gt 51) and (ord(m) lt 52))..Fout(m)=e=Fout(m+1);
Fout53(m)$((ord(m) gt 52) and (ord(m) lt 53))..Fout(m)=e=Fout(m+1);
Fout54(m)$((ord(m) gt 53) and (ord(m) lt 54))..Fout(m)=e=Fout(m+1);
Fout55(m)$((ord(m) gt 54) and (ord(m) lt 55))..Fout(m)=e=Fout(m+1);
Fout56(m)$((ord(m) gt 55) and (ord(m) lt 56))..Fout(m)=e=Fout(m+1);
Fout57(m)$((ord(m) gt 56) and (ord(m) lt 57))..Fout(m)=e=Fout(m+1);
Fout58(m)$((ord(m) gt 57) and (ord(m) lt 58))..Fout(m)=e=Fout(m+1);
Fout59(m)$((ord(m) gt 58) and (ord(m) lt 59))..Fout(m)=e=Fout(m+1);
Fout60(m)$((ord(m) gt 59) and (ord(m) lt 60))..Fout(m)=e=Fout(m+1);
Fout61(m)$((ord(m) gt 60) and (ord(m) lt 61))..Fout(m)=e=Fout(m+1);
Fout62(m)$((ord(m) gt 61) and (ord(m) lt 62))..Fout(m)=e=Fout(m+1);
Fout63(m)$((ord(m) gt 62) and (ord(m) lt 63))..Fout(m)=e=Fout(m+1);
Fout64(m)$((ord(m) gt 63) and (ord(m) lt 64))..Fout(m)=e=Fout(m+1);
Fout65(m)$((ord(m) gt 64) and (ord(m) lt 65))..Fout(m)=e=Fout(m+1);
Fout66(m)$((ord(m) gt 65) and (ord(m) lt 66))..Fout(m)=e=Fout(m+1);
Fout67(m)$((ord(m) gt 66) and (ord(m) lt 67))..Fout(m)=e=Fout(m+1);
Fout68(m)$((ord(m) gt 67) and (ord(m) lt 68))..Fout(m)=e=Fout(m+1);
Fout69(m)$((ord(m) gt 68) and (ord(m) lt 69))..Fout(m)=e=Fout(m+1);
Fout70(m)$((ord(m) gt 69) and (ord(m) lt 70))..Fout(m)=e=Fout(m+1);
Fout71(m)$((ord(m) gt 70) and (ord(m) lt 71))..Fout(m)=e=Fout(m+1);
Fout72(m)$((ord(m) gt 71) and (ord(m) lt 72))..Fout(m)=e=Fout(m+1);
Fout73(m)$((ord(m) gt 72) and (ord(m) lt 73))..Fout(m)=e=Fout(m+1);
Fout74(m)$((ord(m) gt 73) and (ord(m) lt 74))..Fout(m)=e=Fout(m+1);
Fout75(m)$((ord(m) gt 74) and (ord(m) lt 75))..Fout(m)=e=Fout(m+1);
Fout76(m)$((ord(m) gt 75) and (ord(m) lt 76))..Fout(m)=e=Fout(m+1);
Fout77(m)$((ord(m) gt 76) and (ord(m) lt 77))..Fout(m)=e=Fout(m+1);
Fout78(m)$((ord(m) gt 77) and (ord(m) lt 78))..Fout(m)=e=Fout(m+1);
Fout79(m)$((ord(m) gt 78) and (ord(m) lt 79))..Fout(m)=e=Fout(m+1);
Fout80(m)$((ord(m) gt 79) and (ord(m) lt 80))..Fout(m)=e=Fout(m+1);
Fout81(m)$((ord(m) gt 80) and (ord(m) lt 81))..Fout(m)=e=Fout(m+1);
Fout82(m)$((ord(m) gt 81) and (ord(m) lt 82))..Fout(m)=e=Fout(m+1);
Fout83(m)$((ord(m) gt 82) and (ord(m) lt 83))..Fout(m)=e=Fout(m+1);
Fout84(m)$((ord(m) gt 83) and (ord(m) lt 84))..Fout(m)=e=Fout(m+1);
Fout85(m)$((ord(m) gt 84) and (ord(m) lt 85))..Fout(m)=e=Fout(m+1);
Fout86(m)$((ord(m) gt 85) and (ord(m) lt 86))..Fout(m)=e=Fout(m+1);
Fout87(m)$((ord(m) gt 86) and (ord(m) lt 87))..Fout(m)=e=Fout(m+1);
Fout88(m)$((ord(m) gt 87) and (ord(m) lt 88))..Fout(m)=e=Fout(m+1);
Fout89(m)$((ord(m) gt 88) and (ord(m) lt 89))..Fout(m)=e=Fout(m+1);
Fout90(m)$((ord(m) gt 89) and (ord(m) lt 90))..Fout(m)=e=Fout(m+1);
Fout91(m)$((ord(m) gt 90) and (ord(m) lt 91))..Fout(m)=e=Fout(m+1);
Fout92(m)$((ord(m) gt 91) and (ord(m) lt 92))..Fout(m)=e=Fout(m+1);
Fout93(m)$((ord(m) gt 92) and (ord(m) lt 93))..Fout(m)=e=Fout(m+1);
Fout94(m)$((ord(m) gt 93) and (ord(m) lt 94))..Fout(m)=e=Fout(m+1);
Fout95(m)$((ord(m) gt 94) and (ord(m) lt 95))..Fout(m)=e=Fout(m+1);
Fout96(m)$((ord(m) gt 95) and (ord(m) lt 96))..Fout(m)=e=Fout(m+1);
Fout97(m)$((ord(m) gt 96) and (ord(m) lt 97))..Fout(m)=e=Fout(m+1);
Fout98(m)$((ord(m) gt 97) and (ord(m) lt 98))..Fout(m)=e=Fout(m+1);
Fout99(m)$((ord(m) gt 98) and (ord(m) lt 99))..Fout(m)=e=Fout(m+1);
Fout100(m)$((ord(m) gt 99) and (ord(m) lt 100))..Fout(m)=e=Fout(m+1);
Fout101(m)$((ord(m) gt 100) and (ord(m) lt 101))..Fout(m)=e=Fout(m+1);
Fout102(m)$((ord(m) gt 101) and (ord(m) lt 102))..Fout(m)=e=Fout(m+1);
Fout103(m)$((ord(m) gt 102) and (ord(m) lt 103))..Fout(m)=e=Fout(m+1);
Fout104(m)$((ord(m) gt 103) and (ord(m) lt 104))..Fout(m)=e=Fout(m+1);
Fout105(m)$((ord(m) gt 104) and (ord(m) lt 105))..Fout(m)=e=Fout(m+1);
Fout106(m)$((ord(m) gt 105) and (ord(m) lt 106))..Fout(m)=e=Fout(m+1);
Fout107(m)$((ord(m) gt 106) and (ord(m) lt 107))..Fout(m)=e=Fout(m+1);
Fout108(m)$((ord(m) gt 107) and (ord(m) lt 108))..Fout(m)=e=Fout(m+1);
Fout109(m)$((ord(m) gt 108) and (ord(m) lt 109))..Fout(m)=e=Fout(m+1);
Fout110(m)$((ord(m) gt 109) and (ord(m) lt 110))..Fout(m)=e=Fout(m+1);
Fout111(m)$((ord(m) gt 110) and (ord(m) lt 111))..Fout(m)=e=Fout(m+1);
Fout112(m)$((ord(m) gt 111) and (ord(m) lt 112))..Fout(m)=e=Fout(m+1);
Fout113(m)$((ord(m) gt 112) and (ord(m) lt 113))..Fout(m)=e=Fout(m+1);
Fout114(m)$((ord(m) gt 113) and (ord(m) lt 114))..Fout(m)=e=Fout(m+1);
Fout115(m)$((ord(m) gt 114) and (ord(m) lt 115))..Fout(m)=e=Fout(m+1);
Fout116(m)$((ord(m) gt 115) and (ord(m) lt 116))..Fout(m)=e=Fout(m+1);
Fout117(m)$((ord(m) gt 116) and (ord(m) lt 117))..Fout(m)=e=Fout(m+1);
Fout118(m)$((ord(m) gt 117) and (ord(m) lt 118))..Fout(m)=e=Fout(m+1);
Fout119(m)$((ord(m) gt 118) and (ord(m) lt 119))..Fout(m)=e=Fout(m+1);
Fout120(m)$((ord(m) gt 119) and (ord(m) lt 120))..Fout(m)=e=Fout(m+1);
Fout121(m)$((ord(m) gt 120) and (ord(m) lt 121))..Fout(m)=e=Fout(m+1);
Fout122(m)$((ord(m) gt 121) and (ord(m) lt 122))..Fout(m)=e=Fout(m+1);
Fout123(m)$((ord(m) gt 122) and (ord(m) lt 123))..Fout(m)=e=Fout(m+1);
Fout124(m)$((ord(m) gt 123) and (ord(m) lt 124))..Fout(m)=e=Fout(m+1);
Fout125(m)$((ord(m) gt 124) and (ord(m) lt 125))..Fout(m)=e=Fout(m+1);
Fout126(m)$((ord(m) gt 125) and (ord(m) lt 126))..Fout(m)=e=Fout(m+1);
Fout127(m)$((ord(m) gt 126) and (ord(m) lt 127))..Fout(m)=e=Fout(m+1);
Fout128(m)$((ord(m) gt 127) and (ord(m) lt 128))..Fout(m)=e=Fout(m+1);
Fout129(m)$((ord(m) gt 128) and (ord(m) lt 129))..Fout(m)=e=Fout(m+1);
Fout130(m)$((ord(m) gt 129) and (ord(m) lt 130))..Fout(m)=e=Fout(m+1);
Fout131(m)$((ord(m) gt 130) and (ord(m) lt 131))..Fout(m)=e=Fout(m+1);
Fout132(m)$((ord(m) gt 131) and (ord(m) lt 132))..Fout(m)=e=Fout(m+1);
Fout133(m)$((ord(m) gt 132) and (ord(m) lt 133))..Fout(m)=e=Fout(m+1);
Fout134(m)$((ord(m) gt 133) and (ord(m) lt 134))..Fout(m)=e=Fout(m+1);
Fout135(m)$((ord(m) gt 134) and (ord(m) lt 135))..Fout(m)=e=Fout(m+1);
Fout136(m)$((ord(m) gt 135) and (ord(m) lt 136))..Fout(m)=e=Fout(m+1);
Fout137(m)$((ord(m) gt 136) and (ord(m) lt 137))..Fout(m)=e=Fout(m+1);
Fout138(m)$((ord(m) gt 137) and (ord(m) lt 138))..Fout(m)=e=Fout(m+1);
Fout139(m)$((ord(m) gt 138) and (ord(m) lt 139))..Fout(m)=e=Fout(m+1);
Fout140(m)$((ord(m) gt 139) and (ord(m) lt 140))..Fout(m)=e=Fout(m+1);
Fout141(m)$((ord(m) gt 140) and (ord(m) lt 141))..Fout(m)=e=Fout(m+1);
Fout142(m)$((ord(m) gt 141) and (ord(m) lt 142))..Fout(m)=e=Fout(m+1);
Fout143(m)$((ord(m) gt 142) and (ord(m) lt 143))..Fout(m)=e=Fout(m+1);
Fout144(m)$((ord(m) gt 143) and (ord(m) lt 144))..Fout(m)=e=Fout(m+1);
Fout145(m)$((ord(m) gt 144) and (ord(m) lt 145))..Fout(m)=e=Fout(m+1);
Fout146(m)$((ord(m) gt 145) and (ord(m) lt 146))..Fout(m)=e=Fout(m+1);
Fout147(m)$((ord(m) gt 146) and (ord(m) lt 147))..Fout(m)=e=Fout(m+1);
Fout148(m)$((ord(m) gt 147) and (ord(m) lt 148))..Fout(m)=e=Fout(m+1);
Fout149(m)$((ord(m) gt 148) and (ord(m) lt 149))..Fout(m)=e=Fout(m+1);
Fout150(m)$((ord(m) gt 149) and (ord(m) lt 150))..Fout(m)=e=Fout(m+1);
Fout151(m)$((ord(m) gt 150) and (ord(m) lt 151))..Fout(m)=e=Fout(m+1);
Fout152(m)$((ord(m) gt 151) and (ord(m) lt 152))..Fout(m)=e=Fout(m+1);
Fout153(m)$((ord(m) gt 152) and (ord(m) lt 153))..Fout(m)=e=Fout(m+1);
Fout154(m)$((ord(m) gt 153) and (ord(m) lt 154))..Fout(m)=e=Fout(m+1);
Fout155(m)$((ord(m) gt 154) and (ord(m) lt 155))..Fout(m)=e=Fout(m+1);
Fout156(m)$((ord(m) gt 155) and (ord(m) lt 156))..Fout(m)=e=Fout(m+1);
Fout157(m)$((ord(m) gt 156) and (ord(m) lt 157))..Fout(m)=e=Fout(m+1);
Fout158(m)$((ord(m) gt 157) and (ord(m) lt 158))..Fout(m)=e=Fout(m+1);
Fout159(m)$((ord(m) gt 158) and (ord(m) lt 159))..Fout(m)=e=Fout(m+1);
Fout160(m)$((ord(m) gt 159) and (ord(m) lt 160))..Fout(m)=e=Fout(m+1);
Fout161(m)$((ord(m) gt 160) and (ord(m) lt 161))..Fout(m)=e=Fout(m+1);
Fout162(m)$((ord(m) gt 161) and (ord(m) lt 162))..Fout(m)=e=Fout(m+1);
Fout163(m)$((ord(m) gt 162) and (ord(m) lt 163))..Fout(m)=e=Fout(m+1);
Fout164(m)$((ord(m) gt 163) and (ord(m) lt 164))..Fout(m)=e=Fout(m+1);
Fout165(m)$((ord(m) gt 164) and (ord(m) lt 165))..Fout(m)=e=Fout(m+1);
Fout166(m)$((ord(m) gt 165) and (ord(m) lt 166))..Fout(m)=e=Fout(m+1);
Fout167(m)$((ord(m) gt 166) and (ord(m) lt 167))..Fout(m)=e=Fout(m+1);
Fout168(m)$((ord(m) gt 167) and (ord(m) lt 168))..Fout(m)=e=Fout(m+1);
Fout169(m)$((ord(m) gt 168) and (ord(m) lt 169))..Fout(m)=e=Fout(m+1);
Fout170(m)$((ord(m) gt 169) and (ord(m) lt 170))..Fout(m)=e=Fout(m+1);
Fout171(m)$((ord(m) gt 170) and (ord(m) lt 171))..Fout(m)=e=Fout(m+1);
Fout172(m)$((ord(m) gt 171) and (ord(m) lt 172))..Fout(m)=e=Fout(m+1);
Fout173(m)$((ord(m) gt 172) and (ord(m) lt 173))..Fout(m)=e=Fout(m+1);
Fout174(m)$((ord(m) gt 173) and (ord(m) lt 174))..Fout(m)=e=Fout(m+1);
Fout175(m)$((ord(m) gt 174) and (ord(m) lt 175))..Fout(m)=e=Fout(m+1);
Fout176(m)$((ord(m) gt 175) and (ord(m) lt 176))..Fout(m)=e=Fout(m+1);
Fout177(m)$((ord(m) gt 176) and (ord(m) lt 177))..Fout(m)=e=Fout(m+1);
Fout178(m)$((ord(m) gt 177) and (ord(m) lt 178))..Fout(m)=e=Fout(m+1);
Fout179(m)$((ord(m) gt 178) and (ord(m) lt 179))..Fout(m)=e=Fout(m+1);
Fout180(m)$((ord(m) gt 179) and (ord(m) lt 180))..Fout(m)=e=Fout(m+1);
Fout181(m)$((ord(m) gt 180) and (ord(m) lt 181))..Fout(m)=e=Fout(m+1);
Fout182(m)$((ord(m) gt 181) and (ord(m) lt 182))..Fout(m)=e=Fout(m+1);
Fout183(m)$((ord(m) gt 182) and (ord(m) lt 183))..Fout(m)=e=Fout(m+1);
Fout184(m)$((ord(m) gt 183) and (ord(m) lt 184))..Fout(m)=e=Fout(m+1);
Fout185(m)$((ord(m) gt 184) and (ord(m) lt 185))..Fout(m)=e=Fout(m+1);
Fout186(m)$((ord(m) gt 185) and (ord(m) lt 186))..Fout(m)=e=Fout(m+1);
Fout187(m)$((ord(m) gt 186) and (ord(m) lt 187))..Fout(m)=e=Fout(m+1);
Fout188(m)$((ord(m) gt 187) and (ord(m) lt 188))..Fout(m)=e=Fout(m+1);
Fout189(m)$((ord(m) gt 188) and (ord(m) lt 189))..Fout(m)=e=Fout(m+1);
Fout190(m)$((ord(m) gt 189) and (ord(m) lt 190))..Fout(m)=e=Fout(m+1);
Fout191(m)$((ord(m) gt 190) and (ord(m) lt 191))..Fout(m)=e=Fout(m+1);
Fout192(m)$((ord(m) gt 191) and (ord(m) lt 192))..Fout(m)=e=Fout(m+1);
Fout193(m)$((ord(m) gt 192) and (ord(m) lt 193))..Fout(m)=e=Fout(m+1);
Fout194(m)$((ord(m) gt 193) and (ord(m) lt 194))..Fout(m)=e=Fout(m+1);
Fout195(m)$((ord(m) gt 194) and (ord(m) lt 195))..Fout(m)=e=Fout(m+1);
Fout196(m)$((ord(m) gt 195) and (ord(m) lt 196))..Fout(m)=e=Fout(m+1);
Fout197(m)$((ord(m) gt 196) and (ord(m) lt 197))..Fout(m)=e=Fout(m+1);
Fout198(m)$((ord(m) gt 197) and (ord(m) lt 198))..Fout(m)=e=Fout(m+1);
Fout199(m)$((ord(m) gt 198) and (ord(m) lt 199))..Fout(m)=e=Fout(m+1);
Fout200(m)$((ord(m) gt 199) and (ord(m) lt 200))..Fout(m)=e=Fout(m+1);
Fout201(m)$((ord(m) gt 200) and (ord(m) lt 201))..Fout(m)=e=Fout(m+1);
Fout202(m)$((ord(m) gt 201) and (ord(m) lt 202))..Fout(m)=e=Fout(m+1);
Fout203(m)$((ord(m) gt 202) and (ord(m) lt 203))..Fout(m)=e=Fout(m+1);
Fout204(m)$((ord(m) gt 203) and (ord(m) lt 204))..Fout(m)=e=Fout(m+1);
Fout205(m)$((ord(m) gt 204) and (ord(m) lt 205))..Fout(m)=e=Fout(m+1);
Fout206(m)$((ord(m) gt 205) and (ord(m) lt 206))..Fout(m)=e=Fout(m+1);
Fout207(m)$((ord(m) gt 206) and (ord(m) lt 207))..Fout(m)=e=Fout(m+1);
Fout208(m)$((ord(m) gt 207) and (ord(m) lt 208))..Fout(m)=e=Fout(m+1);
Fout209(m)$((ord(m) gt 208) and (ord(m) lt 209))..Fout(m)=e=Fout(m+1);
Fout210(m)$((ord(m) gt 209) and (ord(m) lt 210))..Fout(m)=e=Fout(m+1);
Fout211(m)$((ord(m) gt 210) and (ord(m) lt 211))..Fout(m)=e=Fout(m+1);
Fout212(m)$((ord(m) gt 211) and (ord(m) lt 212))..Fout(m)=e=Fout(m+1);
Fout213(m)$((ord(m) gt 212) and (ord(m) lt 213))..Fout(m)=e=Fout(m+1);
Fout214(m)$((ord(m) gt 213) and (ord(m) lt 214))..Fout(m)=e=Fout(m+1);
Fout215(m)$((ord(m) gt 214) and (ord(m) lt 215))..Fout(m)=e=Fout(m+1);
Fout216(m)$((ord(m) gt 215) and (ord(m) lt 216))..Fout(m)=e=Fout(m+1);
Fout217(m)$((ord(m) gt 216) and (ord(m) lt 217))..Fout(m)=e=Fout(m+1);
Fout218(m)$((ord(m) gt 217) and (ord(m) lt 218))..Fout(m)=e=Fout(m+1);
Fout219(m)$((ord(m) gt 218) and (ord(m) lt 219))..Fout(m)=e=Fout(m+1);
Fout220(m)$((ord(m) gt 219) and (ord(m) lt 220))..Fout(m)=e=Fout(m+1);
Fout221(m)$((ord(m) gt 220) and (ord(m) lt 221))..Fout(m)=e=Fout(m+1);
Fout222(m)$((ord(m) gt 221) and (ord(m) lt 222))..Fout(m)=e=Fout(m+1);
Fout223(m)$((ord(m) gt 222) and (ord(m) lt 223))..Fout(m)=e=Fout(m+1);
Fout224(m)$((ord(m) gt 223) and (ord(m) lt 224))..Fout(m)=e=Fout(m+1);
Fout225(m)$((ord(m) gt 224) and (ord(m) lt 225))..Fout(m)=e=Fout(m+1);
Fout226(m)$((ord(m) gt 225) and (ord(m) lt 226))..Fout(m)=e=Fout(m+1);
Fout227(m)$((ord(m) gt 226) and (ord(m) lt 227))..Fout(m)=e=Fout(m+1);
Fout228(m)$((ord(m) gt 227) and (ord(m) lt 228))..Fout(m)=e=Fout(m+1);
Fout229(m)$((ord(m) gt 228) and (ord(m) lt 229))..Fout(m)=e=Fout(m+1);
Fout230(m)$((ord(m) gt 229) and (ord(m) lt 230))..Fout(m)=e=Fout(m+1);
Fout231(m)$((ord(m) gt 230) and (ord(m) lt 231))..Fout(m)=e=Fout(m+1);
Fout232(m)$((ord(m) gt 231) and (ord(m) lt 232))..Fout(m)=e=Fout(m+1);
Fout233(m)$((ord(m) gt 232) and (ord(m) lt 233))..Fout(m)=e=Fout(m+1);
Fout234(m)$((ord(m) gt 233) and (ord(m) lt 234))..Fout(m)=e=Fout(m+1);
Fout235(m)$((ord(m) gt 234) and (ord(m) lt 235))..Fout(m)=e=Fout(m+1);
Fout236(m)$((ord(m) gt 235) and (ord(m) lt 236))..Fout(m)=e=Fout(m+1);
Fout237(m)$((ord(m) gt 236) and (ord(m) lt 237))..Fout(m)=e=Fout(m+1);
Fout238(m)$((ord(m) gt 237) and (ord(m) lt 238))..Fout(m)=e=Fout(m+1);
Fout239(m)$((ord(m) gt 238) and (ord(m) lt 239))..Fout(m)=e=Fout(m+1);
Fout240(m)$((ord(m) gt 239) and (ord(m) lt 240))..Fout(m)=e=Fout(m+1);

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