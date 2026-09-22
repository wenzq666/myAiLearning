import os

import pandas as pd
import torch
import torch.nn.functional as F

from src.config import Config
from src.models.label_semantic_macbert import LabelSemanticMacBERT


config = Config()


class IntentClassifier:

    def __init__(
            self,
            confidence_threshold=0.50,
            ambiguous_margin_threshold=0.15,
            max_length=64
    ):

        self.device = config.device

        self.tokenizer = (
            config.tokenizer
        )

        self.confidence_threshold = (
            confidence_threshold
        )

        self.ambiguous_margin_threshold = (
            ambiguous_margin_threshold
        )

        self.max_length = (
            max_length
        )

        # =============================================
        # Label Mapping
        # =============================================

        self.label_mapping = (
            self._load_label_mapping()
        )

        self.num_classes = (
            max(
                self.label_mapping.keys()
            )
            + 1
        )

        # =============================================
        # Temperature
        # =============================================

        self.temperature = (
            self._load_temperature()
        )

        # =============================================
        # Model
        # =============================================

        self.model = (
            self._load_model()
        )

    # =====================================================
    # Label Mapping
    # =====================================================

    def _load_label_mapping(self):

        train_path = (
            config.PROCESSED_DATA_DIR
            + "/train_clean.csv"
        )

        if not os.path.exists(
            train_path
        ):

            raise FileNotFoundError(
                f"找不到训练数据："
                f"{train_path}"
            )

        df = pd.read_csv(
            train_path
        )

        mapping_df = (
            df[
                [
                    "label",
                    "label_des"
                ]
            ]
            .drop_duplicates(
                subset=["label"]
            )
            .sort_values(
                "label"
            )
        )

        mapping = {}

        for _, row in (
            mapping_df.iterrows()
        ):

            label_id = int(
                row["label"]
            )

            label_des = str(
                row["label_des"]
            ).strip()

            mapping[
                label_id
            ] = label_des

        return mapping

    # =====================================================
    # Temperature
    # =====================================================

    def _load_temperature(self):

        temperature_path = (
            config.INTERIM_DATA_DIR
            + "/temperature.txt"
        )

        if not os.path.exists(
            temperature_path
        ):

            raise FileNotFoundError(
                "找不到 Temperature 文件："
                f"{temperature_path}"
            )

        with open(
            temperature_path,
            "r",
            encoding="utf-8"
        ) as f:

            temperature = float(
                f.read().strip()
            )

        if temperature <= 0:

            raise ValueError(
                "Temperature 必须 > 0"
            )

        return temperature

    # =====================================================
    # Model
    # =====================================================

    def _load_model(self):

        model_path = (
            config.bert_save_model
            + "/macbert_clean_label_semantic_best.pt"
        )

        if not os.path.exists(
            model_path
        ):

            raise FileNotFoundError(
                f"找不到模型："
                f"{model_path}"
            )

        model = (
            LabelSemanticMacBERT(
                bert_path=
                    config.bert_path,

                num_classes=
                    self.num_classes,

                temperature=
                    0.05
            )
        )

        state_dict = (
            torch.load(
                model_path,
                map_location=
                    self.device
            )
        )

        model.load_state_dict(
            state_dict
        )

        model = model.to(
            self.device
        )

        model.eval()

        return model

    # =====================================================
    # Encode
    # =====================================================

    def _encode(self, text):

        encoded = (
            self.tokenizer(
                text,
                max_length=
                    self.max_length,

                padding=
                    "max_length",

                truncation=
                    True,

                return_tensors=
                    "pt"
            )
        )

        input_ids = (
            encoded[
                "input_ids"
            ]
            .to(
                self.device
            )
        )

        attention_mask = (
            encoded[
                "attention_mask"
            ]
            .to(
                self.device
            )
        )

        return (
            input_ids,
            attention_mask
        )

    # =====================================================
    # Status Router
    # =====================================================

    def _get_status(
            self,
            confidence,
            margin
    ):

        # ---------------------------------------------
        # 高置信度
        # ---------------------------------------------

        if (
            confidence
            >= self.confidence_threshold
        ):

            return "accepted"

        # ---------------------------------------------
        # Top1 / Top2 非常接近
        # ---------------------------------------------

        if (
            margin
            < self.ambiguous_margin_threshold
        ):

            return "ambiguous"

        # ---------------------------------------------
        # 整体置信度不足
        # ---------------------------------------------

        return "uncertain"

    # =====================================================
    # Predict
    # =====================================================

    def predict(
            self,
            text,
            top_k=3
    ):

        if text is None:

            raise ValueError(
                "text 不能为空"
            )

        text = str(
            text
        ).strip()

        if not text:

            raise ValueError(
                "text 不能为空"
            )

        input_ids, attention_mask = (
            self._encode(
                text
            )
        )

        with torch.no_grad():

            outputs = (
                self.model(
                    input_ids=
                        input_ids,

                    attention_mask=
                        attention_mask
                )
            )

            logits = (
                outputs[
                    "classification_logits"
                ]
            )

            # =========================================
            # Temperature Scaling
            # =========================================

            calibrated_logits = (
                logits
                / self.temperature
            )

            probabilities = (
                F.softmax(
                    calibrated_logits,
                    dim=1
                )
            )

        probabilities = (
            probabilities[0]
            .detach()
            .cpu()
        )

        # =============================================
        # Top-K
        # =============================================

        top_k = max(
            2,
            top_k
        )

        top_k = min(
            top_k,
            self.num_classes
        )

        top_probs, top_labels = (
            torch.topk(
                probabilities,
                k=top_k
            )
        )

        top_results = []

        for prob, label_id in zip(
                top_probs.tolist(),
                top_labels.tolist()
        ):

            label_id = int(
                label_id
            )

            top_results.append(
                {
                    "label":
                        label_id,

                    "intent":
                        self.label_mapping[
                            label_id
                        ],

                    "confidence":
                        round(
                            float(prob),
                            4
                        )
                }
            )

        # =============================================
        # Top1 / Top2
        # =============================================

        best_result = (
            top_results[0]
        )

        second_result = (
            top_results[1]
        )

        confidence = float(
            top_probs[0]
        )

        second_confidence = float(
            top_probs[1]
        )

        margin = (
            confidence
            - second_confidence
        )

        # =============================================
        # Router
        # =============================================

        status = (
            self._get_status(
                confidence=
                    confidence,

                margin=
                    margin
            )
        )

        # =============================================
        # Result
        # =============================================

        return {
            "text":
                text,

            "label":
                best_result[
                    "label"
                ],

            "intent":
                best_result[
                    "intent"
                ],

            "confidence":
                round(
                    confidence,
                    4
                ),

            "second_intent":
                second_result[
                    "intent"
                ],

            "second_confidence":
                round(
                    second_confidence,
                    4
                ),

            "margin":
                round(
                    margin,
                    4
                ),

            "status":
                status,

            "top_k":
                top_results
        }

    # =====================================================
    # Batch Predict
    # =====================================================

    def predict_batch(
            self,
            texts,
            top_k=3
    ):

        results = []

        for text in texts:

            result = (
                self.predict(
                    text=text,
                    top_k=top_k
                )
            )

            results.append(
                result
            )

        return results


