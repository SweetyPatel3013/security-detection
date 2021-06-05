import cv2
import winsound
# we are using only one camera so thats why we entered 0
cam=cv2.VideoCapture(0)

while cam.isOpened():
    
    # frame of the camera is given to frame
    #to read input from camera
    #b is a boolean value will tell whether caputuring object is working or not
    #to read input from camera
    b,frame1=cam.read()
    b,frame2=cam.read()
    
    #capturing 2 instance of frame and comparing both in order to capturing movement in frame
    #diff. will show movement in black and color
    #if diff. between current and previous position(frames) is same nothing will be shown
    diff=cv2.absdiff(frame1,frame2)
    #grey will show moment in grey color
    grey=cv2.cvtColor(diff,cv2.COLOR_RGB2GRAY)
    blur=cv2.GaussianBlur(grey,(5,5),0)
    
    #thresh will help us to rmove noice , more clear movement will be shown
    # it gives 2 values one will be store in thresh other in '_' as we dont other value
    _,thresh=cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    
    #dilating 3 times'iterations=3' kernel=none
    dilated=cv2.dilate(thresh,None,iterations=2)
    
    #contoours are the boundries of item that
    #we have didected moving what things are moving
    #find every moving object use findcontours ,
    #'RETR_TREE' is a mode,'cv2.CHAIN_APPROX_SIMPLE' is method
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    # to actuallydraw contours on frame1 use draw contours, -1  for everything, ,
    #2 is thickness,0,255,0 is green color
    #it will detect all small things that are moving
    '''cv2.drawContours(frame1,contours,-1,(0,255,0),2)'''
    # to detect only large objects
    # waitKey help toterminate program without any error
    for c in contours:
        if cv2.contourArea(c)<3000:
            continue
        x,y,w,h=cv2.boundingRect(c)
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),3)
    if cv2.waitKey(5)== ord('q'):
        # to release camera source 
        cam.release()
        cv2.destroyAllWindows()
        break
    # it will show captured video on screen
    cv2.imshow('Movement Detection Camera',frame1)

    ## David's comment

