import numpy as np

class rgb_mask:
    def __init__(self,binA,color):
        self.binA = binA
        self.color = color
        self.binAsmooth = binA

    def plotform(self):
        return np.stack([self.binA*self.color[0],self.binA*self.color[1],self.binA*self.color[2],self.binA]).swapaxes(0,2).swapaxes(0,1)

    def add_mask(self, mask2):
        binA1u2 = ((self.binA+mask2.binA)>0.5).astype('uint8')
        return rgb_mask(binA1u2,self.color)
    
    def subtract_mask(self, mask2):
        binA1wo2 = ((self.binA-mask2.binA)>0.5).astype('uint8')
        return rgb_mask(binA1wo2,self.color)
    
    def intersect_mask(self,mask2):
        binA1a2 = self.binA*mask2.binA
        return rgb_mask(binA1a2,self.color)
    
    def plotform_combine_with(self, mask2, color_mixing='mean'):
        mask1wo2 = self.subtract_mask(mask2)
        mask2wo1 = mask2.subtract_mask(self)
        mask1a2  = self.intersect_mask(mask2)
        if color_mixing == 'mean':
            mask1a2.color = np.mean([self.color, mask2.color],axis=0)
        if color_mixing == 'max':
            mask1a2.color = np.amax([self.color, mask2.color],axis=0)
        if color_mixing == 'min':
            mask1a2.color = np.amin([self.color, mask2.color],axis=0)
        if color_mixing == 'orth':
            mask1a2.color = np.clip(np.cross(self.color, mask2.color),0,1)
            print(mask1a2.color)
        return mask1wo2.plotform()+mask2wo1.plotform()+mask1a2.plotform()
    
    def create_dilated_mask(self,kerneldiameter,iterations):
        dil_mask = rgb_mask(self.binA, self.color)
        
        #create smoothing kernel
        morphostruct = np.zeros((kerneldiameter,kerneldiameter))
        for k in range(kerneldiameter):
            for j in range(kerneldiameter):
                if np.sqrt((k-kerneldiameter/2)**2+(j-kerneldiameter/2)**2)<=kerneldiameter/2:
                    morphostruct[k,j]=1

        dil_mask.binA = binary_closing(self.binA,
                            structure=morphostruct,
                            iterations=iterations)
        return dil_mask
