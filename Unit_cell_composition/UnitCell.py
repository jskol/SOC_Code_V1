import numpy as np


class Atom:
    def __init__(self,name:str ,orbitals: list ,position: list):
        self.name=name
        self.position=position
        self.orbitals=orbitals

    def print_details(self):
        print("Atom %s"%self.name)
        print("composed of orbitals:" ,self.orbitals)
        print("is located at ",self.position)


class UnitCell:
    def __init__(self,list_of_atoms):
        self.composition=[] # List allows for duplicates
        for atom in list_of_atoms:
            self.composition.append(atom)
    def add_atom(self, atom:Atom):
        self.composition.append(atom)

    def print_composition(self):
        for at in self.composition:
            at.print_details()

if __name__=="__main__":
    Indium1=Atom(name="In",orbitals=['s'],position=[2.1035000,-1.2144563,5.8756420])
    Indium2=Atom(name="In",orbitals=['s'],position=[2.1035000,1.2144563,14.8201420])
    Indium3=Atom(name="In",orbitals=['s'],position=[2.1035000,1.2144563,12.0133580])
    Indium4=Atom(name="In",orbitals=['s'],position=[2.1035000,-1.2144563,3.0688580])

    uc=UnitCell([Indium1,Indium2,Indium3,Indium4])
    uc.print_composition()


