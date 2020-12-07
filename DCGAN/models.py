""" models of Generators, Endoders and Discriminators at various image sizes
following deep convolutionnal model of DCGAN
cf https://pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html
and https://github.com/pytorch/examples/tree/master/dcgan

the final non linearity of the generator should be tanh ( positive and negative values, centered at zero) for GAN, but sigmoid for VAE,
where image pixel values are coded as probabilities between 0 and 1
"""


from __future__ import print_function
import torch
import torch.nn as nn
from torch.nn.utils import spectral_norm
from DCGAN.SN import SpectralNorm

from Param import nz, nc

class Generator64(nn.Module):

    def __init__(self,nz=nz,ngf=64,nc=nc):
        super(Generator64, self).__init__()
        self.nz=nz
        self.nc=nc
        self.main = nn.Sequential(
            # input is z, going into a convolution
            # input shape bachsize x nz
            nn.Conv2d(nz, ngf * 16, 1, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 16),
            nn.ReLU(True),
            nn.ConvTranspose2d(ngf * 16, ngf * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 8),
            nn.ReLU(True),
            # state size. (ngf*8) x 4 x 4
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),
            # state size. (ngf*4) x 8 x 8
            nn.ConvTranspose2d(ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),
            # state size. (ngf*2) x 16 x 16
            nn.ConvTranspose2d(ngf * 2, ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),
            # state size. (ngf) x 32 x 32
            nn.ConvTranspose2d(ngf, nc, 4, 2, 1, bias=False),
            nn.Tanh()
            #nn.Sigmoid() for VAE
            # state size. (nc) x 64 x 64
        )

    def forward(self, input):
        output = self.main(input.reshape(-1, self.nz, 1, 1))
        return output



class Generator128(nn.Module):
    def __init__(self,nz=nz,ngf=32,nc=nc):
        super(Generator128, self).__init__()
        self.nz = nz
        self.nc = nc
        self.main = nn.Sequential(
            nn.ConvTranspose2d(nz, ngf *32 , 2, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 32),
            nn.ReLU(True),
            # size ngf*32 x2 x2
            nn.ConvTranspose2d(ngf*32, ngf * 16, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 16),
            nn.ReLU(True),
            # size ngf*16 x4 x4
            nn.ConvTranspose2d(ngf * 16, ngf * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 8),
            nn.ReLU(True),
            # state size. (ngf*8) x 8 x 8
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),
            # state size. (ngf*4) x 16 x16
            nn.ConvTranspose2d(ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),
            # state size. (ngf*2) x 32 x 32
            nn.ConvTranspose2d(ngf * 2, ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),
            # state size. (ngf) x 64 x 64
            nn.ConvTranspose2d(ngf, nc, 4, 2, 1, bias=False),
            nn.Tanh()
            # nn.Sigmoid() for VAE
            # state size. (nc) x 128 x 128
        )

    def forward(self, input):
        output = self.main(input.reshape(-1, self.nz, 1, 1))
        return output


class Generator256(nn.Module):
    def __init__(self,nz=nz,ngf=16,nc=nc):
        super(Generator256, self).__init__()
        self.nz=nz
        self.nc=nc
        self.main = nn.Sequential(
            nn.ConvTranspose2d(nz, ngf *64 , 2, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 64),
            nn.ReLU(True),
            # size ngf*64 x2 x2
            nn.ConvTranspose2d(ngf * 64, ngf * 32, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 32),
            nn.ReLU(True),
            # size ngf*32 x4 x4
            nn.ConvTranspose2d(ngf*32, ngf * 16, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 16),
            nn.ReLU(True),
            # state size. (ngf*8) x 8 x 8
            nn.ConvTranspose2d(ngf * 16, ngf * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 8),
            nn.ReLU(True),
            # state size. (ngf*4) x 16 x16
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),
            # state size. (ngf*2) x 32 x 32
            nn.ConvTranspose2d(ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),
            # state size. (ngf) x 64 x 64
            nn.ConvTranspose2d(ngf * 2, ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),
            # state size. (nc) x 128 x 128
            nn.ConvTranspose2d(ngf, nc, 4, 2, 1, bias=False),
            nn.Tanh()
            # nn.Sigmoid() for VAE
            # state size. (nc) x 256 x 256

        )

    def forward(self, input):
        output = self.main(input.reshape(-1, self.nz, 1, 1))
        return output



