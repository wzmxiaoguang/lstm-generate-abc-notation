import os
import codecs
import collections
from six.moves import cPickle
import numpy as np


class TextLoader:
    def __init__(self, data_dir, batch_size, seq_length, encoding='utf-8'):
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.encoding = encoding

        input_file = os.path.join(data_dir, "input.txt")
        chars_file = os.path.join(data_dir, "chars.pkl")
        vocab_file = os.path.join(data_dir, "vocab.pkl")
        tensor_file = os.path.join(data_dir, "data.npy")
        if not (os.path.exists(chars_file) and os.path.exists(vocab_file) and os.path.exists(tensor_file)):
            self.preprocess(input_file, chars_file, vocab_file, tensor_file)
        else:
            self.load_preprocessed(chars_file, vocab_file, tensor_file)
        
        self.create_batches()
        self.reset_batch_pointer()

    def preprocess(self, input_file, chars_file, vocab_file, tensor_file):
        with codecs.open(input_file, "r", encoding=self.encoding) as f:
            data = f.read()
        counter = collections.Counter(data)  # 统计每个字符在数据中出现次数
        count_pairs = sorted(counter.items(), key=lambda x: -x[1])  # 按字符出现次数从大到小排序
        self.chars, _ = zip(*count_pairs)  # 将字符打包
        with open(chars_file, 'wb') as f:
            cPickle.dump(self.chars, f)
        self.vocab_size = len(self.chars)
        self.vocab = dict(zip(self.chars, range(self.vocab_size)))  # 给字符编号
        with open(vocab_file, 'wb') as f:
            cPickle.dump(self.vocab, f)
        self.tensor = np.array(list(map(self.vocab.get, data)))  # 将数据文件转为数字编码
        np.save(tensor_file, self.tensor)

    def load_preprocessed(self, chars_file, vocab_file, tensor_file):
        with open(chars_file, 'rb') as f:
            self.chars = cPickle.load(f)
        self.vocab_size = len(self.chars)
        with open(vocab_file, 'rb') as f:
            self.vocab = cPickle.load(f)
        self.tensor = np.load(tensor_file)

    def create_batches(self):
        """
        将数据拆分为num_batches组
        每组为[batch_size, seq_length]
        """
        self.num_batches = int(self.tensor.size / (self.batch_size * self.seq_length))
        self. tensor = self.tensor[:self.num_batches * self.batch_size * self.seq_length]
        xdata = self.tensor
        ydata = np.copy(self.tensor)
        ydata[:-1] = xdata[1:]
        ydata[-1] = xdata[0]
        self.x_batches = np.split(xdata.reshape(self.batch_size, -1), self.num_batches, 1)
        self.y_batches = np.split(ydata.reshape(self.batch_size, -1), self.num_batches, 1)

    def next_batch(self):
        x, y = self.x_batches[self.pointer], self.y_batches[self.pointer]
        self.pointer += 1
        return x, y

    def reset_batch_pointer(self):
        self.pointer = 0


