import customtkinter
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.

from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

import numpy as np
import math

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

#Fet per Xavier Prats, Joan Giol, Rafael Esquius, Lluc Estruch

#Globals
rotM = np.array([[1.00,0.00,0.00],
                [0.00,1.00,0.00],
                [0.00,0.00,1.00]])

m0=np.array([0.00,0.00,0.00])
m1=np.array([0.00,0.00,0.00])

#Ball radious
r2=3
r=math.sqrt(r2)

eqmodule=0
#Functions to calcule:
def module(a,b,c):
    r=math.sqrt(a**2+b**2+c**2)
    return r
     
def quat2rotm(q0,q1,q2,q3):

    quatModule = np.sqrt(q0*q0+q1*q1+q2*q2+q3*q3)
    q0/=quatModule
    q1/=quatModule
    q2/=quatModule
    q3/=quatModule
    rotM[0,0] = q0*q0 + q1*q1 - q2*q2 - q3*q3
    rotM[0,1] = 2*q1*q2 - 2*q0*q3
    rotM[0,2] = 2*q1*q3 + 2*q0*q2
    rotM[1,0] = 2*q1*q2 + 2*q0*q3
    rotM[1,1] = q0*q0 - q1*q1 + q2*q2 - q3*q3
    rotM[1,2] = 2*q2*q3 - 2*q0*q1
    rotM[2,0] = 2*q1*q3 - 2*q0*q2
    rotM[2,1] = 2*q2*q3 + 2*q0*q1
    rotM[2,2] = q0*q0 - q1*q1 - q2*q2 + q3*q3
    return rotM

def quat2EA(x, y, z, w):
      
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(t0, t1)
    
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch = math.asin(t2)
    
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(t3, t4)
    
    return roll, pitch, yaw

def AA2rotm(axis1,axis2,axis3,angle):
        
        angle = np.deg2rad(angle)
        axisModule = np.sqrt(axis1*axis1+axis2*axis2+axis3*axis3)

        axis1/=axisModule
        axis2/=axisModule
        axis3/=axisModule
        rotM[0,0] = axis1*axis1 + (1-axis1*axis1)*math.cos(angle)
        rotM[0,1] = axis1*axis2*(1-math.cos(angle))-axis3*math.sin(angle)
        rotM[0,2] = axis1*axis3*(1-math.cos(angle))+axis2*math.sin(angle)
        rotM[1,0] = axis1*axis2*(1-math.cos(angle))+axis3*math.sin(angle)
        rotM[1,1] = axis2*axis2+(1-axis2*axis2)*math.cos(angle)
        rotM[1,2] = axis2*axis3*(1-math.cos(angle))-axis1*math.sin(angle)
        rotM[2,0] = axis1*axis3*(1-math.cos(angle))-axis2*math.sin(angle)
        rotM[2,1] = axis2*axis3*(1-math.cos(angle))+axis1*math.sin(angle)
        rotM[2,2] = axis3*axis3+(1-axis3*axis3)*math.cos(angle)
        
def AA2RV(a1,a2,a3,angle):
    RV=np.array([0.00,0.00,0.00])
    rvmodule=module(a1,a2,a3)
    a1=a1/rvmodule
    a2=a2/rvmodule
    a3=a3/rvmodule
    RV[0]=a1*angle
    RV[1]=a2*angle
    RV[2]=a3*angle
    return RV
    
def AA2quat(raxis, angle):
    quat=np.array([0.00,0.00,0.00,0.00])
    quat[0]=math.cos(angle/2)
    qvec=math.sin(angle/2)*(raxis/module(raxis[0],raxis[2],raxis[2]))
    quat[1]=qvec[0]
    quat[2]=qvec[1]
    quat[3]=qvec[2]
    return quat

def EA2rotm(theta,phi,psi):
    theta = np.deg2rad(theta)
    phi = np.deg2rad(phi)
    psi = np.deg2rad(psi)

    rotM[0,0] = math.cos(theta)*math.cos(psi)
    rotM[0,1] = math.cos(psi)*math.sin(theta)*math.sin(phi) - math.cos(phi)*math.sin(psi)
    rotM[0,2] = math.cos(psi)*math.cos(phi)*math.sin(theta) + math.sin(psi)*math.sin(phi)
    rotM[1,0] = math.cos(theta)*math.sin(psi)
    rotM[1,1] = math.sin(psi)*math.sin(theta)*math.sin(phi) + math.cos(phi)*math.cos(psi)
    rotM[1,2] = math.sin(psi)*math.sin(theta)*math.cos(phi) - math.cos(psi)*math.sin(phi)
    rotM[2,0] = -math.sin(theta)
    rotM[2,1] = math.cos(theta)*math.sin(phi)
    rotM[2,2] = math.cos(theta)*math.cos(phi)

def rotM2AA(R):
    # Calculate the angle of rotation
    angle = math.acos((np.trace(R) - 1) / 2)
    
    # Calculate the principal axis
    axis = (1 / (2 * math.sin(angle))) * np.array([R[2,1] - R[1,2], R[0,2] - R[2,0], R[1,0] - R[0,1]])
    
    return axis, angle

def rotm2EA(R):
    pitch = -np.arcsin(R[2,0])
    roll = np.arctan2(R[2,1]/np.cos(pitch),R[2,2]/np.cos(pitch))
    yaw = np.arctan2(R[1,0]/np.cos(pitch),R[0,0]/np.cos(pitch))
    return roll, pitch, yaw
