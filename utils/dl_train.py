## author: xin luo 
# creat: 2022.9.26
# des: script for model training 

import torch

def train_model(model, train_dloader, optimizer, loss_fun, epochs, val_dloader=None, vis_step=10):
    '''
    train the built cnn model
    '''
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        count_tra = count_val = 0
        correct_tra = correct_val = 0
        # train
        for data_tra in train_dloader:
            x_tra, y_tra = data_tra
            optimizer.zero_grad()
            ## forward + backward + optimize
            pred_tra = model(x_tra)
            loss = loss_fun(pred_tra, y_tra)
            loss.backward()
            optimizer.step()
            ## print statistics
            running_loss += loss.item()
            # accuracy
            _, pred_tra = torch.max(pred_tra, 1)
            count_tra += y_tra.size(0)
            correct_tra += (pred_tra == y_tra).sum().item()
        acc_tra = correct_tra/count_tra
        # validation
        if epoch % vis_step == 0:
            if val_dloader != None:
                model.eval()
                for data_val in val_dloader:
                    x_val, y_val = data_val
                    pred_val = model(x_val)
                    _, pred_val = torch.max(pred_val, 1)
                    count_val += y_val.size(0)
                    correct_val += (pred_val == y_val).sum().item()
                acc_val = correct_val/count_val
                print('epoch: %d, loss_sum: %.6f, acc_tra: %.4f, acc_val: %.4f' % (epoch+1, running_loss, acc_tra ,acc_val))
            else:
                print('epoch: %d, loss_sum: %.6f, acc_tra: %.4f' % (epoch+1, running_loss, acc_tra))




