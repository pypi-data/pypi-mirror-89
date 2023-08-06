import os
import numpy as np
from PIL import Image
from Functions import *

def NumOCR(path, label=None, debug=False, show=False):

    # Calling for target photo
    ImageFile = Image.open(path).convert("L")
    if show:
        ImageFile.show()
    ContentArray = np.array(ImageFile.resize((28, 28)))
    ImageFile.close()

    # Calling for trained model
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
