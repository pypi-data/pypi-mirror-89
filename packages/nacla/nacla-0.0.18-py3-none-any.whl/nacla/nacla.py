import torch
import os
import string
n_letters=57
n_hidden=128
n_categories=18

import torch.nn as nn
import torch
all_letters = string.ascii_letters + " .,;'"
n_letters = len(all_letters)
# Find letter index from all_letters, e.g. "a" = 0
def letterToIndex(letter):
    return all_letters.find(letter)

# Just for demonstration, turn a letter into a <1 x n_letters> Tensor
def letterToTensor(letter):
    tensor = torch.zeros(1, n_letters)
    tensor[0][letterToIndex(letter)] = 1
    return tensor

# Turn a line into a <line_length x 1 x n_letters>,
# or an array of one-hot letter vectors
def lineToTensor(line):
    tensor = torch.zeros(len(line), 1, n_letters)
    for li, letter in enumerate(line):
        tensor[li][0][letterToIndex(letter)] = 1
    return tensor
class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()

        self.hidden_size = hidden_size

        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        combined = torch.cat((input, hidden), 1)
        hidden = self.i2h(combined)
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, self.hidden_size)

# Just return an output given a line
def evaluate(rnn,line_tensor):
    hidden = rnn.initHidden()

    for i in range(line_tensor.size()[0]):
        output, hidden = rnn(line_tensor[i], hidden)

    return output




def rnn_predict(input_line, rnn,n_predictions=3):
    #print('\n> %s' % input_line)
    with torch.no_grad():
        #import pdb
        #pdb.set_trace()
        output = evaluate(rnn,lineToTensor(input_line))

        # Get top N categories
        topv, topi = output.topk(n_predictions, 1, True)
        predictions = []

        for i in range(n_predictions):
            value = topv[0][i].item()
            category_index = topi[0][i].item()
            print('(%.2f) %s' % (value, all_categories[category_index]))
            predictions.append([value, all_categories[category_index]])
all_categories=['Czech','German','Arabic','Japanese','Chinese','Vietnamese','Russian','French','Irish','English','Spanish','Greek','Italian','Portuguese','Scottish','Dutch','Korean','Polish']

def predict(namestr):
    dirpath=os.path.dirname(os.path.abspath(__file__))
    PATH=os.path.join(dirpath,"./model/rnn.pth")
    net = RNN(57,128,18)
    net.load_state_dict(torch.load(PATH))
    rnn_predict(namestr,net)
     
if __name__=="__main__":
    dirpath=os.path.dirname(os.path.abspath(__file__))
    PATH=os.path.join(dirpath,"./model/rnn.pth")
    net = RNN(57,128,18)
    net.load_state_dict(torch.load(PATH))
    rnn_predict("time",net)
