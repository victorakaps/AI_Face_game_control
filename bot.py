import cv2
import keyboard

def crossHair(img, faceCascade):
    grayScaleImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    features = faceCascade.detectMultiScale(grayScaleImage, 1.1, 8)
    crossHairCords = []
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x,y), (x+w, y+h),  (0,255,0), 2)
        cv2.circle(img, ((2*x+w)//2,(2*y+h)//2), 10, (0,0,255), 2) 
        crossHairCords = ((2*x+w)//2,(2*y+h)//2)
    return img, crossHairCords

def boundary(img, cords):
    size = 40
    x1 = cords[0] - size
    y1 = cords[1] - size
    x2 = cords[0] + size
    y2 = cords[1] + size
    cv2.circle(img, cords,  size, (255,255,0), 2) 
    return [(x1,y1), (x2,y2)]

def keyboard_events(crossHairCords, cords, key):
    try:
        [(x1,y1), (x2,y2)] = cords
        xc, yc = crossHairCords
    except Exception as e: 
        print(e)
        return
    if xc < x1:
        key = "left"
    elif(xc > x2):
        key = "right"
    elif(yc<y1):
        key = "up"
    elif(yc > y2):
        key = "down"
    if key:
        keyboard.press_and_release(key)
    return img,key
def resetFlag(crossHairCords, cords,key):
    try:
        [(x1,y1), (x2,y2)] = cords
        xc, yc = crossHairCords
    except: 
        return True,key
    if x1<xc<x2 and y1<yc<y2:
        return True,None
    return False,key
    
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

videoFeed = cv2.VideoCapture(0)

width  = videoFeed.get(3) 
height = videoFeed.get(4) 
flag = False
key = ""

while True:
    _, img = videoFeed.read()
    img = cv2.flip( img, 1 )

    img, crossHairCords = crossHair(img, faceCascade)
    cv2.putText(img, key, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1, cv2.LINE_AA)

    cords = boundary(img, (int(width/2), int(height//2)) )
    if flag and len(crossHairCords):
        img,key = keyboard_events(crossHairCords,cords, key)
    flag,key = resetFlag(crossHairCords,cords,key)

    cv2.imshow("victor", img)
    if cv2.waitKey(1) & 0xFF == ord('z'):
        break

videoFeed.release()
cv2.destroyAllWindows()
