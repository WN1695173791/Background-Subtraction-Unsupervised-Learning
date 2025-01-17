import torch
from torch import nn
import torchvision.utils as vutils
import torchvision.models as models

import numpy as np

from AE_pretrained_models.model import *


from Param import *
from utils import weights_init


from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def frozen_params(module: nn.Module):
    for p in module.parameters():
        p.requires_grad = False


def fit(data, Encoder, Decoder, optimizer, criterion):

    img = data[0].to(device)
    
    encod_out = Encoder(img)
    output = Decoder(encod_out)

    loss = criterion(output, img)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    loss.detach_()

    return loss



def trainAE(dataloader, print_epoch=batch_size, verbose=True):

    
    if image_size_W == image_size_H:
        image_size = image_size_H


    pretrained_model = 'alexnet' # 'resnet50' #  
    if image_size == 512:
            Encoder_model = Encoder512(model=pretrained_model).to(device)
            Decoder_model = Decoder512().to(device)
    elif image_size == 256:
            Encoder_model = Encoder256(model=pretrained_model).to(device)
            Decoder_model = Decoder256().to(device)
    else:
        assert(0)
    

    if loss_ == True:
        criterion = nn.BCELoss()
    else:
        criterion = nn.MSELoss() 

    optimizer = torch.optim.Adam(list(Encoder_model.parameters())+ list(Decoder_model.parameters()), lr=lr)


    print("Starting Training Loop...")


    AE_losses = []
    img_list = []
    # For each epoch
    for epoch in range(num_epochs):
        torch.cuda.empty_cache()
        
        # For each batch in the dataloader
        for i, data in enumerate(dataloader, 0):
         
            if verbose: print(data[0].shape)
            if verbose: print(data[1].shape)

            #frozen_params(alexnet)
            recons_loss = fit(data, Encoder_model, Decoder_model, optimizer, criterion)

            # Output training stats
            if i % print_epoch == 0:
                print('[%d/%d][%d/%d]\tLoss_AE: %.4f'
                        % (epoch+1, num_epochs, i, len(dataloader), recons_loss.item()))

            # Save Losses for plotting later
            AE_losses.append(recons_loss.item())
            
            # Check how the generator is doing by saving G's output on fixed_noise
            if (i % 500 == 0) or ((epoch == num_epochs-1) and (i == len(dataloader)-1)):
                with torch.no_grad():
                    enc_out = Encoder_model(data[0].to(device))
                    img_out = Decoder_model(enc_out).detach().cpu()
                img_list.append(vutils.make_grid(img_out[0:10], nrow=5, normalize=True))
            

    return AE_losses, img_list, Encoder_model, Decoder_model




