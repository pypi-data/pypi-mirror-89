import os
import numpy as np
from PIL import Image

print('1', os.getcwd())

def func(x):
    #return -np.log(x*(-1)/255.1 + 1)
    return - 1/ ((1 * x/256)-1) - 1

def NumOCR(path, label=None, debug=False, show=False):

    # Calling for target photo
    ImageFile = Image.open(path).convert("L")
    if show:
        ImageFile.show()
    ContentArray = np.array(ImageFile.resize((28, 28)))
    ImageFile.close()

    # Calling for trained model
    print('2', os.getcwd())
    try:
        ThetaArray = np.load("theta.npy")
    except:
        os.chdir("./MNIST2")
        ThetaArray = np.load("theta.npy")

    # Comparison
    ThetaArray = np.fabs(ThetaArray - ContentArray)
    Theta = func(ThetaArray).sum(axis=1).sum(axis=1)
    
    #print(Theta)
    Prediction = np.argmin(Theta)

    if debug:
        print(Theta)

    if not label:
        print("Prediction :", Prediction)

    if label:
        return True if Prediction == label else False

if __name__ == "__main__":
    print('3', os.getcwd())
    NumOCR("tmpl6deljrh.PNG", label=None, debug=False, show=False)