# =========================================================
# Test
# =========================================================

def main():

    classifier = (
        IntentClassifier()
    )

    print(
        "Temperature:",
        round(
            classifier.temperature,
            4
        )
    )

    print(
        "Confidence Threshold:",
        classifier.confidence_threshold
    )

    print(
        "Ambiguous Margin Threshold:",
        classifier.ambiguous_margin_threshold
    )

    test_texts = [
        "我的快递怎么还没到",
        "帮我修改一下收货地址",
        "这个和另外一款有什么区别",
        "双十一买两个有优惠吗",
        "什么时候可以发货"
    ]

    for text in test_texts:

        result = (
            classifier.predict(
                text,
                top_k=3
            )
        )

        print(
            "\n================================"
        )

        print(
            f"Text       : "
            f"{result['text']}"
        )

        print(
            f"Intent     : "
            f"{result['intent']}"
        )

        print(
            f"Confidence : "
            f"{result['confidence']:.4f}"
        )

        print(
            f"Second     : "
            f"{result['second_intent']}"
        )

        print(
            f"Second Conf: "
            f"{result['second_confidence']:.4f}"
        )

        print(
            f"Margin     : "
            f"{result['margin']:.4f}"
        )

        print(
            f"Status     : "
            f"{result['status']}"
        )

        print(
            "Top-K:"
        )

        for item in result[
            "top_k"
        ]:

            print(
                f"  "
                f"{item['intent']:<25} "
                f"{item['confidence']:.4f}"
            )


if __name__ == "__main__":
    main()