import cv2
import numpy as np
def func(img):
    stand = 105
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            l = 0
            m = 0
            s = 0
            k = abs(img[i,j].mean() - s)
            if img[i,j,0] > img[i,j,1] and img[i,j,0] > img[i,j,2]:
                l = 0
                if img[i,j,1] >= img[i,j,2]:
                    m = 1
                    s = 2
                else:
                    m = 2
                    s = 1
            if img[i,j,1] > img[i,j,0] and img[i,j,1] > img[i,j,2]:
                l = 1
                if img[i,j,0] >= img[i,j,2]:
                    m = 0
                    s = 2
                else:
                    m = 2
                    s = 0
            if img[i,j,2] > img[i,j,1] and img[i,j,2] > img[i,j,0]:
                l = 2
                if img[i,j,1] >= img[i,j,0]:
                    m = 1
                    s = 0
                else:
                    m = 0
                    s = 1

            if img[i,j].mean() > stand:
                img[i,j,l] = int(img[i,j,l] - k * (0.2))
                img[i,j,m] = int(img[i,j,m] - k * (0.3))
                img[i,j,s] = int(img[i,j,s] - k * (0.5))

            if img[i,j].mean() < stand:
                img[i,j,l] = int(img[i,j,l] + k * (0.5))
                img[i,j,m] = int(img[i,j,m] + k * (0.3))
                img[i,j,s] = int(img[i,j,s] + k * (0.2))
            img[i,j] = np.clip(img[i,j], 0, 255)
    return img


def modify(img, lightness=50, saturation=300):

    origin_img = img


    fImg = img.astype(np.float32)
    fImg = fImg / 255.0


    hlsImg = cv2.cvtColor(fImg, cv2.COLOR_BGR2HLS)
    hlsCopy = np.copy(hlsImg)


    hlsCopy[:, :, 1] = (1 + lightness / 100.0) * hlsCopy[:, :, 1]
    hlsCopy[:, :, 1][hlsCopy[:, :, 1] > 1] = 1


    hlsCopy[:, :, 2] = (1 + saturation / 100.0) * hlsCopy[:, :, 2]
    hlsCopy[:, :, 2][hlsCopy[:, :, 2] > 1] = 1


    result_img = cv2.cvtColor(hlsCopy, cv2.COLOR_HLS2BGR)
    result_img = ((result_img * 255).astype(np.uint8))

    return result_img


# #####################



def pixel_l(R,G,B,L):
    a = [B,G,R]
    x = [0.11,0.3,0.59]
    b=sorted(a)
    for i in range(3):
        for j in range(3):
            if (b[i] == a[j]):
                a[j] = a[j]*(L*x[i])

    return a

def cal_l(img,i,j):
    a=[img[i,j,0],img[i,j,1],img[i,j,2]]
    c = 0
    x = [0.11,0.30,0.59]
    b=sorted(a)
    for k in range(img.shape[2]):
        for l in range(img.shape[2]):
            if(b[k] == a[l]):
                c = c + a[l] * x[k]


    return c


def exCorrectTest(img):
    stand = cv2.imread("bench.jpg")
    s = stand.mean()
    img2 = img
    h = img2.mean()
    sammy = 0
    sammycount = 0
    tim = 0
    timcount = 0
    img2=np.uint16(img2)

    for i in range(img2.shape[0]):
        for j in range(img2.shape[1]):
            jim = img2[i,j].mean()
            if(jim<h):
                
                sammy = sammy+jim
                sammycount = sammycount+1
            if(jim>h):
                tim = tim+jim
                timcount = timcount+1


    sammy = sammy/sammycount
    tim = tim/timcount

    # print((1-(0.01*(jim/tim))))
    # print((1-(0.0001*(tim/h))))



    for i in range(img2.shape[0]):
        for j in range(img2.shape[1]):
            jim = img2[i,j].mean()
            if(h < s):
                if(jim<sammy):
                    img2[i,j,0] = (1+(0.5*(img2[i,j,0]/h))) * img2[i,j,0]
                    img2[i,j,1] = (1+(0.5*(img2[i,j,1]/h))) * img2[i,j,1]
                    img2[i,j,2] = (1+(0.5*(img2[i,j,2]/h))) * img2[i,j,2]
            if(h > s):
                if(jim>h):
                    img2[i,j,0] = (1-(0.5*((255-img2[i,j,0])/255))) * img2[i,j,0]
                    img2[i,j,1] = (1-(0.5*((255-img2[i,j,1])/255))) * img2[i,j,1]
                    img2[i,j,2] = (1-(0.5*((255-img2[i,j,2])/255))) * img2[i,j,2]
            img2[i,j] = np.clip(img2[i,j], 0, 255)
            
    # print("after1 : ",img2[100,8])

    h = img2.mean()
    for i in range(img2.shape[0]):
        for j in range(img2.shape[1]):
            img2[i,j,0] = ((s/h)) * img2[i,j,0]
            img2[i,j,1] = ((s/h)) * img2[i,j,1]
            img2[i,j,2] = ((s/h)) * img2[i,j,2]
            img2[i,j] = np.clip(img2[i,j], 0, 255)

    img2 = np.clip(img2, 0, 255)
    img2 = np.uint8(img2)
    
    # avg_light = img2.mean()
    # print("avg light = ",avg_light)
    # print("s = ",s)
    # cv2.imshow('img2', img2)
    # cv2.waitKey(0)

    return img2