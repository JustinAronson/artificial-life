from pyrosim.commonFunctions import Save_Whitespace

from matplotlib import colors

class MATERIAL: 

    def __init__(self, colorName = 'cyan'):

        self.depth  = 3

        self.string1 = '<material name="' + colorName + '">'

        if colorName == 'blue':
            self.string2 = '    <color rgba="0 0.0 1.0 1.0"/>'
        elif colorName == 'green':
            self.string2 = '    <color rgba="0 0.0 1.0 0.0"/>'
        else:
            self.string2 = '    <color rgba="0 1.0 1.0 1.0"/>'

        self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
