'''
https://github.com/prlz77/attend-and-rectify
'''
import numpy as np
import torch
import torch.nn.functional as F


class Gate(torch.nn.Module):
    """
    Attention Gate. Weights Attention output by its importance.
    """

    def __init__(self, in_ch, ngates=1, gate_depth=1):
        """ Constructor
        Args:
            in_ch: number of input channels.
        """
        super(Gate, self).__init__()
        if gate_depth == 1:
            self.gates = torch.nn.Linear(in_ch, ngates, bias=False)
        else:
            self.gates = torch.nn.Linear(in_ch // 2, ngates, bias=False)
            self.pre_gates = torch.nn.Linear(in_ch, in_ch // 2, bias=False)
            torch.nn.init.kaiming_normal_(self.pre_gates.weight.data)
            self.pre_bn = torch.nn.BatchNorm1d(in_ch // 2)

        torch.nn.init.kaiming_normal_(self.gates.weight.data)
        self.bn = torch.nn.BatchNorm1d(ngates)

        self.gate_depth = gate_depth

    def forward(self, x):
        """ Pytorch forward function
        Args:
            x: input Variable
        Returns: gate value (Variable)
        """
        if self.gate_depth == 1:
            return torch.tanh(self.bn(self.gates(x)))
        else:
            return torch.tanh(self.bn(self.gates(F.relu(self.pre_bn(self.pre_gates(x))))))


class AttentionHead(torch.nn.Module):
    """ Attention Heads
    Attentds a given feature map. Provides inter-mask regularization.
    """

    def __init__(self, in_ch, nheads=1):
        """ Constructor
        Args:
            in_ch: input feature map channels
            nheads: number of attention masks
        """
        super(AttentionHead, self).__init__()
        self.nheads = nheads
        self.conv = torch.nn.Conv2d(in_ch, nheads, kernel_size=3, padding=1, bias=False)
        torch.nn.init.kaiming_normal_(self.conv.weight.data)
        self.register_buffer("diag", torch.from_numpy(1 - np.eye(self.nheads, self.nheads).reshape(1, self.nheads, self.nheads)).float())

    def reg_loss(self):
        """ Regularization Loss
        Returns: a Variable with the inter-head regularization loss.
        """
        mask2loss = self.att_mask.view(self.att_mask.size(0), self.nheads, -1)
        reg_loss = torch.bmm(mask2loss, mask2loss.transpose(1, 2)) * torch.autograd.Variable(self.diag, requires_grad=False)

        return (reg_loss.view(-1) ** 2).mean()

    def forward(self, x):
        """ Pytorch Forward
        Args:
            x: input feature map
        Returns: the multiple attended feature maps
        """
        b, c, h, w = x.size()
        att_mask = F.softmax(self.conv(x).view(b, self.nheads, w * h), 2).view(b, self.nheads, h, w)
        self.att_mask = F.avg_pool2d(att_mask, 2, 2)
        return att_mask


class OutHead(torch.nn.Module):
    """ Attention Heads
    Attentds a given feature map. Provides inter-mask regularization.
    """

    def __init__(self, in_ch, out_ch):
        """ Constructor
        Args:
            in_ch: input feature map channels
            nheads: number of attention masks
        """
        super(OutHead, self).__init__()
        self.conv = torch.nn.Conv2d(in_ch, out_ch, kernel_size=3, padding=1, bias=False)
        torch.nn.init.kaiming_normal_(self.conv.weight.data)

    def forward(self, x):
        """ Pytorch Forward
        Args:
            x: input feature map
        Returns: the multiple attended feature maps
        """
        return self.conv(x)


class AttentionModule(torch.nn.Module):
    """ Attention Module
    Applies different attention masks with the Attention Heads and ouputs classification hypotheses.
    """

    def __init__(self, in_ch, nlabels, nheads=1, reg_w=0.0, self_attention=True):
        """ Constructor
        Args:
            in_ch: number of input feature map channels
            h: input feature map height
            w: input feature map width
            nlabels: number of output classes
            nheads: number of attention heads
            has_gates: whether to use gating (recommended)
            reg_w: inter-mask regularization weight
        """
        super(AttentionModule, self).__init__()
        self.in_ch = in_ch
        self.nlabels = nlabels
        self.nheads = nheads
        self.reg_w = reg_w
        self.self_attention = self_attention

        self.att_head = AttentionHead(in_ch, nheads)
        self.out_head = OutHead(in_ch, nlabels * nheads)
        if self.self_attention:
            self.score = OutHead(in_ch, nheads)

    def reg_loss(self):
        """ Regularization loss
        Returns: A Variable with the inter-mask regularization loss for this  Attention Module.
        """
        return self.att_head.reg_loss() * self.reg_w

    def forward(self, x):
        """ Pytorch Forward
        Args:
            x: input feature map.
        Returns: tuple with predictions and gates. Gets are set to None if disabled.
        """
        b, c, h, w = x.size()
        
        # Spatial attention에 대해서 output head의 결과와 broadcasting으로 각 클래스별 spatial 정보들과 곱
        # 곱한 후 spatial 정보를 하나로 합하여 각 nheads개의 클래스별 하나의 attention 값이 나옴
        att_mask = self.att_head(x).view(b, self.nheads, 1, h * w)  
        output = (self.out_head(x).view(b, self.nheads, self.nlabels, h * w) * att_mask).sum(3) # (b, self.nhead, self.nlabels)
        
        # 각 nhead의 self attention은 spatial attention과 각 nhead의 spatial 정보를 곱한 후 spatial 정보를 하나로 합함
        # 합해진 결과를 self.nhead 간 softmax로 계산 후 output의 self.nhead와 곱하여 self.nhead를 기준으로 하나로 합함
        if self.self_attention:
            scores = self.score(x).view(b, self.nheads, 1, h * w)
            scores = (scores * att_mask).sum(3) # (b, self.nhead, 1)
            scores = F.softmax(torch.tanh(scores), 1) 
            return (output * scores).sum(1, keepdim=True) # (b, 1, self.nlabels)
        else:
            return output

    @staticmethod
    def aggregate(outputs, gates, function='softmax'):
        """ Generates the final output after aggregating all the attention modules.
        Args:
            last_output: network output logits
            last_gate: gate for the network output
        Returns: final network prediction
        """
        outputs = torch.cat(outputs, 1) # (b, len(outputs), nb_class)
        outputs = F.log_softmax(outputs, dim=2) 
        if gates is not None:
            # outputs의 수와 gates 수는 같음
            # 각 gates에 softmax or sigmoid 적용 후 outputs의 채널(len(outputs))을 기준으로 곱하고 더함
            if function == 'softmax':
                gates = F.softmax(gates, 1).view(gates.size(0), -1, 1) 
                ret = (outputs * gates).sum(1)
            else:
                gates = F.sigmoid(gates).view(gates.size(0), -1, 1)
                ret = (outputs * gates).sum(1) / (1e-6 + gates.sum(1))
        else:
            ret = outputs.mean(1)

        return ret # (b, nb_class)

class Block(torch.nn.Module):
    """
    Pre-activation residual block (3,3)
    """
    def __init__(self, ni, no, stride, dropout, save_input=False):
        """ Constructor
        Args:
            ni: input channels
            no: output channels
            stride: conv stride
            dropout: dropout prob
            save_input: retain input after batchnorm for later reuse
        """
        super(Block, self).__init__()
        self.dropout = dropout
        self.conv0 = torch.nn.Conv2d(ni, no, 3, stride=stride, padding=1, bias=False)
        torch.nn.init.kaiming_normal_(self.conv0.weight.data)
        self.bn0 = torch.nn.BatchNorm2d(ni)
        self.conv1 = torch.nn.Conv2d(no, no, 3, stride=1, padding=1, bias=False)
        self.bn1 = torch.nn.BatchNorm2d(no)
        torch.nn.init.kaiming_normal_(self.conv1.weight.data)
        self.reduce = ni != no
        self.save_input = save_input
        if self.reduce:
            self.conv_reduce = torch.nn.Conv2d(ni, no, 1, stride=stride, bias=False)
            torch.nn.init.kaiming_normal_(self.conv_reduce.weight.data)

    def forward(self, x):
        """ Pytorch Module forward
        Args:
            x: input
        Returns: block(x)
        """
        block_input = F.relu(self.bn0(x), True)

        if self.save_input:
            self.block_input = block_input

        y = self.conv0(block_input)
        o2 = F.relu(self.bn1(y), inplace=True)
        if self.dropout > 0:
            o2 = F.dropout2d(o2, self.dropout, training=self.training, inplace=True)
        z = self.conv1(o2)
        if self.reduce:
            return z + self.conv_reduce(x)
        else:
            return z + x


class Group(torch.nn.Module):
    """
    Wide ResNet Group
    """
    def __init__(self, ni, no, n, stride, dropout):
        """
        Args:
            ni: input channels
            no: output channels
            n: number of blocks
            stride: stride
            dropout: dropout prob
        """
        super(Group, self).__init__()
        self.n = n
        for i in range(n):
            self.__setattr__("block_%d" % i,
                             Block(ni if i == 0 else no, no, stride if i == 0 else 1, dropout, save_input=(i == 0)))

    def forward(self, x):
        """ Pytorch Module forward
        Args:
            x: input
        Returns: group(x)
        """
        for i in range(self.n):
            x = self.__getattr__("block_%d" % i)(x)
        return x