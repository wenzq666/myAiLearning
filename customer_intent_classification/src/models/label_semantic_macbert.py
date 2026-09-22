import torch
import torch.nn as nn
import torch.nn.functional as F

from transformers import AutoModel


class LabelSemanticMacBERT(nn.Module):

    def __init__(
            self,
            bert_path,
            num_classes,
            temperature=0.05
    ):
        super().__init__()

        # =================================================
        # 1. 共享 MacBERT Encoder
        # =================================================

        self.bert = AutoModel.from_pretrained(
            bert_path
        )

        self.hidden_size = (
            self.bert.config.hidden_size
        )

        self.num_classes = num_classes

        # =================================================
        # 2. 普通分类头
        #
        # 保留原来的 MacBERT 分类能力
        # =================================================

        self.dropout = nn.Dropout(
            0.1
        )

        self.classifier = nn.Linear(
            self.hidden_size,
            num_classes
        )

        # =================================================
        # 3. Semantic Similarity Temperature
        # =================================================

        self.temperature = temperature


    # =====================================================
    # Mean Pooling
    # =====================================================

    def mean_pooling(
            self,
            last_hidden_state,
            attention_mask
    ):

        # attention_mask:
        # [batch_size, seq_len]
        #
        # ->
        #
        # [batch_size, seq_len, 1]

        mask = (
            attention_mask
            .unsqueeze(-1)
            .float()
        )

        # -------------------------------------------------
        # PAD token 不参与 pooling
        # -------------------------------------------------

        summed = torch.sum(
            last_hidden_state * mask,
            dim=1
        )

        count = (
            mask
            .sum(dim=1)
            .clamp(min=1e-9)
        )

        embedding = (
            summed / count
        )

        return embedding


    # =====================================================
    # Encode Text
    # =====================================================

    def encode(
            self,
            input_ids,
            attention_mask
    ):

        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        embedding = self.mean_pooling(
            outputs.last_hidden_state,
            attention_mask
        )

        return embedding


    # =====================================================
    # Forward
    # =====================================================

    def forward(
            self,

            input_ids,
            attention_mask,

            label_input_ids=None,
            label_attention_mask=None
    ):

        # =================================================
        # 1. 用户文本 Encoding
        # =================================================

        text_embedding = self.encode(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        # =================================================
        # 2. 普通 Classification Head
        # =================================================

        classification_logits = (
            self.classifier(
                self.dropout(
                    text_embedding
                )
            )
        )

        # =================================================
        # 如果没有传 Label Description
        #
        # 推理时可以只使用普通分类头
        # =================================================

        if label_input_ids is None:

            return {
                "classification_logits":
                    classification_logits,

                "semantic_logits":
                    None,

                "text_embedding":
                    text_embedding,

                "label_embedding":
                    None
            }

        # =================================================
        # 3. Label Description Encoding
        #
        # shape:
        #
        # [num_classes, seq_len]
        #
        # ->
        #
        # [num_classes, hidden_size]
        # =================================================

        label_embedding = self.encode(
            input_ids=label_input_ids,
            attention_mask=label_attention_mask
        )

        # =================================================
        # 4. L2 Normalize
        #
        # cosine similarity
        # =================================================

        normalized_text = (
            F.normalize(
                text_embedding,
                p=2,
                dim=1
            )
        )

        normalized_label = (
            F.normalize(
                label_embedding,
                p=2,
                dim=1
            )
        )

        # =================================================
        # 5. Text × Label Semantic Similarity
        #
        # text:
        # [batch, hidden]
        #
        # label:
        # [118, hidden]
        #
        # ->
        #
        # [batch, 118]
        # =================================================

        semantic_logits = torch.matmul(
            normalized_text,
            normalized_label.transpose(
                0,
                1
            )
        )

        # =================================================
        # 6. Temperature Scaling
        # =================================================

        semantic_logits = (
            semantic_logits
            /
            self.temperature
        )

        return {

            "classification_logits":
                classification_logits,

            "semantic_logits":
                semantic_logits,

            "text_embedding":
                text_embedding,

            "label_embedding":
                label_embedding
        }