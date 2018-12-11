import tensorflow as tf
from arguments import arguments
from utils import TextLoader
from model import Model
import os

class sample:
    def __init__(self, secnum):
        args = arguments()
        self.sample(args, secnum)

    def sample(self, args, secnum):
        data_loader = TextLoader(args.data_dir, args.batch_size, args.seq_length)
        args.vocab_size = data_loader.vocab_size
        chars = data_loader.chars
        vocab = data_loader.vocab
        model = Model(args, training=False)
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver = tf.train.Saver()
            ckpt = tf.train.get_checkpoint_state(args.save_dir)
            saver.restore(sess, ckpt.model_checkpoint_path)
            with open(os.getcwd() + '\\music\\' + str(secnum) + '.abc', "w") as f:
                f.write(model.sample(sess, chars, vocab, str(secnum)))
        tf.reset_default_graph()

