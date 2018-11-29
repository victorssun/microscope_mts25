### ids camera functions
# always run start_cam() first
# camPreview to do live previewing, 1s per frame
# close fig by ctrl+c
# should there be a delay?
# close cam before turn off

'''
start_cam() - in & out
take_pic2() - in & out
display_img() - in
save_img() - in & out
save_img2() - no work
camPreview() - in
'''

import ids, pylab, time, cv2, sys, datetime

def start_cam(ida, expo=0, pixelclock=24):
    # turn on cam, note default exposure time and pixelclock
    # what should color mode be?
    cam = ids.Camera(ida)
    cam.color_mode = ids.ids_core.COLOR_RGB8 # preview blue, saved yellow
    #cam.color_mode = ids.ids_core.COLOR_BGR8 # preview yellow, saved blue
    cam.pixelclock =  pixelclock # reduce pxclock to increase expo
    if expo > 0:
        cam.exposure = expo
    elif expo == 0:
        cam.exposure = 50  
        #cam.auto_exposure = True
    return cam

def take_pic2(cam, autosave=False, direct=''):
    # takes a picture after x delay, throwing out first five frames due to buffer
    expo = cam.exposure
    time.sleep(expo/1000 * 3) # delay to ensure correct exposure
    cam.continuous_capture = True
    for i in range(5): # have to run through buffered frames, how do you know five is enough
        img, meta = cam.next()
    img, meta = cam.next()
    if autosave == True:
        filename = '%s%s.jpg' %(direct, datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M%S'))
        cam.next_save(filename)
    cam.continuous_capture = False
    return img, expo

def display_img(fig, img):
    # requires fig = pylab.figure()/pylab.ion() for continuous viewing
    pylab.clf()
    ax1 = fig.add_subplot(111)
    ax1.imshow(img)
    ax1.figure.canvas.draw()

def save_img(filename, img):
    # should save bgr or rgb?
    img2 = img
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite(filename, img2)

def save_img2(filename, cam):
    # doesn't work half the time
    print filename
    print cam
    #cam.continuous_capture = True
    #cam.next_save(str(filename))
    cam.next_save('test.jpg')
    cam.continuous_capture = False

def camPreview(direct='/mnt/cluster-victor/lin_motors/pics/raster/'):
    # for pylab previewing/ueye alternative: option to save last frame
    # note the default save directory
    check = raw_input(' preview starting... close ueye. continue? (y/n) ')
    if check == 'y':
        pylab.ion()
        fig = pylab.figure()
        # run cam
        cam = start_cam(2)
        conts = 0
        try:
            while True:
                #a = time.time()
                img, expo = take_pic2(cam, False, direct)
                #img, expo = take_pic(2) # find cam id
                display_img(fig, img)
                fn = '/mnt/cluster-victor/lin_motors/pics/d%s_c%003d.png' %(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'), conts)
                conts = conts + 1
                save_img(fn, img)
                #b = time.time()
                #print b-a
        except KeyboardInterrupt:
                display_img(fig, img) # display last frame
        #save_img2('test2.jpg', cam)
        #cam.next_save('test.jpg')
        cam.close()
        # saving file
        filename = '%stest_exp_%.2f.png' %(direct, expo)
        if raw_input(' save img: %s? (y/n): ' %filename) == 'y':
            save_img(filename, img)
        else: 
            print(' no save')


### MAIN CODE
#direct = '/mnt/cluster-victor/lin_motors/pics/raster/'

#camPreview()

if __name__ == '__main__':
    if raw_input(' turn on camPreview? (y/n): ') == 'y':
        camPreview()
    else:
        print('camcontrol.py ran directly')
else:
    print('camcontrol.py imported. run start_cam(id) before using cam.')




