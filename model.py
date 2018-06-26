import numpy as np
from keras.applications.vgg16 import VGG16

model = VGG16(weights='imagenet', include_top=False, pooling='avg')

# see http://tsuwabuki.hatenablog.com/entry/2016/10/17/150033
x = np.zeros((224, 224, 3))
x = np.expand_dims(x, axis=0)
model.predict(x)

