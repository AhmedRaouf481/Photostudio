
from copy import deepcopy
import numpy as np


class Histograms:

    def __init__(self, img):
        self.img = img

    def getImg(self):
        return self.img

    def operateOn(self, img):
        self.img = img

    def equalize(self):
        img = self.getImg()
        histogram = self.getHistoGram(img)
        cumulativeSum = self.getCumSum(histogram)

        cumulativeSum /= cumulativeSum[-1]
        cumulativeSum *= 255
        cumulativeSum = cumulativeSum.astype('uint8')

        flattenedImg = self.flatten(img)
        newImg = cumulativeSum[flattenedImg]
        newImg = np.reshape(newImg, img.shape)

        return newImg

    def normalise(self):
        img = self.getImg()
        newImg = deepcopy(img)
        rows = img.shape[0]
        columns = img.shape[1]
        for i in range(rows):
            for j in range(columns):
                newImg[i][j] = newImg[i][j]/(255) * 400

        return newImg

    def applyGlobalThreshold(self, threshold):
        newImg = self.getImg()

        newImg[newImg > threshold] = 255
        newImg[newImg != 255] = 0

        return newImg

    def applyLocalThreshold(self, blockSize=10, C=5):
        inputImg = self.getImg()
        # if blockSize % 2 == 0:
        #     blockSize += 1

        output = np.zeros_like(inputImg)

        for x in range(inputImg.shape[0]):
            for y in range(inputImg.shape[1]):
                # Get the neighborhood around the pixel
                neighborhood = []
                for i in range(-blockSize // 2, blockSize // 2 + 1):
                    for j in range(-blockSize // 2, blockSize // 2 + 1):
                        # Check if the pixel is within the image boundaries
                        px = x + i
                        py = y + j
                        if px >= 0 and px < inputImg.shape[0] and py >= 0 and py < inputImg.shape[1]:
                            neighborhood.append(inputImg[px, py])

                # Compute the local threshold using the mean and constant C
                threshold = int(round(np.mean(neighborhood) - C))

                # Apply the threshold to the pixel
                if inputImg[x][y] >= threshold:
                    output[x][y] = 255
                else:
                    output[x][y] = 0

        return output

    # splits the img to 3 frames r,g,b
    # the img must be colored
    def split(self):
        img = self.getImg()

        # determining width and height of original image
        w, h = img.shape[:2]

        # new Image dimension with 4 attribute in each pixel
        r = np.zeros_like(img)
        g = np.zeros_like(img)
        b = np.zeros_like(img)
        print(w)
        print(h)

        for i in range(w):
            for j in range(h):
                # ratio of RGB will be between 0 and 1
                b[i][j] = (img[i][j][0])
                g[i][j] = (img[i][j][1])
                r[i][j] = (img[i][j][2])
        return r, g, b

    # takes 1darray and return its cumulative sum
    def getCumSum(self,arr):
        a = np.array(arr)
        b = []

        isFirstElement = True
        for i in a:
            if isFirstElement:
                b.append(a[0])
                isFirstElement = False
                continue
            b.append(b[-1] + i)

        b = np.array(b)
        return b

    # takes 2darray and returns 1d histogram array whose index represents
    # the intensity and the value at each index represents the frequency of that intennsity
    def getHistoGram(self, arr2d, bins=256):
        flattenedImage = self.flatten(arr2d)

        # array with size of bins, set to zeros
        histogram = np.zeros(bins)

        # loop through pixels and sum up counts of pixels
        for pixel in flattenedImage:
            histogram[pixel] += 1

        # return our final result
        return histogram

    # takes a 2darray and return it as just 1d.
    def flatten(self,arr2d):
        img = np.asarray(arr2d)
        img = img.flatten()
        return img


class ColoredOperator:

    def __init__(self, img):
        self.img = img
        r, g, b = self.split()
        self.red = r
        self.green = g
        self.blue = b

    def getImg(self):
        return self.img

    def getRedFrame(self):
        return self.red

    def getGreenFrame(self):
        return self.green

    def getBlueFrame(self):
        return self.blue

    # splits the img to 3 frames r,g,b
    # the img must be colored

    def split(self):
        img = self.getImg()

        # determining width and height of original image
        w, h = img.shape[:2]

        # new Image dimension with 4 attribute in each pixel
        r = np.zeros_like(img)
        g = np.zeros_like(img)
        b = np.zeros_like(img)
        print(w)
        print(h)

        for i in range(w):
            for j in range(h):
                # ratio of RGB will be between 0 and 1
                b[i][j] = (img[i][j][0])
                g[i][j] = (img[i][j][1])
                r[i][j] = (img[i][j][2])
        return r, g, b
