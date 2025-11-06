import unittest


from read_DOS import read_DOS

class TestCases(unittest.TestCase):
    def test_wrong_col(self):
        with self.assertRaises(RuntimeError):
            E1,D1=read_DOS("dos.dat",0)
    
    def test_col_out_of_range(self):
        with self.assertRaises(RuntimeError):
            E1,D1=read_DOS("dos.dat", 110)


    def test_file_doesnt_exist(self):
        with self.assertRaises(FileNotFoundError):
            E1,E2=read_DOS("foo.dat",1)

    def test_compare_sets(self):
        E1,D1=read_DOS("dos.dat", 1)
        E2,D2=read_DOS("dos.dat", 2)
        self.assertTrue((E1==E2).all()) # Check if energies are the same
        self.assertFalse((D1 == D2).all()) # Check if some DOS's are different
        
if __name__=="__main__":
    unittest.main()