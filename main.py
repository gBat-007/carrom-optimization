from math import *
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
from tqdm import tqdm

def s(x_c, y_c, x_s, theta):
    A = ((x_s - x_c) * cos(theta)) - (y_c * sin(theta))
    B = (x_s - x_c)**2 + y_c**2 - 12.25
    inside_sqrt = A**2 - B
    if inside_sqrt < 0:
        return None
    return (y_c * sin(theta)) - ((x_s - x_c) * cos(theta)) - sqrt(inside_sqrt)

def v_c(x_c,y_c,x_s,v_s,theta):#make sure to input theta in radians(deg)!
  ss = s(x_c,y_c,x_s,theta)
  sine = sin(theta)
  cosi = cos(theta)
  return (19/24)*(sqrt((v_s**2 - 78.4*ss)/((x_c - x_s - ss*cosi)**2 + (y_c - ss*sine)**2)))*(x_c*cosi - x_s * cosi - ss*(cosi**2) + y_c * sine - ss * (sine**2))


def n_x(x_c,y_c,x_s,theta): #make sure to input theta in radians(deg)!
  ss = s(x_c,y_c,x_s,theta)
  sine = sin(theta)
  cosi = cos(theta)
  return (x_c - x_s - ss*cos(theta))/(sqrt((x_c - x_s - ss * cos(theta))**2 + (y_c - ss*sin(theta))**2))

def n_y(x_c,y_c,x_s,theta): #make sure to input theta in radians(deg)!
  ss = s(x_c,y_c,x_s,theta)
  sine = sin(theta)
  cosi = cos(theta)
  return (y_c - ss*sin(theta))/(sqrt((x_c - x_s - ss * cos(theta))**2 + (y_c - ss*sin(theta))**2))


def pot(x_c,y_c,x_s,v_s,theta,x_p): #in radians!
  nx = n_x(x_c,y_c,x_s,theta)
  ny = n_y(x_c,y_c,x_s,theta)
  vc = v_c(x_c,y_c,x_s,v_s,theta)
  reaches = (0 <= (x_p - x_c)*nx + (60.648 - y_c)*ny <= ((vc**2)/78.4))
  goesIn = (sqrt((x_p - x_c - ((x_p - x_c)*nx + (60.648 - y_c)*ny)*nx)**2 + (60.648 - y_c - ((x_p - x_c)*nx + (60.648 - y_c)*ny)*ny)**2) <= 2.4)
  return goesIn * reaches


def p(x_c,y_c,x_s,v_s,theta):
  return 1 if (pot(x_c,y_c,x_s,v_s,theta,-34.648) + pot(x_c,y_c,x_s,v_s,theta,34.648) >= 1) else 0


def coll(x_c,y_c,x_s,v_s,theta):
  if (abs((x_s - x_c)*sin(theta) + (y_c * cos(theta))) <= 3.5) and (v_s**2 >= 78.4*((x_c - x_s)*cos(theta) + y_c * sin(theta) - 3.5)):
    return True
  else:
    return False

def scoll(x_c, y_c, x_s, v_s, theta):
    ss = s(x_c, y_c, x_s, theta)
    if ss is None:
        return False
    return v_s**2 - 78.4 * ss > 0

def score(x_c, y_c, v_s):
    sc = 0
    for x_s in np.arange(-22.5, 22.6, 0.25):
        for theta in np.arange(0.25, 180, 0.25):
            theta_rad = radians(theta)
            if not coll(x_c, y_c, x_s,v_s, theta_rad):
                continue
            if not scoll(x_c, y_c, x_s, v_s, theta_rad):
                continue
            sc += p(x_c, y_c, x_s, v_s, theta_rad)
    return sc

def score_wrapper(args):
    x_c, y_c, v_s = args
    return score(x_c, y_c, v_s)
def allScores(v_s):
    coords = []
    y_c = 3
    for i in range(99):     # 99 rows
        y_c += 0.5
        x_c = -27
        for j in range(107):  # 107 cols
            x_c += 0.5
            coords.append((x_c, y_c, v_s))

    print(f"Computing {len(coords)} scores...")

    with mp.Pool() as pool:
        results = list(tqdm(pool.imap(score_wrapper, coords), total=len(coords)))


    scores = np.array(results).reshape((99, 107))
    
    filename = f"scores_vs{v_s}.npy"
    np.save(filename, scores)
    print(f"Scores saved to {filename}")

    extent = [-26.5, 26.5, 3.5, 52.5]
    plt.imshow(scores, cmap='viridis', interpolation='nearest', origin='lower', extent=extent)
    plt.colorbar(label="Score")
    plt.xlabel("x_c (cm)")
    plt.ylabel("y_c (cm)")
    plt.title(f"Carromboard Score Heatmap for v_s = {v_s}")
    plt.show()

    
if __name__ == "__main__":
    allScores(158)