from numpy import *
def loadDataSet(fileName):
    # drop the colum(last colum) of label.
    numFeat = len(open(fileName).readline().split('\t')) - 1
    dataMat = []
    labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat, labelMat
# w = (X.T * X) ^ -1 * X.T * y
def standRegres(xArr, yArr):
    xMat = mat(xArr)
    yMat = mat(yArr).T
    xTx = xMat.T*xMat
    if linalg.det(xTx) == 0.0:
        print("This matrix is singular, connot do inverse")
        return
    ws = xTx.I * (xMat.T*yMat)
    return ws

# w = (X.T * W * X) ^ -1 * X.T * W * y
# weighted data points.
# Gaussian kernel:
# w(i, i) = exp(|x(i) - x| / (-2 * k^2))
# more far from testpoint lower weight the data point has.
def lwlr(testPoint, xArr, yArr, k = 1.0):
    xMat = mat(xArr)
    yMat = mat(yArr).T
    m = shape(xMat)[0]
    weights = mat(eye((m)))
    for j in range(m):
        diffMat = testPoint - xMat[j,:] # distance from testpoint to point in trainning data.
        weights[j, j] = exp(diffMat*diffMat.T/(-2.0*k**2))
    xTx = xMat.T * (weights * xMat)
    if linalg.det(xTx) == 0.0:
        print("This matrix is singular, cannot do inverse")
        return
    ws = xTx.I * (xMat.T * (weights * yMat))
    return testPoint * ws

def lwlrTest(testArr, xArr, yArr, k=1.0):
    m = shape(testArr)[0]
    yHat = zeros(m)
    for i in range(m):
        yHat[i] = lwlr(testArr[i], xArr, yArr, k)
    return yHat

def rssError(yArr, yHatArr):
    return ((yArr - yHatArr) ** 2).sum()

# w = (X.T * X + lambda * I) ^ -1 * X.T * y
# Ridge regression adds an additional matrix (lambda * I) to the matrix (X.T * X) so that it’s non-singular,
# and we can take the inverse of the whole thing: (X.T * X + lambda * I)
# Ridge regression was originally developed to deal with the problem of having more
# features than data points. But it can also be used to add bias into our estimations, giving us a better estimate.
def ridgeRegres(xMat, yMat, lam = 0.2):
    xTx = xMat.T * xMat
    denom = xTx + eye(shape(xMat)[1]) * lam
    if linalg.det(denom) == 0.0:
        print("This matrix is singular, cannot do inverse")
        return
    ws = denom.I * (xMat.T * yMat)
    return ws

def ridgeTest(xArr, yArr):
    xMat = mat(xArr)
    yMat = mat(yArr).T

    yMean = mean(yMat, 0)
    yMat = yMat - yMean

    xMeans = mean(xMat, 0)
    xVar = var(xMat, 0)
    xMat = (xMat - xMeans) / xVar

    numTestPts = 30
    wMat = zeros((numTestPts, shape(xMat)[1]))
    for i in range(numTestPts):
        ws = ridgeRegres(xMat, yMat, exp(i-10))
        wMat[i,:] = ws.T
    return wMat

xArr, yArr = loadDataSet('ex0.txt')
print(xArr)
print(yArr)
ws = standRegres(xArr, yArr)
print(ws)

xMat = mat(xArr)
yMat = mat(yArr)
yHat = xMat * ws

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(xMat[:, 1].flatten().A[0], yMat.T[:, 0].flatten().A[0])
xCopy = xMat.copy()
xCopy.sort(0)
yHat = xCopy*ws
ax.plot(xCopy[:, 1], yHat)
plt.show()

xArr,yArr=loadDataSet('ex0.txt')
print(yArr[0])
print(lwlr(xArr[0],xArr,yArr,1.0))
print(lwlr(xArr[0],xArr,yArr,0.001))
yHat = lwlrTest(xArr, xArr, yArr,0.003)

xMat = mat(xArr)
srtInd = xMat[:, 1].argsort(0)
xSort = xMat[srtInd][:,0,:]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(xSort[:, 1], yHat[srtInd])
ax.scatter(xMat[:, 1].flatten().A[0], mat(yArr).T.flatten().A[0], s = 2, c = 'red')
plt.show()

abX, abY = loadDataSet('abalone.txt')
ridgeWeights = ridgeTest(abX, abY)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(ridgeWeights)
plt.show()