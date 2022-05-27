import io
import os
import joblib
import collections
import numpy as np
import pandas as pd
from glob import glob
from tqdm import tqdm
from colorthief import ColorThief

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
  paths = []
  color = None
#  emotions = ['LOVELY','CUTE','PEACEFUL','ENGAGED','VIVID','INSPIRED','JOYFUL','HOPEFUL','REFRESHED','COMFORTABLE','HIP','ENERGETIC']
#  emotions = get_emotions()
  matched_emotion = {}
  
  ept = pd.read_csv('./matched_emotions.csv')
  avail = list(ept['업장명'])
  
  folders = glob(r'./img/*')
  for folder in folders:
    paths.append(glob(folder + '/*'))

  for path in paths:
    emotion = []
    name = path[0].split(os.path.sep)[1]
    if name in avail: continue

    for file in tqdm(path, desc=name):
      with open(file, 'rb') as f:
        data = f.read()
        color = list(get_dominant_color(data))

      x = np.array(color)
      x = x.reshape(-1, 1)
      x = np.transpose(x)

      clf_from_joblib = joblib.load('placeEmotion.pkl') 
      tmp = clf_from_joblib.predict(x)
      try:  emotion.append(tmp[0])
      except: emotion.append('x')
    
    counts = collections.Counter(emotion)
    t = list(counts.most_common(2))
    if 'x' in t[0]: matched_emotion[name] = t[1][0]
    else: matched_emotion[name] = t[0][0]

    ept = pd.read_csv('./matched_emotions.csv')
    seri = pd.Series((name, matched_emotion[name]), index=['업장명', '분위기'])
    ept = ept.append(seri, ignore_index=True)
    print(ept.head())
    ept.to_csv('./matched_emotions.csv', index=False)

if __name__ == "__main__":
    main()