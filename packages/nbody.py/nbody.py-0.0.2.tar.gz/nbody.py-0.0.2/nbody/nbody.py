import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML
import matplotlib.animation
from IPython.display import display, clear_output
from matplotlib.animation import FuncAnimation
from IPython.display import Video
from setuptools import find_packages, setup

def aceleracion( pos, mass, G, softening ):
    # positions r = [x,y,z] for all particles
    x = pos[:,0:1]
    y = pos[:,1:2]
    z = pos[:,2:3]


    dx = x.T - x
    dy = y.T - y
    dz = z.T - z

    inv_r3 = (dx**2 + dy**2 + dz**2 + softening**2)
    inv_r3[inv_r3>0] = inv_r3[inv_r3>0]**(-1.5)

    ax = G * (dx * inv_r3) @ mass
    ay = G * (dy * inv_r3) @ mass
    az = G * (dz * inv_r3) @ mass
    
    a = np.hstack((ax,ay,az))

    return a
def energia( pos, vel, mass, G ):
    
    E_K = 0.5 * np.sum(np.sum( mass * vel**2 ))

    x = pos[:,0:1]
    y = pos[:,1:2]
    z = pos[:,2:3]

    dx = x.T - x
    dy = y.T - y
    dz = z.T - z
    
    inv_r = np.sqrt(dx**2 + dy**2 + dz**2)
    inv_r[inv_r>0] = 1.0/inv_r[inv_r>0]


    E_P = G * np.sum(np.sum(np.triu(-(mass*mass.T)*inv_r,1)))
    return E_K,E_P

class Particula(object):
    def __init__(self,posicion,velocidad,masa,indice,suavizador,aceleracion=0):
        self.posicion = posicion
        self.x = posicion[:,0:1]
        self.y = posicion[:,1:2]
        self.z = posicion[:,2:3]
        self.velocidad = velocidad
        self.masa = masa
        self.indices = indice
        self.s = suavizador
        self.a = aceleracion
        E_K, E_P = energia(posicion,velocidad,masa,1)
        self.K = E_K
        self.V = E_P
        self.E = E_P + E_K
    def __str__(self):
        return f"---------------------\nParticula ID {self.indices}\n\nVelocidad:{self.velocidad}\nPosiciones: {self.posicion}\nMasa: {self.masa}\nAceleracion: {self.a}\nEnergia Cinetica: {self.K}\nEnergia Potencial: {self.V}\nEnergia Total: {self.E}\n---------------------\n"