class Generator512(nn.Module):
    def __init__(self,nz=nz,ngf=8,nc=nc):
        super(Generator512, self).__init__()
        self.nz=nz
        self.nc=nc
        self.main = nn.Sequential(
            nn.ConvTranspose2d(nz, ngf *128 , 2, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 128),
            nn.ReLU(True),
            # size ngf*128 x2 x2
            nn.ConvTranspose2d(ngf * 128, ngf * 64, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 64),
            nn.ReLU(True),
            # size ngf*64 x4 x4
            nn.ConvTranspose2d(ngf * 64, ngf * 32, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 32),
            nn.ReLU(True),
            # size ngf*32 x8 x8
            nn.ConvTranspose2d(ngf*32, ngf * 16, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 16),
            nn.ReLU(True),
            # state size. (ngf*16) x 16 x16
            nn.ConvTranspose2d(ngf * 16, ngf * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 8),
            nn.ReLU(True),
            # state size. (ngf*8) x 32 x 32
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),
            # state size. (ngf*4) x 64 x 64
            nn.ConvTranspose2d(ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),
            # state size. (ngf*2) x 128 x 128
            nn.ConvTranspose2d(ngf * 2, ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),
            # state size. (ngf) x 256 x 256
            nn.ConvTranspose2d(ngf, nc, 4, 2, 1, bias=False),
            nn.Tanh()
            #nn.Sigmoid() for VAE
            # state size. (nc) x 256 x 256

        )

    def forward(self, input):
        output = self.main(input.reshape(-1, self.nz, 1, 1))
        return output





class Discriminator64(nn.Module):
    def __init__(self,nef=64,nc=nc):
        super(Discriminator64, self).__init__()
        self.nef=nef
        self.main = nn.Sequential(
            # input is (nc) x 64 x 64
            nn.Conv2d(nc, nef, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef) x 32 x 32
            nn.Conv2d(nef, nef * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 2),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef*2) x 16 x 16
            nn.Conv2d(nef * 2, nef * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 4),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef*4) x 8 x 8
            nn.Conv2d(nef * 4, nef * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 8),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef*8) x 4 x 4
            nn.Conv2d(nef * 8, nef * 16, 4, 1, 0, bias=False),
            nn.Conv2d(nef * 16, 1, 1, 1, 0, bias=True),
            nn.Sigmoid()
        )

    def forward(self, input):
        output = self.main(input)
        return output.reshape(-1, 1)



class Discriminator128(nn.Module):
    def __init__(self,nef=32,nc=nc):
        super(Discriminator128, self).__init__()
        self.nc=nc
        self.main = nn.Sequential(
            # input is (nc) x 128 x 128
            nn.Conv2d(nc, nef, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef) x 64 x 64
            nn.Conv2d(nef, nef * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 2),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef) x 32 x 32
            nn.Conv2d(nef*2, nef * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 4),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef*2) x 16 x 16
            nn.Conv2d(nef * 4, nef * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 8),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef*4) x 8 x 8
            nn.Conv2d(nef * 8, nef * 16, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 16),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef*8) x 4 x 4
            nn.Conv2d(nef * 16, nef * 32, 4, 1, 0, bias=False),
            nn.BatchNorm2d(nef * 32),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(nef * 32, 1, 1, 1, 0, bias=True),
            nn.Sigmoid()
        )

    def forward(self, input):
        output = self.main(input)
        return output.reshape(-1, 1)


class Discriminator256(nn.Module):
    def __init__(self,nef=16,nc=nc):
        super(Discriminator256, self).__init__()
        self.nc=nc
        self.main = nn.Sequential(
            # input is (nc) x 258 x 256
            nn.Conv2d(nc, nef, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef) x 128 x 128
            nn.Conv2d(nef, nef * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 2),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef) x 64 x 64
            nn.Conv2d(nef * 2, nef * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 4),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef) x 32 x 32
            nn.Conv2d(nef*4, nef * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 8),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef*2) x 16 x 16
            nn.Conv2d(nef * 8, nef * 16, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 16),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef*4) x 8 x 8
            nn.Conv2d(nef * 16, nef * 32, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 32),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef*8) x 4 x 4
            nn.Conv2d(nef * 32, nef * 64, 4, 1, 0, bias=False),
            nn.BatchNorm2d(nef * 64),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(nef * 64, 1, 1, 1, 0, bias=True),
            nn.Sigmoid()
        )

    def forward(self, input):
        output = self.main(input)
        return output.reshape(-1, 1)




