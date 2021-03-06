
import matplotlib.pyplot as plt
import numpy as np
from keras.datasets import mnist
from keras.datasets import fashion_mnist
from keras.layers import Input, Dense
from keras.models import Model

#%matplotlib inline

(X_train, _), (X_test, _) = mnist.load_data()
(X_train2, _), (X_test2, _) = fashion_mnist.load_data()

X_train = X_train.astype('float32')/255
X_test = X_test.astype('float32')/255
X_train = X_train.reshape(len(X_train), np.prod(X_train.shape[1:]))
X_test = X_test.reshape(len(X_test), np.prod(X_test.shape[1:]))
print(X_train.shape)
print(X_test.shape)

X_train2 = X_train2.astype('float32')/255
X_test2 = X_test2.astype('float32')/255
X_train2 = X_train2.reshape(len(X_train2), np.prod(X_train2.shape[1:]))
X_test2 = X_test2.reshape(len(X_test2), np.prod(X_test2.shape[1:]))
print(X_train2.shape)
print(X_test2.shape)

input_img= Input(shape=(784,))

encoded = Dense(units=128, activation='relu')(input_img)
encoded = Dense(units=64, activation='relu')(encoded)
encoded = Dense(units=32, activation='relu')(encoded)
decoded = Dense(units=64, activation='relu')(encoded)
decoded = Dense(units=128, activation='relu')(decoded)
decoded = Dense(units=784, activation='sigmoid')(decoded)

autoencoder=Model(input_img, decoded)

encoder = Model(input_img, encoded)

autoencoder.summary()

encoder.summary()

autoencoder.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

autoencoder.fit(X_train2, X_train2,
                epochs=50,
                batch_size=256,
                shuffle=True,
                validation_data=(X_test2, X_test2))

encoded_imgs = encoder.predict(X_test)
predicted = autoencoder.predict(X_test2)

plt.figure(figsize=(40, 4))
for i in range(10):
    # display original images
    ax = plt.subplot(3, 20, i + 1)
    plt.imshow(X_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # display encoded images
    ax = plt.subplot(3, 20, i + 1 + 20)
    plt.imshow(encoded_imgs[i].reshape(8, 4))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # display reconstructed images
    ax = plt.subplot(3, 20, 2 * 20 + i + 1)
    plt.imshow(predicted[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

plt.show()

#loading only images and not their labels

#number data:
(X_train, _), (X_test, _) = mnist.load_data()

X_train = X_train.astype('float32')/255
X_test = X_test.astype('float32')/255

X_train = X_train.reshape(len(X_train), np.prod(X_train.shape[1:]))
X_test = X_test.reshape(len(X_test), np.prod(X_test.shape[1:]))

X_train_noisy = X_train + np.random.normal(loc=0.0, scale=0.5, size=X_train.shape)
X_train_noisy = np.clip(X_train_noisy, 0., 1.)
X_test_noisy = X_test + np.random.normal(loc=0.0, scale=0.5, size=X_test.shape)
X_test_noisy = np.clip(X_test_noisy, 0., 1.)
print(X_train_noisy.shape)
print(X_test_noisy.shape)

#fashion data:
(X_train2, _), (X_test2, _) = fashion_mnist.load_data()

X_train2 = X_train2.astype('float32')/255
X_test2 = X_test2.astype('float32')/255

X_train2 = X_train2.reshape(len(X_train), np.prod(X_train2.shape[1:]))
X_test2 = X_test2.reshape(len(X_test), np.prod(X_test2.shape[1:]))

X_train_noisy2 = X_train2 + np.random.normal(loc=0.0, scale=0.5, size=X_train2.shape)
X_train_noisy2 = np.clip(X_train_noisy2, 0., 1.)
X_test_noisy2 = X_test2 + np.random.normal(loc=0.0, scale=0.5, size=X_test2.shape)
X_test_noisy2 = np.clip(X_test_noisy2, 0., 1.)
print(X_train_noisy2.shape)
print(X_test_noisy2.shape)

# Input image
input_img = Input(shape=(784,))
# encoded and decoded layer for the autoencoder
encoded = Dense(units=128, activation='relu')(input_img)
encoded = Dense(units=64, activation='relu')(encoded)
encoded = Dense(units=32, activation='relu')(encoded)
decoded = Dense(units=64, activation='relu')(encoded)
decoded = Dense(units=128, activation='relu')(decoded)
decoded = Dense(units=784, activation='sigmoid')(decoded)
# Building autoencoder
autoencoder = Model(input_img, decoded)
# extracting encoder
encoder = Model(input_img, encoded)
# compiling the autoencoder
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy', metrics=['accuracy'])
# Fitting the noise trained data to the autoencoder
autoencoder.fit(X_train_noisy2, X_train_noisy2,
                epochs=100,
                batch_size=256,
                shuffle=True,
                validation_data=(X_test_noisy, X_test_noisy))
# reconstructing the image from autoencoder and encoder
encoded_imgs = encoder.predict(X_test_noisy)
predicted = autoencoder.predict(X_test_noisy2)
# plotting the noised image, encoded image and the reconstructed image
plt.figure(figsize=(40, 4))
for i in range(10):
    # display original images

    ax = plt.subplot(4, 20, i + 1)
    plt.imshow(X_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # display noised images
    ax = plt.subplot(4, 20, i + 1 + 20)
    plt.imshow(X_test_noisy[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # display encoded images
    ax = plt.subplot(4, 20, 2 * 20 + i + 1)
    plt.imshow(encoded_imgs[i].reshape(8, 4))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # display reconstruction images
    ax = plt.subplot(4, 20, 3 * 20 + i + 1)
    plt.imshow(predicted[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

plt.show()

