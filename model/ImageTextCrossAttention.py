from utils import ImageToTextAttention, TextToImageAttention
import torch.nn as nn
from model.TextFeatureExtractor import TextFeatureExtractor
from model.ImageFeatureExtractor import ImageFeatureExtractor


# 图文交叉注意力模块
class ImageTextCrossAttention(nn.Module):
    def __init__(self):
        super(ImageTextCrossAttention, self).__init__()

        self.text_feature_extractor = TextFeatureExtractor()
        self.image_feature_extractor = ImageFeatureExtractor()

    # text: 文本
    # image: 图片路径
    def forward(self, text, image):
        # 特征提取
        image_features = self.image_feature_extractor(image)
        text_features = self.text_feature_extractor(text)

        # Text to Image
        tti_attention_matrix = TextToImageAttention.preassign_attention(image_features, text_features)
        tti_score_matrix = TextToImageAttention.calculate_score(tti_attention_matrix)
        image_ss = TextToImageAttention.image_share_semantic(image_features, tti_score_matrix)
        image_ss_relevance = TextToImageAttention.relevance(text_features, image_ss)

        # Image to Text
        itt_score_matrix = tti_score_matrix.transpose(1, 2)
        text_ss = ImageToTextAttention.text_share_semantic(text_features, itt_score_matrix)
        text_ss_relevance = ImageToTextAttention.relevance(text_ss, image_features)

        # 合相似度
        return image_ss_relevance + text_ss_relevance