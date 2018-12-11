import os

class arguments:
    def __init__(self):
        self.data_dir = os.getcwd() + '\\data'
        self.save_dir = os.getcwd() + '\\save'
        self.rnn_size = 128
        self.num_layers = 2
        self.batch_size = 50
        self.seq_length = 50
        self.num_epochs = 20
        self.grad_clip = 5
        self.learning_rate = 0.002
        self.decay_rate = 0.97
        self.vocab_size = 0
