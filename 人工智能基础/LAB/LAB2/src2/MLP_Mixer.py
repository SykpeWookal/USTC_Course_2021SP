import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.datasets import MNIST
#禁止import除了torch以外的其他包，依赖这几个包已经可以完成实验了

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class Mixer_Layer(nn.Module):
    def __init__(self, patch_size, hidden_dim):
        super(Mixer_Layer, self).__init__()
        ########################################################################
        #这里需要写Mixer_Layer（layernorm，mlp1，mlp2，skip_connection）
        patchesN = pow((28 // patch_size) , 2)#patches数目
        tokensN = 512 #隐层个数
        channelsN = 4096 #channel个数
        #print("patchesN:", patchesN)
        #以下实现示例图中的MixerLayer
        self.tokenInput = nn.LayerNorm(hidden_dim)
        self.tokenMixer = nn.Sequential(nn.Linear(patchesN, tokensN), nn.GELU(), nn.Linear(tokensN, patchesN))
        self.channelInput = nn.LayerNorm(hidden_dim)
        self.channelMixer = nn.Sequential(nn.Linear(hidden_dim, channelsN), nn.GELU(), nn.Linear(channelsN, hidden_dim))
        ########################################################################

    def forward(self, x):
        ########################################################################
        # print(x.shape)
        out = self.tokenInput(x).transpose(1, 2)
        x = x + self.tokenMixer(out).transpose(1, 2)#skip-connections
        out = self.channelInput(x)
        x = x + self.channelMixer(out)
        return x
        ########################################################################


class MLPMixer(nn.Module):
    def __init__(self, patch_size, hidden_dim, depth):
        super(MLPMixer, self).__init__()
        assert 28 % patch_size == 0, 'image_size must be divisible by patch_size'
        assert depth > 1, 'depth must be larger than 1'
        ########################################################################
        #这里写Pre-patch Fully-connected, Global average pooling, fully connected
        self.patchesN = pow((28 // patch_size), 2)
        self.patch_emb = nn.Conv2d(1, hidden_dim, kernel_size=patch_size, stride=patch_size, bias=False)
        self.mixerBlocks = nn.ModuleList([])
        for _ in range(depth):
            self.mixerBlocks.append(Mixer_Layer(patch_size, hidden_dim))
        self.In = nn.LayerNorm(hidden_dim)
        self.mlp_head = nn.Sequential(nn.Linear(hidden_dim, 123))
        ########################################################################


    def forward(self, data):
        ########################################################################
        #注意维度的变化
        result = self.patch_emb(data)
        result = result.flatten(2).transpose(1, 2)
        for mixer_block in self.mixerBlocks:
            result = mixer_block(result)
        result = self.In(result)
        result = result.mean(dim=1)
        result = self.mlp_head(result)
        return result
        ########################################################################


def train(model, train_loader, optimizer, n_epochs, criterion):
    model.train()
    for epoch in range(n_epochs):
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            ########################################################################
            #计算loss并进行优化
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            ########################################################################
            if batch_idx % 100 == 0:
                print('Train Epoch: {}/{} [{}/{}]\tLoss: {:.6f}'.format(
                    epoch, n_epochs, batch_idx * len(data), len(train_loader.dataset), loss.item()))


def test(model, test_loader, criterion):
    model.eval()
    test_loss = 0.
    num_correct = 0 #correct的个数
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
        ########################################################################
        #需要计算测试集的loss和accuracy
            output = model(data)
            test_loss = test_loss + criterion(output, target)
            pred = output.data.max(1, keepdim=True)[1]
            num_correct = num_correct + pred.eq(target.data.view_as(pred)).cpu().sum()
        test_loss = test_loss / len(test_loader.dataset)
        accuracy = num_correct / len(test_loader.dataset)
        ########################################################################
        print("Test set: Average loss: {:.4f}\t Acc {:.2f}".format(test_loss.item(), accuracy))




if __name__ == '__main__':
    n_epochs = 5
    batch_size = 128
    learning_rate = 1e-3

    transform = transforms.Compose(
        [transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))])

    trainset = MNIST(root = './data', train=True, download=True, transform=transform)
    train_loader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=2, pin_memory=True)

    testset = MNIST(root = './data', train=False, download=True, transform=transform)
    test_loader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=2, pin_memory=True)

    
    ########################################################################
    model = MLPMixer(patch_size = 4, hidden_dim = 1024, depth = 2).to(device) # 参数自己设定，其中depth必须大于1
    # 这里需要调用optimizer，criterion(交叉熵)
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss()
    ########################################################################
    
    train(model, train_loader, optimizer, n_epochs, criterion)
    test(model, test_loader, criterion)
