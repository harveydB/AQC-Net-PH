from cProfile import label
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import copy
from model import AQC_NET
import argparse
import numpy as np
import conf_mat
import wandb

if __name__=='__main__':
    wandb.login
    wandb.init(project="my-test-project", entity="kaldra")
    wandb.config = {
      "learning_rate": 0.001,
      "epochs": 10,
      "batch_size": 5
    }

    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.RandomRotation((0,360)),
            transforms.RandomResizedCrop(size = (256,256), scale=(0.8,1)),
            transforms.Resize((256,256)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize((256,256)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('--train_folder', type=str, default = 'C:/Users/Kaldra/Documents/GitHub/EEE-199/Scripts/AQC_Net/train')
        parser.add_argument('--val_folder', type=str, default = 'C:/Users/Kaldra/Documents/GitHub/EEE-199/Scripts/AQC_Net/val')
        parser.add_argument('--num_label', type=str, default = 2 )
        parser.add_argument('--batch_size', type=str, default = 5 )
        return parser.parse_args()

    args = parse_args()
    image_datasets = {'train': datasets.ImageFolder(args.train_folder,data_transforms['train']),
                    'val': datasets.ImageFolder(args.val_folder,data_transforms['val'])
                    }
    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=args.batch_size,
                                                shuffle=True, num_workers=4)
                for x in ['train', 'val']}
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
    class_names = image_datasets['train'].classes

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    def train_model(model, criterion, optimizer, scheduler, num_epochs=50):
        since = time.time()

        best_model_wts = copy.deepcopy(model.state_dict())
        best_acc = 0.0

        for epoch in range(num_epochs):
            print('Epoch {}/{}'.format(epoch, num_epochs - 1))
            print('-' * 10)

            for phase in ['train', 'val']:
                if phase == 'train':
                    model.train()  
                else:
                    rec = True
                    model.eval()   

                running_loss = 0.0
                running_corrects = 0

                for inputs, labels in dataloaders[phase]:
                    inputs = inputs.to(device)
                    labels = labels.to(device)
                    
                    optimizer.zero_grad()

                    with torch.set_grad_enabled(phase == 'train'):
                        #print(inputs)
                        outputs = model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, labels)


                        if phase == 'train':
                            loss.backward()
                            optimizer.step()

                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)
                if phase == 'train':
                    scheduler.step()

                epoch_loss = running_loss / dataset_sizes[phase]
                if phase == 'train':
                    wandb.log({"train loss": epoch_loss})
                if phase == 'val':
                    wandb.log({"test loss": epoch_loss})
                epoch_acc = running_corrects.double() / dataset_sizes[phase]
                if phase == 'train':
                    wandb.log({"train accuracy": epoch_acc})
                if phase == 'val':
                    wandb.log({"test accuracy": epoch_acc})
                print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                    phase, epoch_loss, epoch_acc))
                if phase == 'val':
                    if epoch_acc >= best_acc:
                        best_acc = epoch_acc

            print()

        time_elapsed = time.time() - since
        print('Training complete in {:.0f}m {:.0f}s'.format(
            time_elapsed // 60, time_elapsed % 60))
        print('Best val Acc: {:4f}'.format(best_acc))



    model_ft = AQC_NET(pretrain=True, num_label= args.num_label)
    model_ft = model_ft.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer_ft = optim.Adam(model_ft.parameters(), lr=0.001)
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=3, gamma=0.1)
    train_model(model_ft, criterion, optimizer_ft, exp_lr_scheduler,
                        num_epochs=10)
    pred_np = np.array([9])
    actual_np = np.array([9])
    model_ft.eval()
    running_loss = 0.0
    running_corrects = 0
    phase = "val"

    
    wandb.watch(model_ft)

    for inputs, labels in dataloaders[phase]:
        inputs = inputs.to(device)
        labels = labels.to(device)
            
        with torch.no_grad():
            outputs = model_ft(inputs)
            _, preds = torch.max(outputs, 1)
            loss = criterion(outputs, labels)
            pred_np = np.concatenate((pred_np,preds.to("cpu").numpy()))
            actual_np = np.concatenate((actual_np,labels.to("cpu").numpy()))
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            

    epoch_loss = running_loss / dataset_sizes['val']
    epoch_acc = running_corrects.double() / dataset_sizes['val']
    print('{} Loss: {:.4f} Acc: {:.4f}'.format('val', epoch_loss, epoch_acc))
    np.savetxt("predict_res.txt",pred_np)
    np.savetxt("actual_res.txt",actual_np)
    conf_mat.create_conf_mat()

