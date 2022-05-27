from colorthief import ColorThief
import io
import joblib
import numpy as np

def get_dominant_color(img):
  """Given an image in url format, eturn the dominant color."""
  try:
    f = io.BytesIO(img)
    color_thief = ColorThief(f)
    color = color_thief.get_color(quality=1)
    return color
  except:
    return np.NaN 

def main():
    color = None
    path = './images (1).jpg'
    with open(path, 'rb') as f:
        data = f.read()
        color = list(get_dominant_color(data))

    x = np.array(color)
    x = x.reshape(-1, 1)
    x = np.transpose(x)

    clf_from_joblib = joblib.load('placeEmotion.pkl') 
    print(clf_from_joblib.predict(x))

if __name__ == "__main__":
    main()