import numpy as np
from matplotlib import pyplot as plt
class Resistance2D:
    def __init__(self,lx,ly,nx,ny):
        self.lx = lx
        self.ly=ly
        self.nx=nx
        self.ny=ny 
    def assemble_connectivity(self):
        #nnodes = (self.nx+1)*(self.ny+1)
        location = np.zeros((self.nx+1,self.ny+1),dtype=object)
        for j in range(self.ny+1):
            for i in range(self.nx+1):
                location[i,j] = [i*(self.lx/self.nx), j*(self.ly/self.ny)]


        connectivity_map = []

        xstart = 1
        for j in range(self.ny+1):
            for i in range(xstart,xstart+ self.nx+1):
                if i == xstart+ self.nx and j == self.ny:
                    break
                elif i == xstart + self.nx:
                    connectivity_map.append((i,i+self.nx+1))
                elif j == self.ny:
                    connectivity_map.append((i,i+1))
                else:
                    connectivity_map.append((i,i+self.nx+1))
                    connectivity_map.append((i,i+1))
            xstart+=self.nx+1
        
        print('Connectivity Map: ',connectivity_map)    
    
        """
        x_coords = []
        y_coords = []
        labels = np.arange(1,((self.nx+1)*(self.ny+1))+1,1)

        for j in range(self.ny+1):
            for i in range(self.nx+1):
                x, y = location[i, j]
                x_coords.append(x)
                y_coords.append(y)

        # Plot the points
        

        # Label each point
        for x, y, label in zip(x_coords, y_coords, labels):
            plt.text(x+0.02, y+0.01, label, fontweight='bold',fontsize=8, ha='right', va='bottom')

        for j in range(self.ny+1):
            plt.plot([location[i, j][0] for i in range(self.nx+1)], [location[i, j][1] for i in range(self.nx+1)], 'k-')

        for i in range(self.nx+1):
            plt.plot([location[i, j][0] for j in range(self.ny+1)], [location[i, j][1] for j in range(self.ny+1)], 'k-')
        plt.scatter(x_coords, y_coords)
        plt.show()
        """
        self.visualize_network(location) 
        return connectivity_map
        
    def visualize_network(self,location):
        x_coords = []
        y_coords = []
        labels = np.arange(1,((self.nx+1)*(self.ny+1))+1,1)

        for j in range(self.ny+1):
            for i in range(self.nx+1):
                x, y = location[i, j]
                x_coords.append(x)
                y_coords.append(y)

        # Plot the points
        

        # Label each point
        for x, y, label in zip(x_coords, y_coords, labels):
            plt.text(x+0.02, y+0.01, label, fontweight='bold',fontsize=8, ha='right', va='bottom')

        for j in range(self.ny+1):
            plt.plot([location[i, j][0] for i in range(self.nx+1)], [location[i, j][1] for i in range(self.nx+1)], 'k-')

        for i in range(self.nx+1):
            plt.plot([location[i, j][0] for j in range(self.ny+1)], [location[i, j][1] for j in range(self.ny+1)], 'k-')
        plt.scatter(x_coords, y_coords)
        plt.show()    

#if __name__ == '__main__':

#rtest = Resistance2D(3,3,5,3)
#rtest.assemble_connectivity()

