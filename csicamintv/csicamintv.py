import os
import uuid
import cv2
import time
import sys
#import threading
import concurrent.futures
from jetcam.csi_camera import CSICamera
from jetcam.utils import bgr8_to_jpeg

cptflg = True 

def CameraCpt(invl):
    global cptflg
    camera = CSICamera(width=224, height=224)
    camera.running = True
    camera.unobserve_all()
    #image = camera.read()
    # print(image)
    cont = 0
    while cptflg:
        print("#CPT!" & cont)
        value = camera.value
        filename = '%d_%d_%s.jpg' % (0, 0, str(uuid.uuid1()))
        cv2.imwrite(filename, value)
        time.sleep(invl)
        cont += 1

def CameraCptCnt(invl, cntmax):
    camera = CSICamera(width=224, height=224)
    camera.running = True
    camera.unobserve_all()
    #image = camera.read()
    # print(image)
    for cont in range(cntmax):
        value = camera.value
        filename = '%d_%d_%s.jpg' % (0, 0, str(uuid.uuid1()))
        cv2.imwrite(filename, value)
        time.sleep(invl)

def CameraCptCtl(StartStop) :
    global cptflg
    if StartStop:
        cptflg = True
    else:
        cptflg = False

def CameraCptCtlUsrCmd() :
    global cptflg
    loopflg = True
    while loopflg:
        print("(g,s)>>")
        char = imput() 
        if char == 'g':
            # go
            cptflg = True 
            loopflg = True
        elif char == 's':
            # stop
            cptflg = False
            loopflg = True
        else:
            loopflg = False 


if  __name__ == "__main__":
    cptflg = True

    # executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

    # executor.submit(CameraCptCtlUsrCmd)
    # executor.submit(CameraCpt)
    print("start cpt")
    CameraCptCnt(1, 10)
    sys.exit()
""" 


from jetcam.csi_camera import CSICamera
# from jetcam.usb_camera import USBCamera

camera = CSICamera(width=224, height=224)
# camera = USBCamera(width=224, height=224)

camera.running = True

import cv2
import ipywidgets
import traitlets
from IPython.display import display
from jetcam.utils import bgr8_to_jpeg
from jupyter_clickable_image_widget import ClickableImageWidget


# initialize active dataset
dataset = datasets[DATASETS[0]]

# unobserve all callbacks from camera in case we are running this cell for second time
camera.unobserve_all()

# create image preview
camera_widget = ClickableImageWidget(width=camera.width, height=camera.height)
snapshot_widget = ipywidgets.Image(width=camera.width, height=camera.height)
traitlets.dlink((camera, 'value'), (camera_widget, 'value'), transform=bgr8_to_jpeg)

# create widgets
dataset_widget = ipywidgets.Dropdown(options=DATASETS, description='dataset')
category_widget = ipywidgets.Dropdown(options=dataset.categories, description='category')
count_widget = ipywidgets.IntText(description='count')

# manually update counts at initialization
count_widget.value = dataset.get_count(category_widget.value)

# sets the active dataset
def set_dataset(change):
    global dataset
    dataset = datasets[change['new']]
    count_widget.value = dataset.get_count(category_widget.value)
dataset_widget.observe(set_dataset, names='value')

# update counts when we select a new category
def update_counts(change):
    count_widget.value = dataset.get_count(change['new'])
category_widget.observe(update_counts, names='value')


def save_snapshot(_, content, msg):
    if content['event'] == 'click':
        data = content['eventData']
        x = data['offsetX']
        y = data['offsetY']
        
        # save to disk
        dataset.save_entry(category_widget.value, camera.value, x, y)
        # ココで保存しているはず。category_widget.valueはなんかわからんがパスを作ってるらしい。
        # cv2.imwrite()で画像を保存しているっぽい。
        

        # カメラバリューがカメラの値のハズ。
            def save_entry(self, category, image, x, y):
                category_dir = os.path.join(self.directory, category)
                if not os.path.exists(category_dir):f
                    subprocess.call(['mkdir', '-p', category_dir])
                    
                filename = '%d_%d_%s.jpg' % (x, y, str(uuid.uuid1()))
                
                image_path = os.path.join(category_dir, filename)
                cv2.imwrite(image_path, image)
                self.refresh()

        # display saved snapshot
        snapshot = camera.value.copy()
        snapshot = cv2.circle(snapshot, (x, y), 8, (0, 255, 0), 3)
        snapshot_widget.value = bgr8_to_jpeg(snapshot)
        count_widget.value = dataset.get_count(category_widget.value)
        
camera_widget.on_msg(save_snapshot)

data_collection_widget = ipywidgets.VBox([
    ipywidgets.HBox([camera_widget, snapshot_widget]),
    dataset_widget,
    category_widget,
    count_widget
])

display(data_collection_widget)
 """