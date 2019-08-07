import math

"""
Функция sgd получает на вход координаты точки, азимутальное направление
и расстояние до второй точки. Возвращает координаты второй точки
"""
def sgd (azimuth = 221.693, lat = 55.751052, lon = 37.623968, s = 755092):

    b = 6356863.019
    e = 0.0066934216
    e2 = 0.0067385254
    ro = 206264.80624709

    u = []
    m = []
    kf = []
    r = []
    temp = []
    B = []
    L = []
    A = []

    B.append(lat * math.pi/180)
    L.append(lon * math.pi/180)
    A.append(azimuth * math.pi/180)

    u.append(math.atan(math.sqrt(1 - e) * math.tan(B[0])))
    m.append(math.atan(math.tan(u[0]) / math.cos(A[0])))
    m.append(math.asin(math.sin(A[0]) * math.cos(u[0])))
    k = math.sqrt(e2 * math.cos(m[1]) * math.cos(m[1]))

    r.append(1+k*k/4-(3*math.pow(k,4))/64)
    r.append(math.pow(k,2) / 4-math.pow(k,4)/16)
    r.append(math.pow(k,4) / 128)

    alpha = ro / (b*r[0])
    beta = r[1]/r[0]
    gamma = r[2]/r[0]

    kf.append((0.5+e/8-e/16*math.cos(m[1])*math.cos(m[1]))*e)
    kf.append((math.cos(m[1])*math.cos(m[1])*ro*math.pow(e,2))/16)

    temp.append((alpha*s)/3600*math.pi/180)
    temp.append(temp[0]+beta*math.sin(temp[0])*math.cos(2*m[0]+temp[0]))
    temp.append(temp[0]+beta*math.sin(temp[1])*math.cos(2*m[0]+temp[1])
            +gamma*math.sin(2*temp[1])*math.cos(4*m[0]+2*temp[1]))
    temp.append(temp[0]+beta*math.sin(temp[2])*math.cos(2*m[0]+temp[2])
            +gamma*math.sin(2*temp[2])*math.cos(4*m[0]+2*temp[2]))

    while math.fabs(temp[2]-temp[3]) > 0.001:
        temp[2] = temp[3]
        temp[3] = temp[0]+beta*math.sin(temp[2])*math.cos(2*m[0]+temp[2])+gamma*math.sin(2*temp[2])*math.cos(4*m[0]+2*temp[2])
    sigma = temp[3]

    u.append(math.asin(math.cos(m[1])*math.sin(m[0]+sigma)))
    A.append(math.asin(math.sin(m[1])/math.cos(u[1])))

    if A[1] > 0:
        A[1] += math.pi
    if A[1] < 0:
        A[1] = math.fabs(A[1])

    omega = math.asin((math.sin(sigma)*math.sin(A[0]))/math.cos(u[1]))

    dl = omega-math.sin(m[1])*(kf[0]*sigma++kf[1]*math.sin(sigma)
        *math.cos(2*m[0]+sigma))

    L.append(L[0]+dl)
    B.append(math.fabs(math.atan(math.tan(u[1])/math.sqrt(1-e))))

    lat = B[1]*180/math.pi
    lon = L[1]*180/math.pi
    azimuth = A[1]*180/math.pi
    B[0] = B[0]*180/math.pi
    L[0] = L[0]*180/math.pi
    A[0] = A[0]*180/math.pi
    return azimuth, lat, lon