#Functions to print:
def rotMprinted(self):
    self.entry_RotM_11.configure(state="normal")
    self.entry_RotM_11.delete(0,60)
    self.entry_RotM_11.insert(0,"{0:.4f}".format(rotM[0,0]))
    self.entry_RotM_11.configure(state="disabled")

    self.entry_RotM_12.configure(state="normal")
    self.entry_RotM_12.delete(0,60)
    self.entry_RotM_12.insert(0,"{0:.4f}".format(rotM[0,1]))
    self.entry_RotM_12.configure(state="disabled")

    self.entry_RotM_13.configure(state="normal")
    self.entry_RotM_13.delete(0,60)
    self.entry_RotM_13.insert(0,"{0:.4f}".format(rotM[0,2]))
    self.entry_RotM_13.configure(state="disabled")

    self.entry_RotM_21.configure(state="normal")
    self.entry_RotM_21.delete(0,60)
    self.entry_RotM_21.insert(0,"{0:.4f}".format(rotM[1,0]))
    self.entry_RotM_21.configure(state="disabled")

    self.entry_RotM_22.configure(state="normal")
    self.entry_RotM_22.delete(0,60)
    self.entry_RotM_22.insert(0,"{0:.4f}".format(rotM[1,1]))
    self.entry_RotM_22.configure(state="disabled")

    self.entry_RotM_23.configure(state="normal")
    self.entry_RotM_23.delete(0,60)
    self.entry_RotM_23.insert(0,"{0:.4f}".format(rotM[1,2]))
    self.entry_RotM_23.configure(state="disabled")
    
    self.entry_RotM_31.configure(state="normal")
    self.entry_RotM_31.delete(0,60)
    self.entry_RotM_31.insert(0,"{0:.4f}".format(rotM[2,0]))
    self.entry_RotM_31.configure(state="disabled")
    
    self.entry_RotM_32.configure(state="normal")
    self.entry_RotM_32.delete(0,60)
    self.entry_RotM_32.insert(0,"{0:.4f}".format(rotM[2,1]))
    self.entry_RotM_32.configure(state="disabled")

    self.entry_RotM_33.configure(state="normal")
    self.entry_RotM_33.delete(0,60)
    self.entry_RotM_33.insert(0,"{0:.4f}".format(rotM[2,2]))
    self.entry_RotM_33.configure(state="disabled")

    self.M = rotM.dot(self.M)
    self.update_cube()

    pass

def AAprinted(self,raxis,angle):
    self.entry_AA_angle.delete(0,50)
    self.entry_AA_angle.insert(0,"{0:.4f}".format(np.rad2deg(angle)))
    self.entry_AA_ax1.delete(0,50)
    self.entry_AA_ax1.insert(0,"{0:.4f}".format(raxis[0]))
    self.entry_AA_ax2.delete(0,50)
    self.entry_AA_ax2.insert(0,"{0:.4f}".format(raxis[1]))
    self.entry_AA_ax3.delete(0,50)
    self.entry_AA_ax3.insert(0,"{0:.4f}".format(raxis[2]))
    pass

def RVprinted(self,Rv):

    self.entry_rotV_1.delete(0,50)
    self.entry_rotV_1.insert(0,"{0:.4f}".format(Rv[0]))
    self.entry_rotV_2.delete(0,50)
    self.entry_rotV_2.insert(0,"{0:.4f}".format(Rv[1]))
    self.entry_rotV_3.delete(0,50)
    self.entry_rotV_3.insert(0,"{0:.4f}".format(Rv[2]))
    pass

def EAprinted(self,roll, pitch, yaw):
    self.entry_EA_roll.delete(0,50)
    self.entry_EA_roll.insert(0,"{0:.4f}".format(np.rad2deg(roll)))
    self.entry_EA_pitch.delete(0,50)
    self.entry_EA_pitch.insert(0,"{0:.4f}".format(np.rad2deg(pitch)))
    self.entry_EA_yaw.delete(0,50)
    self.entry_EA_yaw.insert(0,"{0:.4f}".format(np.rad2deg(yaw)))

def quatprinted(self, quat):
    self.entry_quat_0.delete(0,50)
    self.entry_quat_0.insert(0,"{0:.4f}".format(quat[0]))
    self.entry_quat_1.delete(0,50)
    self.entry_quat_1.insert(0,"{0:.4f}".format(quat[1]))
    self.entry_quat_2.delete(0,50)
    self.entry_quat_2.insert(0,"{0:.4f}".format(quat[2]))
    self.entry_quat_3.delete(0,50)
    self.entry_quat_3.insert(0,"{0:.4f}".format(quat[3]))

