import torch.nn as nn
import torch.nn.functional as F
from torchsummary import summary

class cnn_1d(nn.Module):
    def __init__(self):
        super(cnn_1d, self).__init__()
        # input data channel:1, output channels:6, convolution: 6
        self.conv1 = nn.Conv1d(1, 16, 6, stride=2, padding=0)
        self.bn1 = nn.BatchNorm1d(16)
        self.conv2 = nn.Conv1d(16, 32, 6, stride=2, padding=0)
        self.bn2 = nn.BatchNorm1d(32)
        self.conv3 = nn.Conv1d(32, 64, 4, stride=2, padding=0)
        self.bn3 = nn.BatchNorm1d(64)
        self.conv4 = nn.Conv1d(64, 128, 4, stride=3, padding=0)
        self.bn4 = nn.BatchNorm1d(128)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(128*4, 120)  #
        self.bn5 = nn.BatchNorm1d(120)
        self.fc2 = nn.Linear(120, 2)

    def forward(self, x):
        # x = F.dropout(F.relu(self.conv1(x)),p=0.2)
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.dropout(x, p=0.2)
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.dropout(x, p=0.2)
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.dropout(x, p=0.2)
        x = F.relu(self.bn4(self.conv4(x)))
        x = F.dropout(x, p=0.2)
        x = x.view(-1, 128 * 4)
        x = F.relu(self.bn5(self.fc1(x)))
        x = F.dropout(x, p=0.2)
        x = self.fc2(x)
        return x


class cnn_1d_improve(nn.Module):
    def __init__(self):
        super(cnn_1d_improve, self).__init__()
        # input data channel:1, output channels:6, convolution: 6
        self.conv11 = nn.Conv1d(1, 16, 3, stride=1, padding=1)
        self.bn11 = nn.BatchNorm1d(16)
        self.conv12 = nn.Conv1d(16, 16, 3, stride=1, padding=1)
        self.bn12 = nn.BatchNorm1d(16)
        self.conv21 = nn.Conv1d(16, 32, 3, stride=1, padding=1)
        self.bn21 = nn.BatchNorm1d(32)
        self.conv22 = nn.Conv1d(32, 32, 3, stride=1, padding=1)
        self.bn22 = nn.BatchNorm1d(32)
        self.conv31 = nn.Conv1d(32, 64, 3, stride=1, padding=1)
        self.bn31 = nn.BatchNorm1d(64)
        self.conv32 = nn.Conv1d(64, 64, 3, stride=1, padding=1)
        self.bn32 = nn.BatchNorm1d(64)
        self.conv41 = nn.Conv1d(64, 128, 3, stride=1, padding=1)
        self.bn41 = nn.BatchNorm1d(128)
        self.conv42 = nn.Conv1d(128, 128, 3, stride=1, padding=1)
        self.bn42 = nn.BatchNorm1d(128)
        self.conv51 = nn.Conv1d(128, 128, 3, stride=1, padding=1)
        self.bn51 = nn.BatchNorm1d(128)
        self.conv52 = nn.Conv1d(128, 128, 3, stride=1, padding=1)
        self.bn52 = nn.BatchNorm1d(128)
        self.conv61 = nn.Conv1d(128, 128, 3, stride=1, padding=1)
        self.bn61 = nn.BatchNorm1d(128)
        self.conv62 = nn.Conv1d(128, 128, 3, stride=1, padding=1)
        self.bn62 = nn.BatchNorm1d(128)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(128*4, 128)  #
        self.bn7 = nn.BatchNorm1d(128)
        self.fc2 = nn.Linear(128, 2)

    def forward(self, x):
        x = F.relu(self.bn11(self.conv11(x)))
        x_1 = self.bn12(self.conv12(x))
        x_1 = F.relu(x_1+x)
        x_1 = F.avg_pool1d(x_1, kernel_size=2, stride=2) # 64
        x_1 = F.relu(self.bn21(self.conv21(x_1)))
        x_2 = self.bn22(self.conv22(x_1))
        x_2 = F.relu(x_2+x_1)
        x_2 = F.avg_pool1d(x_2, kernel_size=2, stride=2) # 32
        x_2 = F.relu(self.bn31(self.conv31(x_2)))
        x_3 = self.bn32(self.conv32(x_2))
        x_3 = F.relu(x_3+x_2)
        x_3 = F.avg_pool1d(x_3, kernel_size=2, stride=2) # 32
        x_3 = F.relu(self.bn41(self.conv41(x_3)))
        x_4 = self.bn42(self.conv42(x_3))
        x_4 = F.relu(x_4+x_3)
        x_4 = F.avg_pool1d(x_4, kernel_size=2, stride=2) # 16
        x_4 = F.relu(self.bn51(self.conv51(x_4)))
        x_5 = self.bn52(self.conv52(x_4))
        x_5 = F.relu(x_5+x_4)
        x_5 = F.avg_pool1d(x_5, kernel_size=2, stride=2) # 8
        x_5 = F.relu(self.bn61(self.conv61(x_5)))
        x_6 = self.bn62(self.conv62(x_5))
        x_6 = F.relu(x_6+x_5)
        x_fc = x_6.view(-1, 128 * 4)
        x_fc = F.relu(self.bn7(self.fc1(x_fc)))
        x_fc = self.fc2(x_fc)
        return x_fc


class nn_net(nn.Module):
    def __init__(self):
        super(nn_net, self).__init__()
        self.nn1 = nn.Linear(128, 256)
        self.bn1 = nn.BatchNorm1d(256)
        self.nn2 = nn.Linear(256, 256)
        self.bn2 = nn.BatchNorm1d(256)
        self.nn3 = nn.Linear(256, 256)
        self.bn3 = nn.BatchNorm1d(256)
        self.nn4 = nn.Linear(256, 128)  #
        self.bn4 = nn.BatchNorm1d(128)
        self.nn5 = nn.Linear(128, 2)

    def forward(self, x):  
        x = x.view(-1, 128)
        x = F.relu(self.bn1(self.nn1(x)))
        x = F.relu(self.bn2(self.nn2(x)))
        x = F.relu(self.bn3(self.nn3(x)))
        x = F.relu(self.bn4(self.nn4(x)))
        x = self.nn5(x)
        return x

# model = cnn_1d()
# model = cnn_1d_improve()
# model = nn_net()
# model.eval()
# summary(model,(1,128))


