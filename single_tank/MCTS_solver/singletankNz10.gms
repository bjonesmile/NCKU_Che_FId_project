Sets
            m      discretize of time horizon /1*800/;
        Parameters
            A      bottom area of tank    /5/
            h0     initial value for stata var h /5.0/
            vertex(m)

$if not set gdxincname $abort 'no include file name for data file provided'
$gdxin %gdxincname%
$load vertex
$gdxin

        Variables
            qout(m)     flow rate of water out of tank controlled by valve
            z           object function
            FId         flexibility index
            ;
        Positive Variable
            h(m)        height of tank
            theta(m)    uncertainty parameter
            ;
        Equations
            eq(m)       'A*dh/dt=theta-qout'
            ineq1(m)    h upper-bound
            ineq2(m)    h lowwer-bound
            ineq3(m)    qout upper-bound
            ineq4(m)    qout lowwer-bound
            uncertain(m)
            qout1(m)
            qout2(m)
            qout3(m)
            qout4(m)
            qout5(m)
            qout6(m)
            qout7(m)
            qout8(m)
            qout9(m)
            qout10(m)
            obj;
            ;
        eq(m)$(ord(m) lt 800) ..   A*(h(m+1)-h(m)) =e=  1/2*(theta(m+1)-qout(m+1)+theta(m)-qout(m)) ;
        uncertain(m) ..            theta(m) =e= (0.5+0.5*FId*vertex(m)) ;
        ineq1(m) ..                h(m) =l= 10 ;
        ineq2(m) ..                h(m) =g= 1 ;
        ineq3(m) ..                qout(m) =l= 0.7 ;
        ineq4(m) ..                qout(m) =g= 0 ;

        qout1(m)$(ord(m) lt 80) ..    qout(m+1) =e= qout(m) ;
        qout2(m)$((ord(m) gt 80) and (ord(m) lt 160)) ..    qout(m+1) =e= qout(m) ;
        qout3(m)$((ord(m) gt 160) and (ord(m) lt 240)) ..    qout(m+1) =e= qout(m) ;
        qout4(m)$((ord(m) gt 240) and (ord(m) lt 320)) ..    qout(m+1) =e= qout(m) ;
        qout5(m)$((ord(m) gt 320) and (ord(m) lt 400)) ..    qout(m+1) =e= qout(m) ;
        qout6(m)$((ord(m) gt 400) and (ord(m) lt 480)) ..    qout(m+1) =e= qout(m) ;
        qout7(m)$((ord(m) gt 480) and (ord(m) lt 560)) ..    qout(m+1) =e= qout(m) ;
        qout8(m)$((ord(m) gt 560) and (ord(m) lt 640)) ..    qout(m+1) =e= qout(m) ;
        qout9(m)$((ord(m) gt 640) and (ord(m) lt 720)) ..    qout(m+1) =e= qout(m) ;
        qout10(m)$((ord(m) gt 720) and (ord(m) lt 800)) ..    qout(m+1) =e= qout(m) ;
        h.fx('1') = h0;

        obj .. z =e= FId ;
        Model single_tankNz1 /all/ ;
        Scalar ms 'model status', ss 'solve status' ;
        Solve single_tankNz1 using minlp maximizing z ;
        ms=single_tankNz1.modelstat; ss=single_tankNz1.solvestat;
        