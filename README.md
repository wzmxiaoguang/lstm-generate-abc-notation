# lstm-generate-abc-notation

使用lstm网络生成abc notation曲谱并转换为midi文件播放

data - 存放训练数据的文件

logs - 存放tensorflow生成的summary

music - 存放生成的abc和midi文件

save - 存放训练完成的模型参数

arguments.py - 存放各种参数的文件

dataset.py - 用于生成训练集的文件,‘_’代表结束符

utils.py - 对训练数据进行处理

model.py - 存放tensorflow训练和生成用模型

train.py - 训练并保存模型参数用文件

sample.py - 用于生成一首abc歌的类

mode.py - 绘制频谱效果

gui.py - 用pyqt制作的简易界面，用于播放生成的音乐， 可切歌，有频谱效果



