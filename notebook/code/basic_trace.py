import numpy as np
import matplotlib.pyplot as plt
import types

from matplotlib.patches import Arc

def circarrow(self, diameter, cntr, startangle, angle, startarrow=False, endarrow=False, **kwargs):
    R = diameter / 2
    startangle_rad = np.radians(startangle)
    angle_rad = np.radians(angle)
    
    if startarrow:
        t1 = kwargs.get('head_length', 0.045)
        startX = R * np.cos(startangle_rad)
        startY = R * np.sin(startangle_rad)
        startDX =  1e-6 * R * np.sin(startangle_rad + t1)
        startDY = -1e-6 * R * np.cos(startangle_rad + t1)
        
        self.arrow(startX - startDX, startY - startDY, startDX, startDY, **kwargs)
        
    else:
        t1 = 0
        
    if endarrow:
        t2 = angle_rad - kwargs.get('head_length', 0.045)
        endX = R * np.cos(startangle_rad + angle_rad)
        endY = R * np.sin(startangle_rad + angle_rad)
        endDX = -1e-6 * R * np.sin(startangle_rad + t2)
        endDY =  1e-6 * R * np.cos(startangle_rad + t2)
        
        self.arrow(endX - endDX, endY - endDY, endDX, endDY, **kwargs)
        
    else:
        t2 = angle_rad

    arc = Arc(cntr, diameter, diameter,
              angle=startangle,
              theta1=np.rad2deg(t1),
              theta2=np.rad2deg(t2),
              linestyle='-',
              color=kwargs.get('color', 'k'))
    
    self.axes().add_patch(arc)

    
def parameter_trace():
    # setup
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.rcParams['figure.figsize'] = (9,9)
    plt.circarrow = types.MethodType(circarrow, plt)
    R = 0.85 / 2

    # axis
    plt.arrow(-0.05, 0, 0.53, 0, head_width=0.02, color='k')
    plt.arrow(0, -0.05, 0, 0.53, head_width=0.02, color='k')
    plt.text(0.51, 0.02, r'$x^0$', fontsize=18)
    plt.text(0.02, 0.51, r'$x^1$', fontsize=18)

    # sphere outline
    plt.circarrow(2*R, (0,0), -30, 150,
                  startarrow=False,
                  endarrow=False,
                  width=0,
                  head_width=.03,
                  head_length=.045,
                  length_includes_head=True,
                  color='gray')

    # cone and annotations
    a = np.pi / 5
    plt.arrow(0, 0, 0.93 * R * np.cos(a), 0.93 * R * np.sin(a),
              head_width=0.02, 
              color='k')

    plt.circarrow(0.45*R, (0,0), 0, np.rad2deg(a),
                  startarrow=False,
                  endarrow=True,
                  width=0,
                  head_width=.01,
                  head_length=.015,
                  length_includes_head=True,
                  color='k')

    plt.plot((R * np.cos(a), R * np.cos(a)), (R * np.sin(a), 0), 'r--')

    plt.text(0.11, 0.02, r'$\theta$', fontsize=18) 
    plt.text(0.18, 0.17, r'$R$', fontsize=18)
    plt.text(0.41, 0.15, r'$r = R\sin(\theta)$', fontsize=18)


    plt.axes().set_xlim(-0.25, 0.55)
    plt.axes().set_ylim(-0.25, 0.55)
    plt.axes().set_aspect(1)
    plt.axes().axis('off')


    plt.show()