class Arcball(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        # Orientation vars. Initialized to represent 0 rotation
        self.quat = np.array([[1],[0],[0],[0]])
        self.rotM = np.eye(3)
        self.AA = {"axis": np.array([[0],[0],[0]]), "angle":0.0}
        self.rotv = np.array([[0],[0],[0]])
        self.euler = np.array([[0],[0],[0]])

        # configure window
        self.title("Holroyd's arcball")
        self.geometry(f"{1100}x{580}")
        self.resizable(False, False)

        self.grid_columnconfigure((0,1), weight=0   )
        self.grid_rowconfigure((0,1), weight=1)
        self.grid_rowconfigure(2, weight=0)

        # Cube plot
        self.init_cube()

        self.canvas = FigureCanvasTkAgg(self.fig, self)  # A tk.DrawingArea.
        self.bm = BlitManager(self.canvas,[self.facesObj])
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.pressed = False #Bool to bypass the information that mouse is clicked
        self.canvas.mpl_connect('button_press_event', self.onclick)
        self.canvas.mpl_connect('motion_notify_event', self.onmove)
        self.canvas.mpl_connect('button_release_event', self.onrelease)
        
        # Reset button
        self.resetbutton = customtkinter.CTkButton(self, text="Reset", command=self.resetbutton_pressed)
        self.resetbutton.grid(row=3, column=0, padx=(0, 0), pady=(5, 20), sticky="ns")
        
        # Selectable atti
        self.tabview = customtkinter.CTkTabview(self, width=150, height=150)
        self.tabview.grid(row=0, column=1, padx=(0, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Axis angle")
        self.tabview.add("Rotation vector")
        self.tabview.add("Euler angles")
        self.tabview.add("Quaternion")

        # Selectable atti: AA
        self.tabview.tab("Axis angle").grid_columnconfigure(0, weight=0)  # configure grid of individual tabs
        self.tabview.tab("Axis angle").grid_columnconfigure(1, weight=0)  # configure grid of individual tabs

        self.label_AA_axis= customtkinter.CTkLabel(self.tabview.tab("Axis angle"), text="Axis:")
        self.label_AA_axis.grid(row=0, column=0, rowspan=3, padx=(80,0), pady=(45,0), sticky="e")

        self.entry_AA_ax1 = customtkinter.CTkEntry(self.tabview.tab("Axis angle"))
        self.entry_AA_ax1.insert(0,"1.0")
        self.entry_AA_ax1.grid(row=0, column=1, padx=(5, 0), pady=(50, 0), sticky="ew")

        self.entry_AA_ax2 = customtkinter.CTkEntry(self.tabview.tab("Axis angle"))
        self.entry_AA_ax2.insert(0,"0.0")
        self.entry_AA_ax2.grid(row=1, column=1, padx=(5, 0), pady=(5, 0), sticky="ew")

        self.entry_AA_ax3 = customtkinter.CTkEntry(self.tabview.tab("Axis angle"))
        self.entry_AA_ax3.insert(0,"0.0")
        self.entry_AA_ax3.grid(row=2, column=1, padx=(5, 0), pady=(5, 10), sticky="ew")

        self.label_AA_angle = customtkinter.CTkLabel(self.tabview.tab("Axis angle"), text="Angle:")
        self.label_AA_angle.grid(row=3, column=0, padx=(120,0), pady=(10, 20),sticky="w")
        self.entry_AA_angle = customtkinter.CTkEntry(self.tabview.tab("Axis angle"))
        self.entry_AA_angle.insert(0,"0.0")
        self.entry_AA_angle.grid(row=3, column=1, padx=(5, 0), pady=(0, 10), sticky="ew")

        self.button_AA = customtkinter.CTkButton(self.tabview.tab("Axis angle"), text="Apply", command=self.apply_AA, width=180)
        self.button_AA.grid(row=5, column=0, columnspan=2, padx=(0, 0), pady=(5, 0), sticky="e")

        # Selectable atti: rotV
        self.tabview.tab("Rotation vector").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Rotation vector").grid_columnconfigure(1, weight=0)
        
        self.label_rotV= customtkinter.CTkLabel(self.tabview.tab("Rotation vector"), text="rot. Vector:")
        self.label_rotV.grid(row=0, column=0, rowspan=3, padx=(2,0), pady=(45,0), sticky="e")

        self.entry_rotV_1 = customtkinter.CTkEntry(self.tabview.tab("Rotation vector"))
        self.entry_rotV_1.insert(0,"0.0")
        self.entry_rotV_1.grid(row=0, column=1, padx=(5, 60), pady=(50, 0), sticky="ew")

        self.entry_rotV_2 = customtkinter.CTkEntry(self.tabview.tab("Rotation vector"))
        self.entry_rotV_2.insert(0,"0.0")
        self.entry_rotV_2.grid(row=1, column=1, padx=(5, 60), pady=(5, 0), sticky="ew")

        self.entry_rotV_3 = customtkinter.CTkEntry(self.tabview.tab("Rotation vector"))
        self.entry_rotV_3.insert(0,"0.0")
        self.entry_rotV_3.grid(row=2, column=1, padx=(5, 60), pady=(5, 10), sticky="ew")

        self.button_rotV = customtkinter.CTkButton(self.tabview.tab("Rotation vector"), text="Apply", command=self.apply_rotV, width=180)
        self.button_rotV.grid(row=5, column=0, columnspan=2, padx=(0, 60), pady=(5, 0), sticky="e")

        # Selectable atti: Euler angles
        self.tabview.tab("Euler angles").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Euler angles").grid_columnconfigure(1, weight=0)
        
        self.label_EA_roll= customtkinter.CTkLabel(self.tabview.tab("Euler angles"), text="roll:")
        self.label_EA_roll.grid(row=0, column=0, padx=(2,0), pady=(50,0), sticky="e")

        self.label_EA_pitch= customtkinter.CTkLabel(self.tabview.tab("Euler angles"), text="pitch:")
        self.label_EA_pitch.grid(row=1, column=0, padx=(2,0), pady=(5,0), sticky="e")

        self.label_EA_yaw= customtkinter.CTkLabel(self.tabview.tab("Euler angles"), text="yaw:")
        self.label_EA_yaw.grid(row=2, column=0, rowspan=3, padx=(2,0), pady=(5,10), sticky="e")

        self.entry_EA_roll = customtkinter.CTkEntry(self.tabview.tab("Euler angles"))
        self.entry_EA_roll.insert(0,"0.0")
        self.entry_EA_roll.grid(row=0, column=1, padx=(5, 60), pady=(50, 0), sticky="ew")

        self.entry_EA_pitch = customtkinter.CTkEntry(self.tabview.tab("Euler angles"))
        self.entry_EA_pitch.insert(0,"0.0")
        self.entry_EA_pitch.grid(row=1, column=1, padx=(5, 60), pady=(5, 0), sticky="ew")

        self.entry_EA_yaw = customtkinter.CTkEntry(self.tabview.tab("Euler angles"))
        self.entry_EA_yaw.insert(0,"0.0")
        self.entry_EA_yaw.grid(row=2, column=1, padx=(5, 60), pady=(5, 10), sticky="ew")

        self.button_EA = customtkinter.CTkButton(self.tabview.tab("Euler angles"), text="Apply", command=self.apply_EA, width=180)
        self.button_EA.grid(row=5, column=0, columnspan=2, padx=(0, 60), pady=(5, 0), sticky="e")

        # Selectable atti: Quaternion
        self.tabview.tab("Quaternion").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Quaternion").grid_columnconfigure(1, weight=0)
        
        self.label_quat_0= customtkinter.CTkLabel(self.tabview.tab("Quaternion"), text="q0:")
        self.label_quat_0.grid(row=0, column=0, padx=(2,0), pady=(50,0), sticky="e")

        self.label_quat_1= customtkinter.CTkLabel(self.tabview.tab("Quaternion"), text="q1:")
        self.label_quat_1.grid(row=1, column=0, padx=(2,0), pady=(5,0), sticky="e")

        self.label_quat_2= customtkinter.CTkLabel(self.tabview.tab("Quaternion"), text="q2:")
        self.label_quat_2.grid(row=2, column=0, padx=(2,0), pady=(5,0), sticky="e")

        self.label_quat_3= customtkinter.CTkLabel(self.tabview.tab("Quaternion"), text="q3:")
        self.label_quat_3.grid(row=3, column=0, padx=(2,0), pady=(5,10), sticky="e")

        self.entry_quat_0 = customtkinter.CTkEntry(self.tabview.tab("Quaternion"))
        self.entry_quat_0.insert(0,"1.0")
        self.entry_quat_0.grid(row=0, column=1, padx=(5, 60), pady=(50, 0), sticky="ew")

        self.entry_quat_1 = customtkinter.CTkEntry(self.tabview.tab("Quaternion"))
        self.entry_quat_1.insert(0,"0.0")
        self.entry_quat_1.grid(row=1, column=1, padx=(5, 60), pady=(5, 0), sticky="ew")

        self.entry_quat_2 = customtkinter.CTkEntry(self.tabview.tab("Quaternion"))
        self.entry_quat_2.insert(0,"0.0")
        self.entry_quat_2.grid(row=2, column=1, padx=(5, 60), pady=(5, 0), sticky="ew")

        self.entry_quat_3 = customtkinter.CTkEntry(self.tabview.tab("Quaternion"))
        self.entry_quat_3.insert(0,"0.0")
        self.entry_quat_3.grid(row=3, column=1, padx=(5, 60), pady=(5, 10), sticky="ew")

        self.button_quat = customtkinter.CTkButton(self.tabview.tab("Quaternion"), text="Apply", command=self.apply_quat, width=180)
        self.button_quat.grid(row=4, column=0, columnspan=2, padx=(0, 60), pady=(5, 0), sticky="e")

        # Rotation matrix info
        self.RotMFrame = customtkinter.CTkFrame(self, width=150)
        self.RotMFrame.grid(row=1, column=1, rowspan=3, padx=(0, 20), pady=(20, 20), sticky="nsew")

        self.RotMFrame.grid_columnconfigure((0,1,2,3,4), weight=1)

        self.label_RotM= customtkinter.CTkLabel(self.RotMFrame, text="RotM = ")
        self.label_RotM.grid(row=0, column=0, rowspan=3, padx=(2,0), pady=(20,0), sticky="e")

        self.entry_RotM_11= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_11.insert(0,rotM[0,0])
        self.entry_RotM_11.configure(state="disabled")
        self.entry_RotM_11.grid(row=0, column=1, padx=(2,0), pady=(20,0), sticky="ew")


        self.entry_RotM_12= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_12.insert(0,rotM[0,1])
        self.entry_RotM_12.configure(state="disabled")
        self.entry_RotM_12.grid(row=0, column=2, padx=(2,0), pady=(20,0), sticky="ew")

        self.entry_RotM_13= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_13.insert(0,rotM[0,2])
        self.entry_RotM_13.configure(state="disabled")
        self.entry_RotM_13.grid(row=0, column=3, padx=(2,0), pady=(20,0), sticky="ew")

        self.entry_RotM_21= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_21.insert(0,rotM[1,0])
        self.entry_RotM_21.configure(state="disabled")
        self.entry_RotM_21.grid(row=1, column=1, padx=(2,0), pady=(2,0), sticky="ew")

        self.entry_RotM_22= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_22.insert(0,rotM[1,1])
        self.entry_RotM_22.configure(state="disabled")
        self.entry_RotM_22.grid(row=1, column=2, padx=(2,0), pady=(2,0), sticky="ew")

        self.entry_RotM_23= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_23.insert(0,rotM[1,2])
        self.entry_RotM_23.configure(state="disabled")
        self.entry_RotM_23.grid(row=1, column=3, padx=(2,0), pady=(2,0), sticky="ew")

        self.entry_RotM_31= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_31.insert(0,rotM[2,0])
        self.entry_RotM_31.configure(state="disabled")
        self.entry_RotM_31.grid(row=2, column=1, padx=(2,0), pady=(2,0), sticky="ew")

        self.entry_RotM_32= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_32.insert(0,rotM[2,1])
        self.entry_RotM_32.configure(state="disabled")
        self.entry_RotM_32.grid(row=2, column=2, padx=(2,0), pady=(2,0), sticky="ew")

        self.entry_RotM_33= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_33.insert(0,rotM[2,2])
        self.entry_RotM_33.configure(state="disabled")
        self.entry_RotM_33.grid(row=2, column=3, padx=(2,0), pady=(2,0), sticky="ew")
    
    def resetbutton_pressed(self):
        """
        Event triggered function on the event of a push on the button Reset
        """
        rotM = np.array([[1.00,0.00,0.00],
        [0.00,1.00,0.00],
        [0.00,0.00,1.00]])

        # Orientation vars. Initialized to represent 0 rotation
        self.quat = np.array([[1],[0],[0],[0]])
        self.rotM = np.eye(3)
        self.AA = {"axis": np.array([[0],[0],[0]]), "angle":0.0}
        self.rotv = np.array([[0],[0],[0]])
        self.euler = np.array([[0],[0],[0]])

        # configure window
        self.title("Holroyd's arcball")
        self.geometry(f"{1100}x{580}")
        self.resizable(False, False)

        self.grid_columnconfigure((0,1), weight=0   )
        self.grid_rowconfigure((0,1), weight=1)
        self.grid_rowconfigure(2, weight=0)

        # Cube plot
        self.init_cube()

        self.canvas = FigureCanvasTkAgg(self.fig, self)  # A tk.DrawingArea.
        self.bm = BlitManager(self.canvas,[self.facesObj])
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.pressed = False #Bool to bypass the information that mouse is clicked
        self.canvas.mpl_connect('button_press_event', self.onclick)
        self.canvas.mpl_connect('motion_notify_event', self.onmove)
        self.canvas.mpl_connect('button_release_event', self.onrelease)
        
        # Reset button
        self.resetbutton = customtkinter.CTkButton(self, text="Reset", command=self.resetbutton_pressed)
        self.resetbutton.grid(row=3, column=0, padx=(0, 0), pady=(5, 20), sticky="ns")
        
        # Selectable atti
        self.tabview = customtkinter.CTkTabview(self, width=150, height=150)
        self.tabview.grid(row=0, column=1, padx=(0, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Axis angle")
        self.tabview.add("Rotation vector")
        self.tabview.add("Euler angles")
        self.tabview.add("Quaternion")

        # Selectable atti: AA
        self.tabview.tab("Axis angle").grid_columnconfigure(0, weight=0)  # configure grid of individual tabs
        self.tabview.tab("Axis angle").grid_columnconfigure(1, weight=0)  # configure grid of individual tabs

        self.label_AA_axis= customtkinter.CTkLabel(self.tabview.tab("Axis angle"), text="Axis:")
        self.label_AA_axis.grid(row=0, column=0, rowspan=3, padx=(80,0), pady=(45,0), sticky="e")

        self.entry_AA_ax1 = customtkinter.CTkEntry(self.tabview.tab("Axis angle"))
        self.entry_AA_ax1.insert(0,"1.0")
        self.entry_AA_ax1.grid(row=0, column=1, padx=(5, 0), pady=(50, 0), sticky="ew")

        self.entry_AA_ax2 = customtkinter.CTkEntry(self.tabview.tab("Axis angle"))
        self.entry_AA_ax2.insert(0,"0.0")
        self.entry_AA_ax2.grid(row=1, column=1, padx=(5, 0), pady=(5, 0), sticky="ew")

        self.entry_AA_ax3 = customtkinter.CTkEntry(self.tabview.tab("Axis angle"))
        self.entry_AA_ax3.insert(0,"0.0")
        self.entry_AA_ax3.grid(row=2, column=1, padx=(5, 0), pady=(5, 10), sticky="ew")

        self.label_AA_angle = customtkinter.CTkLabel(self.tabview.tab("Axis angle"), text="Angle:")
        self.label_AA_angle.grid(row=3, column=0, padx=(120,0), pady=(10, 20),sticky="w")
        self.entry_AA_angle = customtkinter.CTkEntry(self.tabview.tab("Axis angle"))
        self.entry_AA_angle.insert(0,"0.0")
        self.entry_AA_angle.grid(row=3, column=1, padx=(5, 0), pady=(0, 10), sticky="ew")

        self.button_AA = customtkinter.CTkButton(self.tabview.tab("Axis angle"), text="Apply", command=self.apply_AA, width=180)
        self.button_AA.grid(row=5, column=0, columnspan=2, padx=(0, 0), pady=(5, 0), sticky="e")

        # Selectable atti: rotV
        self.tabview.tab("Rotation vector").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Rotation vector").grid_columnconfigure(1, weight=0)
        
        self.label_rotV= customtkinter.CTkLabel(self.tabview.tab("Rotation vector"), text="rot. Vector:")
        self.label_rotV.grid(row=0, column=0, rowspan=3, padx=(2,0), pady=(45,0), sticky="e")

        self.entry_rotV_1 = customtkinter.CTkEntry(self.tabview.tab("Rotation vector"))
        self.entry_rotV_1.insert(0,"0.0")
        self.entry_rotV_1.grid(row=0, column=1, padx=(5, 60), pady=(50, 0), sticky="ew")

        self.entry_rotV_2 = customtkinter.CTkEntry(self.tabview.tab("Rotation vector"))
        self.entry_rotV_2.insert(0,"0.0")
        self.entry_rotV_2.grid(row=1, column=1, padx=(5, 60), pady=(5, 0), sticky="ew")

        self.entry_rotV_3 = customtkinter.CTkEntry(self.tabview.tab("Rotation vector"))
        self.entry_rotV_3.insert(0,"0.0")
        self.entry_rotV_3.grid(row=2, column=1, padx=(5, 60), pady=(5, 10), sticky="ew")

        self.button_rotV = customtkinter.CTkButton(self.tabview.tab("Rotation vector"), text="Apply", command=self.apply_rotV, width=180)
        self.button_rotV.grid(row=5, column=0, columnspan=2, padx=(0, 60), pady=(5, 0), sticky="e")

        # Selectable atti: Euler angles
        self.tabview.tab("Euler angles").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Euler angles").grid_columnconfigure(1, weight=0)
        
        self.label_EA_roll= customtkinter.CTkLabel(self.tabview.tab("Euler angles"), text="roll:")
        self.label_EA_roll.grid(row=0, column=0, padx=(2,0), pady=(50,0), sticky="e")

        self.label_EA_pitch= customtkinter.CTkLabel(self.tabview.tab("Euler angles"), text="pitch:")
        self.label_EA_pitch.grid(row=1, column=0, padx=(2,0), pady=(5,0), sticky="e")

        self.label_EA_yaw= customtkinter.CTkLabel(self.tabview.tab("Euler angles"), text="yaw:")
        self.label_EA_yaw.grid(row=2, column=0, rowspan=3, padx=(2,0), pady=(5,10), sticky="e")

        self.entry_EA_roll = customtkinter.CTkEntry(self.tabview.tab("Euler angles"))
        self.entry_EA_roll.insert(0,"0.0")
        self.entry_EA_roll.grid(row=0, column=1, padx=(5, 60), pady=(50, 0), sticky="ew")

        self.entry_EA_pitch = customtkinter.CTkEntry(self.tabview.tab("Euler angles"))
        self.entry_EA_pitch.insert(0,"0.0")
        self.entry_EA_pitch.grid(row=1, column=1, padx=(5, 60), pady=(5, 0), sticky="ew")

        self.entry_EA_yaw = customtkinter.CTkEntry(self.tabview.tab("Euler angles"))
        self.entry_EA_yaw.insert(0,"0.0")
        self.entry_EA_yaw.grid(row=2, column=1, padx=(5, 60), pady=(5, 10), sticky="ew")

        self.button_EA = customtkinter.CTkButton(self.tabview.tab("Euler angles"), text="Apply", command=self.apply_EA, width=180)
        self.button_EA.grid(row=5, column=0, columnspan=2, padx=(0, 60), pady=(5, 0), sticky="e")

        # Selectable atti: Quaternion
        self.tabview.tab("Quaternion").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Quaternion").grid_columnconfigure(1, weight=0)
        
        self.label_quat_0= customtkinter.CTkLabel(self.tabview.tab("Quaternion"), text="q0:")
        self.label_quat_0.grid(row=0, column=0, padx=(2,0), pady=(50,0), sticky="e")

        self.label_quat_1= customtkinter.CTkLabel(self.tabview.tab("Quaternion"), text="q1:")
        self.label_quat_1.grid(row=1, column=0, padx=(2,0), pady=(5,0), sticky="e")

        self.label_quat_2= customtkinter.CTkLabel(self.tabview.tab("Quaternion"), text="q2:")
        self.label_quat_2.grid(row=2, column=0, padx=(2,0), pady=(5,0), sticky="e")

        self.label_quat_3= customtkinter.CTkLabel(self.tabview.tab("Quaternion"), text="q3:")
        self.label_quat_3.grid(row=3, column=0, padx=(2,0), pady=(5,10), sticky="e")

        self.entry_quat_0 = customtkinter.CTkEntry(self.tabview.tab("Quaternion"))
        self.entry_quat_0.insert(0,"1.0")
        self.entry_quat_0.grid(row=0, column=1, padx=(5, 60), pady=(50, 0), sticky="ew")

        self.entry_quat_1 = customtkinter.CTkEntry(self.tabview.tab("Quaternion"))
        self.entry_quat_1.insert(0,"0.0")
        self.entry_quat_1.grid(row=1, column=1, padx=(5, 60), pady=(5, 0), sticky="ew")

        self.entry_quat_2 = customtkinter.CTkEntry(self.tabview.tab("Quaternion"))
        self.entry_quat_2.insert(0,"0.0")
        self.entry_quat_2.grid(row=2, column=1, padx=(5, 60), pady=(5, 0), sticky="ew")

        self.entry_quat_3 = customtkinter.CTkEntry(self.tabview.tab("Quaternion"))
        self.entry_quat_3.insert(0,"0.0")
        self.entry_quat_3.grid(row=3, column=1, padx=(5, 60), pady=(5, 10), sticky="ew")

        self.button_quat = customtkinter.CTkButton(self.tabview.tab("Quaternion"), text="Apply", command=self.apply_quat, width=180)
        self.button_quat.grid(row=4, column=0, columnspan=2, padx=(0, 60), pady=(5, 0), sticky="e")

        # Rotation matrix info
        self.RotMFrame = customtkinter.CTkFrame(self, width=150)
        self.RotMFrame.grid(row=1, column=1, rowspan=3, padx=(0, 20), pady=(20, 20), sticky="nsew")

        self.RotMFrame.grid_columnconfigure((0,1,2,3,4), weight=1)

        self.label_RotM= customtkinter.CTkLabel(self.RotMFrame, text="RotM = ")
        self.label_RotM.grid(row=0, column=0, rowspan=3, padx=(2,0), pady=(20,0), sticky="e")

        self.entry_RotM_11= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_11.insert(0,rotM[0,0])
        self.entry_RotM_11.configure(state="disabled")
        self.entry_RotM_11.grid(row=0, column=1, padx=(2,0), pady=(20,0), sticky="ew")


        self.entry_RotM_12= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_12.insert(0,rotM[0,1])
        self.entry_RotM_12.configure(state="disabled")
        self.entry_RotM_12.grid(row=0, column=2, padx=(2,0), pady=(20,0), sticky="ew")

        self.entry_RotM_13= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_13.insert(0,rotM[0,2])
        self.entry_RotM_13.configure(state="disabled")
        self.entry_RotM_13.grid(row=0, column=3, padx=(2,0), pady=(20,0), sticky="ew")

        self.entry_RotM_21= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_21.insert(0,rotM[1,0])
        self.entry_RotM_21.configure(state="disabled")
        self.entry_RotM_21.grid(row=1, column=1, padx=(2,0), pady=(2,0), sticky="ew")

        self.entry_RotM_22= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_22.insert(0,rotM[1,1])
        self.entry_RotM_22.configure(state="disabled")
        self.entry_RotM_22.grid(row=1, column=2, padx=(2,0), pady=(2,0), sticky="ew")

        self.entry_RotM_23= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_23.insert(0,rotM[1,2])
        self.entry_RotM_23.configure(state="disabled")
        self.entry_RotM_23.grid(row=1, column=3, padx=(2,0), pady=(2,0), sticky="ew")

        self.entry_RotM_31= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_31.insert(0,rotM[2,0])
        self.entry_RotM_31.configure(state="disabled")
        self.entry_RotM_31.grid(row=2, column=1, padx=(2,0), pady=(2,0), sticky="ew")

        self.entry_RotM_32= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_32.insert(0,rotM[2,1])
        self.entry_RotM_32.configure(state="disabled")
        self.entry_RotM_32.grid(row=2, column=2, padx=(2,0), pady=(2,0), sticky="ew")

        self.entry_RotM_33= customtkinter.CTkEntry(self.RotMFrame, width=50, border_width=0)
        self.entry_RotM_33.insert(0,rotM[2,2])
        self.entry_RotM_33.configure(state="disabled")
        self.entry_RotM_33.grid(row=2, column=3, padx=(2,0), pady=(2,0), sticky="ew")
        print("reset")

    def apply_AA(self):
        """
        Event triggered function on the event of a push on the button button_AA
        """
       #Example on how to get values from entries:
        angle = float (self.entry_AA_angle.get())
        axis1 = float (self.entry_AA_ax1.get())
        axis2 = float (self.entry_AA_ax2.get())
        axis3 = float (self.entry_AA_ax3.get())
        
        AA2rotm(axis1,axis2,axis3,angle)
        rotMprinted(self)

        #Change the other parameters
        #Axis and angle to Rotation Vector
        rv=AA2RV(axis1,axis2,axis3, np.deg2rad(angle))
        RVprinted(self,rv)

        #Rotm to EA
        roll, pitch, yaw = rotm2EA(rotM)
        EAprinted(self,roll, pitch, yaw)

        #AA to quat
        raxis = np.array([axis1,axis2,axis3])
        quat=AA2quat(raxis,np.deg2rad(angle))
        quatprinted(self, quat)

        pass

    def apply_rotV(self):
        """
        Event triggered function on the event of a push on the button button_rotV 
        """
        pa1=float(self.entry_rotV_1.get())
        pa2=float(self.entry_rotV_2.get())
        pa3=float(self.entry_rotV_3.get())

        angle=np.sqrt((pa1* pa1)+(pa2* pa2)+(pa3*pa3))

        axis1=pa1/angle
        axis2=pa2/angle
        axis3=pa3/angle    

        AA2rotm(axis1,axis2,axis3,np.rad2deg(angle))
        rotMprinted(self)

        #Change other parameters
        #Printing the previously extracted principal axis and angle
        raxis=np.array([axis1,axis2,axis3])
        AAprinted(self,raxis,angle)

        #Rotm to EA
        roll, pitch, yaw = rotm2EA(rotM)
        EAprinted(self,roll, pitch, yaw)

        #AA to quat
        quat=AA2quat(raxis,angle)
        quatprinted(self, quat)
        pass
 
    def apply_EA(self):
        """
        Event triggered function on the event of a push on the button button_EA
        """
        theta = float (self.entry_EA_pitch.get())
        phi = float (self.entry_EA_roll.get())
        psi = float (self.entry_EA_yaw.get())

        EA2rotm(theta,phi,psi)
        rotMprinted(self)

        #Change other parameters
        axis, angle=rotM2AA(rotM)

        AAprinted(self,axis,angle)

        rv=AA2RV(axis[0],axis[1],axis[2],angle)
        RVprinted(self,rv)

        quat=AA2quat(axis,angle)
        quatprinted(self, quat)


        pass
 
    def apply_quat(self):
        """
        Event triggered function on the event of a push on the button button_quat
        """
        q0 = float (self.entry_quat_0.get())
        q1 = float (self.entry_quat_1.get())
        q2 = float (self.entry_quat_2.get())
        q3 = float (self.entry_quat_3.get())

        rotM=quat2rotm(q0,q1,q2,q3)
        rotMprinted(self)

        axis, angle=rotM2AA(rotM)

        AAprinted(self,axis,angle)

        rv=AA2RV(axis[0],axis[1],axis[2], angle)
        RVprinted(self,rv)

        roll, pitch, yaw = rotm2EA(rotM)
        EAprinted(self,roll, pitch, yaw)

        pass
  
    def onclick(self, event):
        """
        Event triggered function on the event of a mouse click inside the figure canvas
        """
        #Save mouse coordinates
        x1,y1= self.canvas_coordinates_to_figure_coordinates(event.x,event.y)
        #Calcule module
        eqmodule=module(x1,y1,(r2/(2*math.sqrt(x1**2+y1**2))))
        #Use the given formula
        if((x1**2+y1**2)<(1/2)*r2):
            m0[0]=y1
            m0[1]=math.sqrt(r2-(x1**2)-(y1**2))
            m0[2]=-x1

        if((x1**2+y1**2)>=(1/2)*r2):
            m0[0]= (r*y1)/eqmodule
            m0[1]= (r*(r2/(2*math.sqrt(x1**2+y1**2))))/eqmodule
            m0[2]= -(r*x1)/eqmodule
            
        print("Pressed button", event.button)

        if event.button:
            self.pressed = True # Bool to control(activate) a drag (click+move)

    def onmove(self,event):
        """
        Event triggered function on the event of a mouse motion
        """
        if self.pressed: #Only triggered if previous click
            
            #Save mouse coordinates
            x1,y1= self.canvas_coordinates_to_figure_coordinates(event.x,event.y)
            #Calcule module
            eqmodule=module(x1,y1,(r2/(2*math.sqrt(x1**2+y1**2))))
            #Use the given formula
            if((x1**2+y1**2)<(1/2)*r2):
                m1[0]=y1
                m1[1]=math.sqrt(r2-(x1**2)-(y1**2))
                m1[2]=-x1

            if((x1**2+y1**2)>=(1/2)*r2):
                m1[0]= (r*y1)/eqmodule
                m1[1]= (r*(r2/(2*math.sqrt(x1**2+y1**2))))/eqmodule
                m1[2]= -(r*x1)/eqmodule
            #Calculate the angle with the formula
            angle=math.acos(np.dot(m0,m1)/(module(m0[0],m0[1],m0[2])*module(m1[0],m1[1],m1[2])))
            #The axis is the cross product since it gives a perpendicular angle to both elements 
            raxis=np.cross(m0,m1)
            
            #Call the function that transforms a principal axis and angle to a quaternion
            quat=AA2quat(raxis,angle)
            
            #Call the function that prints the Axis and angle
            AAprinted(self, raxis, angle)

            #Call the function that given an axis and angle returns a rotation vector
            rv=AA2RV(raxis[0],raxis[1],raxis[2],angle)

            #Call the function that prints the rotation vector
            RVprinted(self, rv)

            #Call the function that given a quaternion returns a set of Euler angles
            angle1,angle2,angle3 = quat2EA(quat[1],quat[2],quat[3],quat[0])

            #Call the function that prints the euler angles
            EAprinted(self,angle1,angle2,angle3)

            #Call the function that prints the quaternion
            quatprinted(self, quat)

            #Call the function that transforms a quaternion into a rotation matrix
            quat2rotm(quat[0],quat[1],quat[2],quat[3])  

            #Call the function that  prints the rotation matrix
            rotMprinted(self)
            self.update_cube() #Update the cube
            #Save the actual m1 in m0, so we can use it in the next loop
            m0[0]=m1[0]
            m0[1]=m1[1]
            m0[2]=m1[2]

    def onrelease(self,event):
        """
        Event triggered function on the event of a mouse release
        """
        self.pressed = False # Bool to control(deactivate) a drag (click+move)

    def init_cube(self):
        """
        Initialization function that sets up cube's geometry and plot information
        """

        self.M = np.array(
            [[ -1,  -1, 1],   #Node 0
            [ -1,   1, 1],    #Node 1
            [1,   1, 1],      #Node 2
            [1,  -1, 1],      #Node 3
            [-1,  -1, -1],    #Node 4
            [-1,  1, -1],     #Node 5
            [1,   1, -1],     #Node 6
            [1,  -1, -1]], dtype=float).transpose() #Node 7

        self.con = [
            [0, 1, 2, 3], #Face 1
            [4, 5, 6, 7], #Face 2
            [3, 2, 6, 7], #Face 3
            [0, 1, 5, 4], #Face 4
            [0, 3, 7, 4], #Face 5
            [1, 2, 6, 5]] #Face 6

        faces = []

        for row in self.con:
            faces.append([self.M[:,row[0]],self.M[:,row[1]],self.M[:,row[2]],self.M[:,row[3]]])

        self.fig = plt.figure()
        ax = self.fig.add_subplot(111, projection='3d')

        for item in [self.fig, ax]:
            item.patch.set_visible(False)

        self.facesObj = Poly3DCollection(faces, linewidths=.2, edgecolors='k',animated = True)
        self.facesObj.set_facecolor([(0,0,1,0.9), #Blue
        (0,1,0,0.9), #Green
        (.9,.5,0.13,0.9), #Orange
        (1,0,0,0.9), #Red
        (1,1,0,0.9), #Yellow
        (0,0,0,0.9)]) #Black

        #Transfering information to the plot
        ax.add_collection3d(self.facesObj)

        #Configuring the plot aspect
        ax.azim=-90
        ax.roll = -90
        ax.elev=0   
        ax.set_xlim3d(-2, 2)
        ax.set_ylim3d(-2, 2)
        ax.set_zlim3d(-2, 2)
        ax.set_aspect('equal')
        ax.disable_mouse_rotation()
        ax.set_axis_off()

        self.pix2unit = 1.0/60 #ratio for drawing the cube 

    def update_cube(self):
        """
        Updates the cube vertices and updates the figure.
        Call this function after modifying the vertex matrix in self.M to redraw the cube
        """

        faces = []

        for row in self.con:
            faces.append([self.M[:,row[0]],self.M[:,row[1]],self.M[:,row[2]], self.M[:,row[3]]])

        self.facesObj.set_verts(faces)
        self.bm.update()

    def canvas_coordinates_to_figure_coordinates(self,x_can,y_can):
        """
        Remap canvas coordinates to cube centered coordinates
        """

        (canvas_width,canvas_height)=self.canvas.get_width_height()
        figure_center_x = canvas_width/2+14
        figure_center_y = canvas_height/2+2
        x_fig = (x_can-figure_center_x)*self.pix2unit
        y_fig = (y_can-figure_center_y)*self.pix2unit

        return(x_fig,y_fig)

    def destroy(self):
        """
        Close function to properly destroy the window and tk with figure
        """
        try:
            self.destroy()
        finally:
            exit()


class BlitManager:
    def __init__(self, canvas, animated_artists=()):
        """
        Parameters
        ----------
        canvas : FigureCanvasAgg
            The canvas to work with, this only works for sub-classes of the Agg
            canvas which have the `~FigureCanvasAgg.copy_from_bbox` and
            `~FigureCanvasAgg.restore_region` methods.

        animated_artists : Iterable[Artist]
            List of the artists to manage
        """
        self.canvas = canvas
        self._bg = None
        self._artists = []

        for a in animated_artists:
            self.add_artist(a)
        # grab the background on every draw
        self.cid = canvas.mpl_connect("draw_event", self.on_draw)

    def on_draw(self, event):
        """Callback to register with 'draw_event'."""
        cv = self.canvas
        if event is not None:
            if event.canvas != cv:
                raise RuntimeError
        self._bg = cv.copy_from_bbox(cv.figure.bbox)
        self._draw_animated()

    def add_artist(self, art):
        """
        Add an artist to be managed.

        Parameters
        ----------
        art : Artist

            The artist to be added.  Will be set to 'animated' (just
            to be safe).  *art* must be in the figure associated with
            the canvas this class is managing.

        """
        if art.figure != self.canvas.figure:
            raise RuntimeError
        art.set_animated(True)
        self._artists.append(art)

    def _draw_animated(self):
        """Draw all of the animated artists."""
        fig = self.canvas.figure
        for a in self._artists:
            fig.draw_artist(a)

    def update(self):
        """Update the screen with animated artists."""
        cv = self.canvas
        fig = cv.figure
        # paranoia in case we missed the draw event,
        if self._bg is None:
            self.on_draw(None)
        else:
            # restore the background
            cv.restore_region(self._bg)
            # draw all of the animated artists
            self._draw_animated()
            # update the GUI state
            cv.blit(fig.bbox)
        # let the GUI event loop process anything it has to do
            cv.draw_idle()


if __name__ == "__main__":
    app = Arcball()
    app.mainloop()
    exit()