class Discriminator512(nn.Module):
    def __init__(self,nef=8,nc=nc):
        super(Discriminator512, self).__init__()
        self.nc=nc
        self.main = nn.Sequential(
            # input is (nc) x 512 x 512
            nn.Conv2d(nc, nef, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef),
            nn.LeakyReLU(0.2, inplace=True),
            # state size is (nef) x 256 x 256
            nn.Conv2d(nef, nef * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 2),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef*2) x 128 x 128
            nn.Conv2d(nef*2, nef * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 4),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef*4) x 64 x 64
            nn.Conv2d(nef * 4, nef * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 8),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef*8) x 32 x 32
            nn.Conv2d(nef*8, nef * 16, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 16),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef*2) x 16 x 16
            nn.Conv2d(nef * 16, nef * 32, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 32),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef*32) x 8 x 8
            nn.Conv2d(nef * 32, nef * 64, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 64),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef*64) x 4 x 4
            nn.Conv2d(nef * 64, nef * 128, 4, 1, 0, bias=False),
            nn.BatchNorm2d(nef * 128),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(nef * 128, 1, 1, 1, 0, bias=True),
            nn.Sigmoid()
        )

    def forward(self, input):
        output = self.main(input)
        return output.reshape(-1, 1)


# Discriminator based on U-net architecture
class netD512(nn.Module):

    def __init__(self, nef=16, nc=nc):
        super(netD512, self).__init__()
        self.nc = nc

        # 3*512*512
        self.down1 = nn.Sequential(
            nn.Conv2d(self.nc, nef, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef, nef, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef),
            nn.ReLU(inplace=True))
        self.down1_pool = nn.Sequential(nn.MaxPool2d(kernel_size=2, stride=2))

        # 16*256*256
        self.down2 = nn.Sequential(
            nn.Conv2d(nef, nef*2, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*2),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef*2, nef*2, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*2),
            nn.ReLU(inplace=True),)
        self.down2_pool = nn.Sequential(nn.MaxPool2d(kernel_size=2, stride=2))

        # 32*128*128
        self.down3 = nn.Sequential(
            nn.Conv2d(nef*2, nef*4, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*4),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef*4, nef*4, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*4),
            nn.ReLU(inplace=True),)
        self.down3_pool = nn.Sequential(nn.MaxPool2d(kernel_size=2, stride=2))

        # 64*64*64
        self.down4 = nn.Sequential(
            nn.Conv2d(nef*4, nef*8, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*8),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef*8, nef*8, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*8),
            nn.ReLU(inplace=True))
        self.down4_pool = nn.Sequential(nn.MaxPool2d(kernel_size=2, stride=2))

        # 128*32*32
        self.down5 = nn.Sequential(
            nn.Conv2d(nef*8, nef*16, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*16),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef*16, nef*16, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*16),
            nn.ReLU(inplace=True))
        self.down5_pool = nn.Sequential(nn.MaxPool2d(kernel_size=2, stride=2))

        # 256*16*16
        self.down6 = nn.Sequential(
            nn.Conv2d(nef*16, nef*32, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*32),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef*32, nef*32, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*32),
            nn.ReLU(inplace=True))
        self.down6_pool = nn.Sequential(nn.MaxPool2d(kernel_size=2, stride=2))

        # 512*8*8
        self.center = nn.Sequential(
            nn.Conv2d(nef*32, nef*64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*64),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef*64, nef*64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*64),
            nn.ReLU(inplace=True),)

        # 1024*8*8
        self.upsample6 = nn.Sequential(nn.Upsample(scale_factor=2, mode='bilinear'))
        self.up6 = nn.Sequential(
            nn.Conv2d(nef*64+nef*32, nef*32, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*32),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef*32, nef*32, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*32),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef*32, nef*32, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*32),
            nn.ReLU(inplace=True),)

        # 512*16*16
        self.upsample5 = nn.Sequential(nn.Upsample(scale_factor=2, mode='bilinear'))
        self.up5 = nn.Sequential(
            nn.Conv2d(nef*32+nef*16, nef*16, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*16),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef*16, nef*16, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*16),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef*16, nef*16, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*16),
            nn.ReLU(inplace=True),)

        # 256*32*32
        self.upsample4 = nn.Sequential(nn.Upsample(scale_factor=2, mode='bilinear'))
        self.up4 = nn.Sequential(
            nn.Conv2d(nef*16+nef*8, nef*8, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*8),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef*8, nef*8, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*8),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef*8, nef*8, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*8),
            nn.ReLU(inplace=True),)

        # 128*64*64
        self.upsample3 = nn.Sequential(nn.Upsample(scale_factor=2, mode='bilinear'))
        self.up3 = nn.Sequential(
            nn.Conv2d(nef*8+nef*4, nef*4, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*4),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef*4, nef*4, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*4),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef*4, nef*4, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*4),
            nn.ReLU(inplace=True),
            )

        # 64*128*128
        self.upsample2 = nn.Sequential(nn.Upsample(scale_factor=2, mode='bilinear'))
        self.up2 = nn.Sequential(
            nn.Conv2d(nef*4+nef*2, nef*2, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*2),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef*2, nef*2, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*2),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef*2, nef*2, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef*2),
            nn.ReLU(inplace=True),
            )

        # 32*256*256
        self.upsample1 = nn.Sequential(nn.Upsample(scale_factor=2, mode='bilinear'))
        self.up1 = nn.Sequential(
            nn.Conv2d(nef*2+nef, nef, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef, nef, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef),
            nn.ReLU(inplace=True),
            nn.Conv2d(nef, nef, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(nef),
            nn.ReLU(inplace=True),
            )
        # 16*512*512
        self.classifier = nn.Sequential(
                nn.Conv2d(nef, self.nc, kernel_size=3, stride=1, padding=1),
                nn.Sigmoid(),
            )
    # 3*512*512

            # state size. (nef*32) x 8 x 8
        self.out = nn.Sequential(
            nn.Conv2d(nef * 32, nef * 64, 4, 2, 1, bias=False),
            nn.BatchNorm2d(nef * 64),
            nn.LeakyReLU(0.2, inplace=True),
            # state size. (nef*64) x 4 x 4
            nn.Conv2d(nef * 64, nef * 128, 4, 1, 0, bias=False),
            nn.BatchNorm2d(nef * 128),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(nef * 128, 1, 1, 1, 0, bias=True),
            nn.Sigmoid())


    def forward(self, img):
        # 3*512*512
        down1 = self.down1(img)
        down1_pool = self.down1_pool(down1)

        # 16*256*256
        down2 = self.down2(down1_pool)
        down2_pool = self.down2_pool(down2)

        # 32*128*128
        down3 = self.down3(down2_pool)
        down3_pool = self.down3_pool(down3)

        # 64*64*64
        down4 = self.down4(down3_pool)
        down4_pool = self.down4_pool(down4)

        # 128*32*32
        down5 = self.down5(down4_pool)
        down5_pool = self.down5_pool(down5)

        # 256*16*16
        down6 = self.down6(down5_pool)
        down6_pool = self.down6_pool(down6)

        # 512*8*8
        center = self.center(down6_pool)
        # 1024*8*8

        up6 = self.upsample6(center)
        # 1024*16*16

        up6 = torch.cat((down6,up6), 1)
        up6 = self.up6(up6)

        # 512*16*16
        up5 = self.upsample5(up6)
        up5 = torch.cat((down5,up5), 1)
        up5 = self.up5(up5)

        # 256*32*32
        up4 = self.upsample4(up5)
        up4 = torch.cat((down4,up4), 1)
        up4 = self.up4(up4)

        # 128*64*64
        up3 = self.upsample3(up4)
        up3 = torch.cat((down3,up3), 1)
        up3 = self.up3(up3)

        # 64*128*128
        up2 = self.upsample2(up3)
        up2 = torch.cat((down2,up2), 1)
        up2 = self.up2(up2)

        # 32*256*256
        up1 = self.upsample1(up2)
        up1 = torch.cat((down1,up1), 1)
        up1 = self.up1(up1)

        # 16*512*512
        prob = self.classifier(up1)
        # 3*512*512

        out = self.out(down6_pool)
        #return prob
        return out



class Discriminator512_SN(nn.Module):
    def __init__(self,nef=8,nc=nc):
        super(Discriminator512_SN, self).__init__()
        self.nc=nc

        nf = [nc, nef, nef*2, nef*4, nef*8, nef*16, nef*32, nef*64]
        self.num_layers = len(nf)-1
        layers_list = []
        for i in range(self.num_layers):
            layers_list.append(SpectralNorm(nn.Conv2d(nf[i], nf[i+1], 4, 2, 1, bias=False)))
        self.con_layers = nn.ModuleList(layers_list)

        self.conv = SpectralNorm(nn.Conv2d(nef * 64, nef * 128, 4, 1, 0, bias=False))
        self.classifier = nn.Conv2d(nef * 128, 1, 1, 1, 0, bias=True)
        self.output = nn.Sigmoid()
           
        self.activation = nn.LeakyReLU(0.2, inplace=True)


    def forward(self, input):
        x = input
        for i in range(self.num_layers):
            x = self.con_layers[i](x)
            x = self.activation(x)

        x = self.conv(x)
        x = self.activation(x)

        output = self.output(self.classifier(x))
        return output.reshape(-1, 1)

