from keras.applications.vgg16 import VGG16

model = VGG16(weights='imagenet', include_top=False, pooling='avg')
