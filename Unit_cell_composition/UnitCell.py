import numpy as np


class Atom:
    def __init__(self,name:str ,orbitals: list ,position: list):
        self.name=name
        self.position=position
        self.orbitals=orbitals

    def print_details(self):
        print("Atom of %s"%self.name)
        print("composed of orbitals:" ,self.orbitals)
        print("is located at ",self.position)


class UnitCell:
    def __init__(self,list_of_atoms=[]):
        self.composition=[] # List allows for duplicates
        for atom in list_of_atoms:
            self.composition.append(atom)
    
    def __iter__(self):
        return iter(self.composition)

    def add_atom(self, atom:Atom):
        self.composition.append(atom)

    def print_composition(self):
        for at in self.composition:
            at.print_details()


    def plot_unit_cell(self):
        import matplotlib.pyplot as plt
        fig=plt.figure()
        ax=fig.add_subplot(projection='3d')
        # find unique names 
        diff_at_num= len(set([x.name for x in self.composition]))
        print("There is %i unique atoms"%diff_at_num)
        
        x_pos,y_pos,z_pos=[],[],[]
        colors=[]
        prev=self.composition[0].name
        col=0
        #print("starting to plot")
        for x in self.composition:
            x_pos.append(x.position[0])
            y_pos.append(x.position[1])
            z_pos.append(x.position[2])
            if x.name !=prev:
                 col +=1
            colors.append( (1.0*col)/diff_at_num)
            prev=x.name

        ax.scatter3D(x_pos,y_pos,z_pos,s=300,c=colors,cmap='Dark2')
        plt.show()

    def get_num_wann(self)->int:
        '''
        Returns number of wannier orbitals
        used in the projection
        '''
        num_wann=0
        for composition_iterator in self.composition:
            num_wann += len(composition_iterator.orbitals)
        return num_wann






if __name__=="__main__":
    Indium1=Atom(name="In",orbitals=['s'],position=[2.1035000,-1.2144563,5.8756420])
    Indium2=Atom(name="In",orbitals=['s'],position=[2.1035000,1.2144563,14.8201420])
    Indium3=Atom(name="In",orbitals=['s'],position=[2.1035000,1.2144563,12.0133580])
    Indium4=Atom(name="In",orbitals=['s'],position=[2.1035000,-1.2144563,3.0688580])

    uc=UnitCell([Indium1,Indium2,Indium3,Indium4])
    #uc.print_composition()
    #uc.plot_unit_cell()


    for el in uc:
        el.print_details()

