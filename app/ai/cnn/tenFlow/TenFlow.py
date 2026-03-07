# import tensorFlow
#
# from tensorFlow.keras import layers, models, datasets
# import numpy as np
#
# # 加载数据集（这里使用CIFAR-10作为示例）
# (train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()
#
# # 数据预处理
# train_images, test_images = train_images / 255.0, test_images / 255.0
#
# # 定义一个简单的CNN模型
# model = models.Sequential([
#     layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
#     layers.MaxPooling2D((2, 2)),
#     layers.Conv2D(64, (3, 3), activation='relu'),
#     layers.MaxPooling2D((2, 2)),
#     layers.Conv2D(64, (3, 3), activation='relu'),
#     layers.Flatten(),
#     layers.Dense(64, activation='relu'),
#     layers.Dense(10)
# ])
#
# # 编译模型
# model.compile(optimizer='adam',
#               loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
#               metrics=['accuracy'])
#
# # 训练模型
# model.fit(train_images, train_labels, epochs=10, validation_data=(test_images, test_labels))
#
# # 这只是一个简单的示例。在实际应用中，你需要根据您的数据和任务调整模型的结构和超参数。
