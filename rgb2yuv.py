import numpy as np
from matplotlib import pyplot as plt

# rec.2020 color gamut
# conversion matrix reference: https://blog.csdn.net/helimin12345/article/details/78536520


#input is a RGB numpy array with shape (height,width,3), can be uint,int, float or double, values expected in the range 0..255
#output is a double YUV numpy array with shape (height,width,3), values in the range 0..255
def RGB2YUV( rgb, b=10 ):
    # scale yuv to 8 bit value range
    scale = pow(2.0,b-8)
    rgb/=scale
    
    m = np.array([[ 0.2256 , 0.5832 , 0.0509],
                  [-0.1227, 0.3166, 0.4392],
                  [ 0.4392, -0.4039 , -0.0353] ]).transpose
    
    yuv = np.dot(rgb,m)
    yuv[:,:,0]+=16
    yuv[:,:,1]+=128
    yuv[:,:,2]+=128
    
    yuv*=scale
    yuv = np.clip(yuv,0,pow(2,b)-1)
        
    return yuv 

#input is an YUV numpy array with shape (height,width,3) can be uint,int, float or double,  values expected in the range 0..255
#output is a double RGB numpy array with shape (height,width,3), values in the range 0..255
def YUV2RGB( yuv, b=10 ):  
    # scale yuv to 8 bit value range
    scale = pow(2.0,b-8)
    yuv/=scale  
    
    m = np.array([[ 1.1632, 0.0002,  1.6794],
                 [1.1632, -0.1870, -0.6497],
                 [ 1.1634 , 2.1421, 0.0008]]).transpose() 
     
    rgb = np.dot(yuv,m)
    rgb[:,:,0]-=233.6003
    rgb[:,:,1]+=88.4933
    rgb[:,:,2]-=292.9093
      
    rgb*=scale
    rgb = np.clip(rgb,0,pow(2,b)-1)
    
    return rgb


##############################
# set these params 
#############################
infile = 'data\\test_3840_2160_rgb44410le_2frames.rgb'
outfile = 'output.yuv'
w=3840
h=2160
b=10 # 10 bit
rgb = np.zeros([h,w,3])

with open(outfile, "wb") as f:
    chunk_size=h*w*3*2
    data = np.fromfile(infile, dtype='uint16',count=chunk_size,offset=chunk_size)
    fidx = 0
    while data.any():
        fidx=fidx+1
        print("frame %d" %(fidx))
        
        data = np.reshape(data,(w,h,3),'F')
    
        rgb[:,:,0] = np.transpose(data[:,:,0])
        rgb[:,:,1] = np.transpose(data[:,:,1])
        rgb[:,:,2] = np.transpose(data[:,:,2])
        
#         print(rgb.shape)
#         print(rgb)
#         plt.imshow(rgb/pow(2,10))
#         plt.show()
        
        yuv = YUV2RGB(rgb)
        
#         plt.imshow(yuv[:,:,0]/pow(2.0,b),cmap='gray')
#         plt.show()
        
        #save rgb
        yuv[:,:,0].astype('uint16').tofile(f)
        yuv[:,:,1].astype('uint16').tofile(f)
        yuv[:,:,2].astype('uint16').tofile(f)
    
        data = np.fromfile(infile, dtype='uint16',count=chunk_size,offset=chunk_size*fidx)

# # test the yuv file
# infile = 'output.yuv'
# chunk_size=h*w*3*2
# data = np.fromfile(infile, dtype='uint16',count=chunk_size,offset=chunk_size)
# fidx = 0
# while data.any():
#     fidx=fidx+1
#     print(fidx)
#        
#     data = np.reshape(data,(w,h,3),'F')
#    
#     yuv[:,:,0] = np.transpose(data[:,:,0])
#     yuv[:,:,1] = np.transpose(data[:,:,1])
#     yuv[:,:,2] = np.transpose(data[:,:,2])
#     
#     plt.imshow(yuv[:,:,0]/pow(2.0,b),cmap='gray')
#     plt.show()
#    
#     data = np.fromfile(infile, dtype='uint16',count=chunk_size,offset=chunk_size*fidx)