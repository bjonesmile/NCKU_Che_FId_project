        Sets
            m      discretize of time horizon /1*800/;
        Parameters
            A1     bottom area of tank1    /5/
            A2     bottom area of tank2    /5/
            h1_0     initial value for stata var tank1 height /3.0/
            h2_0     initial value for stata var tank2 height /5.0/
            R1     R1 linear scale const /10/
            R2     R2 linear scale const /20/
            qout   downstream-demand flowrate /0.4/
            vertex(m)

$if not set gdxincname $abort 'no include file name for data file provided'
$gdxin %gdxincname%
$load vertex
$gdxin
;
        Variables
            qin(m)      flow rate of water into of tank1 controlled by valve
            z           object function
            FId         flexibility index
            ;
        Positive Variable
            h1(m)       height of tank1
            h2(m)       height of tank2
            theta(m)    uncertainty parameter
            ;
        Equations
            tank1_eq(m) 'A1*dh/dt=qin+q2-q1'
            tank2_eq(m) 'A2*dh/dt=theta-q2-qout'
            uncertain(m)
            qin1(m)
            qin2(m)
            qin3(m)
            obj;
            ;
        tank1_eq(m)$(ord(m) lt 800) ..   A1*(h1(m+1)-h1(m)) =e=  1/2*(qin(m+1)+(h2(m+1)-h1(m+1))/R2-h1(m+1)/R1+qin(m)+(h2(m)-h1(m))/R2-h1(m)/R1);
        tank2_eq(m)$(ord(m) lt 800) ..   A2*(h2(m+1)-h2(m)) =e=  1/2*(theta(m+1)-(h2(m+1)-h1(m+1))/R2-qout+theta(m)-(h2(m)-h1(m))/R2-qout);
        uncertain(m) .. theta(m) =e= (0.5+0.5*FId*vertex(m)) ;

        qin1(m)$(ord(m) lt 267) ..  qin(m+1) =e= qin(m) ;
        qin2(m)$((ord(m) gt 267) and (ord(m) lt 534)) ..  qin(m+1) =e= qin(m) ;
        qin3(m)$((ord(m) gt 534) and (ord(m) lt 800)) ..  qin(m+1) =e= qin(m) ;
        qin.up(m) = 0.4;
        qin.lo(m) = 0.0;

        FId.lo = 0;
        FId.up = 1.0;
        h1.lo(m) = 1.0;
        h1.up(m) = 10.0;
        h2.lo(m) = 1.0;
        h2.up(m) = 10.0;
        h1.fx('1') = h1_0;
        h2.fx('1') = h2_0;

        obj .. z =e= FId ;
        Model double_tank /all/ ;
        Scalar ms 'model status', ss 'solve status' ;
        Solve double_tank using minlp maximizing z ;
        ms=double_tank.modelstat; ss=double_tank.solvestat;