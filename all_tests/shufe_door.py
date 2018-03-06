import  requests
import pytesseract
from PIL import Image

from PIL import ImageEnhance,ImageFilter
check_url='https://login.sufe.edu.cn/cas/codeimage?0'
response=requests.get(check_url)
img=response.content
with open("code{}.tiff",'wb')as f:
    f.write(img)
image=Image.open("code{}.tiff")
def binarizing(img,threshold):
    #input: gray image
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):

            if pixdata[x, y] < threshold:
                pixdata[x, y] = (0,0,0)
            else:
                pixdata[x, y] = (255,255,255)

    return img

filtering=image.filter(ImageFilter.SMOOTH)
img=binarizing(filtering,(200,200,200))
img.show()



optCode=pytesseract.image_to_string(img,)
print(optCode)

