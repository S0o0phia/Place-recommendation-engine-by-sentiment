from colorthief import ColorThief
from urllib.request import urlopen
import io
from glob import glob
from tqdm import tqdm
import pandas as pd
import numpy as np

def get_dominant_color(img):
  """Given an image in url format, eturn the dominant color."""
  with open(img, 'rb') as f:
    try:
      x = io.BytesIO(f.read())
      color_thief = ColorThief(x)
      color = color_thief.get_color(quality=1)
      return color
    except Exception as e:
      print(e)
      return np.NaN 

def main():
  origin = pd.read_csv("emotions.csv")
  emotions = origin['emotion'].tolist()
  tmp = [glob('./downloads/' + e + ' place/*') for e in emotions]
  imgs = [path for paths in tmp for path in paths]

  df = pd.DataFrame(imgs)
  colors = [get_dominant_color(img) for img in tqdm(imgs)]
  df['color'] = colors
  df.to_csv("emotions_images_colors.csv")
  
main()
