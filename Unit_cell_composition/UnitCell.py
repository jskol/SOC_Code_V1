import numpy as np

class Atom:
    '''
    An object that has a 
    1) name (str)
    2) position(list)
    3) orbitals used in the projection step (list)
    '''
    def __init__(self,name:str ,orbitals: list ,position: list):
        self.name=name
        self.position=position
        self.orbitals=orbitals

    def print_details(self):
        print("Atom of %s"%self.name)
        print("located at ",self.position)
        print("composed of orbitals:" ,self.orbitals)
        print("List of orbitals split by L:\n", self.split_orbitals_by_L())

    def split_orbitals_by_L(self)-> list:
        '''
        Splits a list of various orbitals into
        lists containing different L-value
        '''
        res = []
        prev_letter=self.orbitals[0][0]
        temp_list=[]
        for orb in self.orbitals:
            curr_letter=orb[0]
            if curr_letter == prev_letter:
                temp_list.append(orb)
            else:
                res.append(temp_list)
                temp_list=[orb]

            prev_letter=curr_letter 
        # Always ends with a non-empty temp_list,
        #  so flush the final list
        res.append(temp_list) 
        return res

def get_L_from_orbitals_set_name(orb_list:list)-> int:
    first_letter=orb_list[0][0]
    if (first_letter == 's'):
        l = 0
    elif (first_letter == 'p'):
        l = 1
    elif (first_letter == 'd'):
        l = 2
    else:
        raise Exception("Orbital unavailable!")
    return l

class UnitCell:
    '''
    An object containing set of Atoms
    '''
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