# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:40:33 2024

@author: wq271
"""

from matplotlib import pyplot as plt 
from matplotlib.patches import Circle
import numpy as np

features_ex1 = [[140, 60],  [8, 89], [179, 12], [270, 4], [235,10], [20,86], [90,0]]

features_ex2 = [[349,18], [245,40], [13,76], [ 180,72], [310,89], [77,12], [360,78],[90,90], [310,85]]

features_ex3 = [[49,18], [245,40], [180,72], [77,12], [360,78], [90,90]]


path = 'C:/Users/wq271/GMP_SoSe24/GMP_Exercises/ex3/'


def aux(dip_angle):
    if ((dip_angle>=0) & (dip_angle<=90)) or (dip_angle == 360):
        if dip_angle == 360:
            return np.radians(90)
        else:
            return np.radians(90 - dip_angle)
    elif ((dip_angle>90) & (dip_angle<=180)):
        return np.radians(180 - dip_angle + 270)
    elif ((dip_angle>180) & (dip_angle<=270)):
        return np.radians(270 - dip_angle + 180)
    elif ((dip_angle>270) & (dip_angle<360)):
        return np.radians(360 - dip_angle + 90)




def plot_strike_dip(features, mode, path, name, save=False):
    fig, axs = plt.subplots(3, 3, figsize=(4, 4))
    axs = axs.ravel()
    for i, feature in enumerate(features):
        ax = axs[i]
        
        ax.axhline(0, color='gray', linewidth=0.5, zorder =1)
        ax.axvline(0, color='gray', linewidth=0.5, zorder =1)
        
        if mode=='plane':
            # dip vector
            xlim_strike = np.cos(aux(feature[0]))
            ylim_strike = np.sin(aux(feature[0]))
            vector = np.array([xlim_strike, ylim_strike])
            
            # strike vector
            ort_vector = np.array([-vector[1], vector[0]])
            
            # plot strike vector
            if feature[1] == 90:
                ax.plot([0, -vector[0]*0.5], [0, -vector[1]*0.5], color='black', zorder =2)
                ax.plot([0, vector[0]*0.5], [0, vector[1]*0.5], color='black', zorder =2)
                ax.plot([0, -ort_vector[0]], [0, -ort_vector[1]], color='black', zorder =2)
                ax.plot([0, ort_vector[0]], [0, ort_vector[1]], color='black', zorder =2)
            elif (feature[1] == 0):
                ax.plot([0, 0], [0, 1], [0, 0], [0, -1],  color='black', zorder =2)
                ax.plot([0, -1], [0, 0],  color='black', zorder =2)
            else:
                ax.plot([0, ort_vector[0]], [0, ort_vector[1]], color='black', zorder =2)
                ax.plot([0, -ort_vector[0]], [0, -ort_vector[1]], color='black', zorder =2)
                
            if not feature[1] == 90:
                # plot dip vector
                ax.plot([0, vector[0]], [0, vector[1]], color='black', zorder =2)
                
            ax.set_xlim(-1.5, 1.5)
            ax.set_ylim(-1.5, 1.5)
            ax.set_aspect('equal')
        
        
        elif mode == 'line':
            xlim_dip = np.cos(aux(feature[0]))
            ylim_dip = np.sin(aux(feature[0]))

            if feature[1] == 90:
                vector = np.array([xlim_dip, ylim_dip])
                
                # Orthogonaler Vektor
                ort_vector = np.array([-vector[1], vector[0]])
                
                # Strike-Vektor zeichnen
                ax.plot([0, vector[0]], [0, vector[1]], color='black', zorder =2)
                ax.plot([0, -vector[0]], [0, -vector[1]], color='black', zorder =2)
                
                ax.plot([0, -ort_vector[0]], [0, -ort_vector[1]], color='black', zorder =2)
                ax.plot([0, ort_vector[0]], [0, ort_vector[1]], color='black', zorder =2)
                circle = Circle((0, 0), 0.08, fill=True, color='black', zorder =2)
                ax.add_patch(circle)
                
            elif feature[1] == 0:
                ax.arrow(0, 0, xlim_dip*0.5, ylim_dip*0.5, head_width=0.1, head_length=0.2, fc='black', ec='black', zorder =2)
                ax.arrow(0, 0, -xlim_dip*0.5, -ylim_dip*0.5, head_width=0.1, head_length=0.2, fc='black', ec='black', zorder =2)
                
            else:
                ax.arrow(0, 0, xlim_dip, ylim_dip, head_width=0.1, head_length=0.2, fc='black', ec='black', zorder =2)
                
            ax.set_xlim(-1.5, 1.5)
            ax.set_ylim(-1.5, 1.5)
            ax.set_aspect('equal')
        
        if not (feature[1] == 90 or feature[1] == 0):
            x_label = np.cos(aux(feature[0])+np.pi/4)
            y_label = np.sin(aux(feature[0])+np.pi/4)
            ax.text(x_label, y_label, f'{feature[1]}', color='black', fontsize=10, zorder =2)
        
    
        ax.axis('off')
        
    for i in range(len(features), len(axs)):
        axs[i].axis('off')
    
    plt.tight_layout()
    if save == True:
        plt.savefig(path + name+'.pdf', format='pdf', dpi=300, bbox_inches='tight')
    plt.show()
    
        
# plot_strike_dip(features_ex1, 'plane',  path, 'geol_to_clar', save= True)
plot_strike_dip(features_ex2,'plane', path, 'clar_to_geol', save=True)
# plot_strike_dip(features_ex3,'line', path, 'lineation_features', save=True)
