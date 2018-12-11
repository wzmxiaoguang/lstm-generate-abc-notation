import tensorflow as tf
import os
from arguments import arguments
from utils import TextLoader
from model import Model


class train:
    def __init__(self):
        args = arguments()
        self.training(args)
 
    def training(self, args):
        data_loader = TextLoader(args.data_dir, args.batch_size, args.seq_length)
        args.vocab_size = data_loader.vocab_size
        if os.path.isdir(args.save_dir):
            ckpt = tf.train.get_checkpoint_state(args.save_dir)
        else:
            os.makedirs(args.save_dir)
            ckpt = None
        model = Model(args)

        with tf.Session() as sess:
            tf.summary.FileWriter(os.getcwd()+'\\logs', sess.graph)
            # 使用cmd在当前目录键入 tensorboard --logdir=logs，并根据提示在chrome打开网址查看网络结构
            sess.run(tf.global_variables_initializer())
            saver = tf.train.Saver()
            now_epochs = 0
            if ckpt:
                saver.restore(sess, ckpt.model_checkpoint_path)
                now_epochs = int(ckpt.model_checkpoint_path.split('-')[1]) // data_loader.num_batches
            count = 0
            for e in range(now_epochs, args.num_epochs):
                sess.run(tf.assign(model.lr, args.learning_rate * (args.decay_rate ** e)))
                data_loader.reset_batch_pointer()
                state = sess.run(model.initial_state)
                for b in range(data_loader.num_batches):
                    x, y = data_loader.next_batch()
                    feed = {model.input_data: x, model.targets: y}
                    for i, (c, h) in enumerate(model.initial_state):
                        feed[c] = state[i].c
                        feed[h] = state[i].h
                    train_loss, state, _ = sess.run([model.cost, model.final_state, model.train_op], feed)

                    if count % 5 == 0:
                        percent = (e * data_loader.num_batches + b + 1) / (args.num_epochs * data_loader.num_batches)
                        print('%' + str(int(percent*100)) + '|' + '▉'*int(50*percent) + ' '*2*(50-int(50*percent)) + '|')
                    count += 1

                checkpoint_path = os.path.join(args.save_dir, 'model.ckpt')
                saver.save(sess, checkpoint_path, global_step=(e + 1) * data_loader.num_batches)
            print('%100'+'|'+'▉'*50+'|')
        tf.reset_default_graph()


if __name__ == '__main__':
    trainer = train()