class Sistema():
    def __init__(self,posiciones,velocidad,masa,indices=0,suavizador=0.1):
        if velocidad.shape[1]!=3 or posiciones.shape[1]!=3:
            raise Exception("La tupla debe ser un objeto (N,3)");
        else:
            if(indices==0):
                indices=np.linspace(1,posiciones.shape[0],posiciones.shape[0]);
            velocidad -= np.mean(masa * velocidad,0) / np.mean(masa)
            self.velocidad = velocidad
            self.posiciones=posiciones
            self.x = posiciones[:,0:1];
            self.y = posiciones[:,1:2];
            self.z = posiciones[:,2:3];
            E_K, E_P= energia(posiciones,velocidad,masa,1)
            self.K = [E_K]
            self.V = [E_P]
            self.E = []
            self.E.append(E_K + E_P)
            self.masa=masa
            self.indices=indices
            self.inx=0
            self.a = aceleracion(posiciones,masa,1,suavizador)
            self.s = suavizador
            self.t = [0]
            self.pos_historia = {}
            self.vel_historia = {}
            self.acel_historia = {}
            
    def simular(self,tf=int,dt=float,plot=False):
        """
        -----------------------------------------------
        Simula el sistema de n-cuerpo actualizando la aceleración,velocidad,posición,etc. de cada una
        de las partículas que lo componen, además de mostrar un gráfico característico del movimiento
        de estas.

        
        PARÁMETROS:
        
        -tf: Corresponde al tiempo durante el cual se simulará el sistema.
        
        -dt: Instante de tiempo en el cual el sistema se actualizará.
        
        -plot: Determina si se desea guardar la animación generada o no.
        
        simular(...) guarda todos los instantes de tiempo simulador en un atributo t y genera un 
        historia para la aceleración, velocidad y posición de los cuerpos en los atributos 
        acel_historial, vel_historial y pos_historial respectivamente.
        
        NOTA: Simular nuevamente el sistema reiniciará tanto el historial como los instantes de 
        tiempo guardados.
        
        ----------------------------------------------
        
        
        """
        self.t = [0]
        self.K = [self.K[-1]]
        self.E = [self.K[-1]]
        self.V = [self.K[-1]]
        KE_save = np.zeros(int(np.ceil(tf/dt))+1)
        KE_save[0] = self.K[0]
        PE_save = np.zeros(int(np.ceil(tf/dt))+1)
        PE_save[0] = self.V[0]
        pos_save = np.zeros((self.masa.shape[0],3,int(np.ceil(tf/dt))+1))
        if plot==True: 
            fig = plt.figure(figsize=(4,5), dpi=80)
            grid = plt.GridSpec(3, 1, wspace=0.0, hspace=0.3)
            ax1 = plt.subplot(grid[0:2,0])
            ax1.set(xlim=(-2, 2), ylim=(-2, 2))

            mx = max(list([np.amax(self.posiciones[:,0:1]),np.amax(self.posiciones[:,1:2])]))
            sc = plt.scatter(self.posiciones[:,0:1],self.posiciones[:,1:2],s=500*self.s/mx,color='blue')

            def actualizar(i):
                t=i*dt + dt
                ax1.set_aspect('equal', 'box')
                self.pos_historia[f'Tiempo {self.t[i]}'] = self.posiciones
                self.vel_historia[f'Tiempo {self.t[i]}'] = self.velocidad
                self.acel_historia[f'Tiempo {self.t[i]}'] = self.a
                self.t.append(t)
                pos_save[:,:,i] = self.posiciones
                self.velocidad = self.velocidad + (self.a * dt)/2.0
                self.posiciones = self.posiciones + self.velocidad*dt
                self.a = aceleracion(self.posiciones,self.masa,1,self.s)
                self.velocidad += (self.a * dt)/2
                self.x = self.posiciones[:,0:1];
                self.y = self.posiciones[:,1:2];
                self.z = self.posiciones[:,2:3];
                E_K, E_P = energia(self.posiciones,self.velocidad,self.masa,1)
                self.K.append(E_K)
                self.V.append(E_P)            
                self.E.append(E_K+E_P)
                xx = pos_save[:,0,max(i-50,0):i+1]
                yy = pos_save[:,1,max(i-50,0):i+1]
                sc.set_offsets(np.c_[self.posiciones[:,0:1],self.posiciones[:,1:2]])
            
                mx = max(list([np.amax(self.posiciones[:,0:1]),np.amax(self.posiciones[:,1:2])]))
                if mx > 10:
                    mx=10
                ax1.set_xticks([-mx,-mx/2,0,mx/2,mx])
                ax1.set_yticks([-mx,-mx/2,0,mx/2,mx])
                sc.set_sizes([500*self.s/mx])
                plt.title(f'Tiempo:{t}')
            ani = matplotlib.animation.FuncAnimation(fig, actualizar, interval=dt, frames=int(np.ceil(tf/dt)))
            ani.save('nbody.gif') 
        elif plot==False:
            for i in range(int(np.ceil(tf/dt))):
                self.pos_historia[f'Tiempo {self.t[i]}'] = self.posiciones
                self.vel_historia[f'Tiempo {self.t[i]}'] = self.velocidad
                self.acel_historia[f'Tiempo {self.t[i]}'] = self.a
                self.t.append(self.t[i]+dt)
                pos_save[:,:,i] = self.posiciones
                self.velocidad = self.velocidad + (self.a * dt)/2.0
                self.posiciones = self.posiciones + self.velocidad*dt
                self.a = aceleracion(self.posiciones,self.masa,1,self.s)
                self.velocidad += (self.a * dt)/2
                self.x = self.posiciones[:,0:1];
                self.y = self.posiciones[:,1:2];
                self.z = self.posiciones[:,2:3];
                E_K, E_P = energia(self.posiciones,self.velocidad,self.masa,1)
                self.K.append(E_K)
                self.V.append(E_P)
                KE_save[i+1] = self.K[i+1]
                PE_save[i+1] = self.V[i+1]               
                self.E[i+1]=KE_save[i+1]+PE_save[i+1]
    def __getitem__(self,item):
        res = ''
        if type(item)==int:
            res = Particula(np.reshape(self.posiciones[item],(1,3)),np.reshape(self.velocidad[item],(1,3)),np.reshape(self.masa[item],(1,1)),self.indices[item],self.s,self.a[item])
        elif type(item)==str:
            print(self.indices)
            for i,n in (enumerate(self.indices)):
                if item==n:
                    res = Particula(np.reshape(self.posiciones[i],(1,3)),np.reshape(self.velocidad[i],(1,3)),np.reshape(self.masa[i],(1,1)),self.indices[i],self.s,self.a[item])
        elif type(item)==slice:
            res = []
            n=item.start
            if n == None:
                n=0
            if n>item.stop:
                raise  Exception('El inicio debe ser menor o igual que el final.')
            while n < item.stop:
                n+=1
                res.append(Particula(np.reshape(self.posiciones[n],(1,3)),np.reshape(self.velocidad[n],(1,3)),np.reshape(self.masa[n],(1,1)),self.indices[n]),self.s,self.a[item])    
        return res
    def __next__(self):
        try:
            item = Particula(np.reshape(self.posiciones[self.inx],(1,3)),np.reshape(self.velocidad[self.inx],(1,3)),np.reshape(self.masa[self.inx],(1,1)),self.indices[self.inx],self.s,self.a[self.inx])
        except IndexError:
            raise StopIteration()
            self.inx=0
        self.inx+=1
        return item
    def __iter__(self):
        return self
    def plot(self):
        """
        ----------------------------------------------
        Genera un gráfico con las posiciones x e y que tienen las partículas del sistema actualmente.
        
        PARÁMETROS:
        
        NINGUNO
        
        ----------------------------------------------
        """
        if len(list(self.pos_historia.keys()))>0:           ##Se ha generado una simulación
            fig = plt.figure(figsize=(4,5), dpi=80)
            grid = plt.GridSpec(3, 1, wspace=0.0, hspace=0.3)
            ax1 = plt.subplot(grid[0:2,0])
            plt.sca(ax1)
            plt.cla()
            xx = self.pos_historia[list(self.pos_historia.keys())[-1]][:,0:1]
            yy = self.pos_historia[list(self.pos_historia.keys())[-1]][:,1:2]
            mx = max(list([np.amax(xx),np.amax(yy)]))
            if mx > 10:
                mx=10
            plt.scatter(xx,yy,500*self.s/mx,color='blue')
            ax1.set(xlim=(-2, 2), ylim=(-2, 2))
            ax1.set_aspect('equal', 'box')
            ax1.set_xticks([-mx,-mx/2,0,mx/2,mx])
            ax1.set_yticks([-mx,-mx/2,0,mx/2,mx])
            plt.title('Posiciones actuales')
            
        else:                                               ##Aún no hemos simulado nada
            fig = plt.figure(figsize=(4,5), dpi=80)
            grid = plt.GridSpec(3, 1, wspace=0.0, hspace=0.3)
            ax1 = plt.subplot(grid[0:2,0])
            plt.sca(ax1)
            plt.cla()
            xx = self.posiciones[:,0:1]
            yy = self.posiciones[:,1:2]
            mx = max(list([np.amax(xx),np.amax(yy)]))
            if mx > 10:
                mx=10
            plt.scatter(xx,yy,s=500*self.s/mx,color='blue')
            ax1.set(xlim=(-2, 2), ylim=(-2, 2))
            ax1.set_aspect('equal', 'box')
            ax1.set_xticks([-mx,-mx/2,0,mx/2,mx])
            ax1.set_yticks([-mx,-mx/2,0,mx/2,mx])
            plt.title('Posiciones actuales')
        return None
    
      