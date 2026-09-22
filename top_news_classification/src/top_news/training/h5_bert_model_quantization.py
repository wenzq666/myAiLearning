from src.top_news.config import Config                   # 导入配置类
import torch                                # 深度学习框架
from src.top_news.models.h2_bert_classifier_model import BertClassifier # 导入自定义的BERT分类器模型
from src.top_news.training.h1_dataloader_utils import build_dataloader    # 导入数据集加载器
from src.top_news.training.h3_train_predict import model2dev              # 导入自定义的验证函数

# todo 0.(可选) 查看并配置量化引擎.
# 打印当前环境支持的 量化计算 后端引擎, 了解可用的量化加入方式.
# 常见的引擎包括: ['none', 'onednn', 'x86', 'fbgemm'] -> ['无加速', '英特尔深度学习加速', 'x86架构优化', 'FaceBook的量化计算库']
print(torch.backends.quantized.supported_engines)

# 设置引擎为: onednn(英特尔深度学习加速)
# torch.backends.quantized.engine = 'onednn'      # 非必须操作(可选), PyTorch会根据硬件自动选择最合适的引擎.
print(torch.backends.quantized.engine)
# todo 1.加载配置参数.
conf = Config()

# todo 2. 构建数据集加载器.
train_dataloader, test_dataloader, dev_dataloader = build_dataloader()


# todo 3. 初始化模型, 并加载参数.
model = BertClassifier()
model.load_state_dict(torch.load(conf.model_save_path, map_location='cpu', weights_only=True))
# 将模型设置为: 评估模式(会关闭训练时的dropout等随机层, 确保推理结果稳定)
model.eval()
print(f'量化前的模型: {model}')

# todo 4. 量化前模型性能验证.
report_test, accuracy_test, precision_test, recall_test, f1_test = model2dev(model, dev_dataloader, device='cpu')
print(f"量化前--准确率:{accuracy_test},精确率{precision_test},召回率{recall_test},f1值{f1_test}")

# todo 5. 执行模型动态量化.
# 参1 model: 待量化的模型.
# 参2 {torch.nn.Linear}: 待量化的层, 这里是仅对 Linear层进行量化.
# 参3: dtype: 量化(后)的数据类型.
# qint8 带量化后的整数值 还有 Z 和 S
quantized_model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
print(f'量化后的模型: {quantized_model}')

# todo 6. 量化后的模型性能验证.
report_quantized, accuracy_quantized, precision_quantized, recall_quantized, f1_quantized = model2dev(quantized_model, dev_dataloader, device='cpu')
print(f"量化后--准确率:{accuracy_quantized},精确率{precision_quantized},召回率{recall_quantized},f1值{f1_quantized}")



# todo 7. 保存量化后的模型.
torch.save(quantized_model.state_dict(),conf.bert_model_quantization_model_path)