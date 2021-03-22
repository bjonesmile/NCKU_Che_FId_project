import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import math

def u0_func(T):
    return -0.000049205*(T**4)+0.00569477*(T**3)-0.24584*(T**2)+4.7132*T-33.435
FId = 0.2393
T_n = 22
T_d = 4
Tn = T_n-T_d*FId
T=Tn
mu0n = -0.000049205*(T**4)+0.00569477*(T**3)-0.24584*(T**2)+4.7132*T-33.435
Tp = T_n+T_d*FId
T=Tp
mu0p = -0.000049205*(T**4)+0.00569477*(T**3)-0.24584*(T**2)+4.7132*T-33.435
print("up bound temp:",Tp,"to",Tn)
print("original temp func:")
print("+:",mu0n)
print("-:",mu0p)
u_list = []
T_list = np.arange(10,35)
print(math.sqrt(4))
for t in T_list:
    print(t,u0_func(t))
    u_list.append(u0_func(t))
plt.plot(T_list,u_list)
plt.show()

# sqrt(p) = m*(T-Tmin)
m = 0.0218
Tmin = 1.37
mu0n = (m*(Tn-Tmin))**2
mu0p = (m*(Tp-Tmin))**2
print("new temp func:")
print("+:",mu0n)
print("-:",mu0p)

exit()

mu_max = [0.004,0.020,0.057,0.098,0.164,0.389]
T_ary = [4,8,12,16,20,30]
T_ary = np.array(T_ary)
mu_max_sqrt = np.sqrt(mu_max)
y = mu_max_sqrt
x = T_ary.reshape((-1,1))
model = LinearRegression().fit(x, y)
r_sq = model.score(x, y)
print('coefficient of determination:', r_sq)
print('intercept:', model.intercept_)
print('slope:', model.coef_)

y_pred = model.predict(x)
y_pred = np.square(y_pred)
print(y_pred)

test_x = np.linspace(-9,30,num=40,endpoint=True).reshape((-1,1))
y_pred = model.predict(test_x)
y_pred = np.square(y_pred).reshape((-1,1))
result = np.hstack((test_x,y_pred))
print(result)