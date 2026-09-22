from src.inference.intent_classifier import IntentClassifier


class IntentRouter:

    # =====================================================
    # 1. 一级业务域
    # =====================================================

    DOMAIN_NAMES = {

        "PRODUCT":
            "商品咨询",

        "PROMOTION":
            "优惠活动",

        "ORDER":
            "订单与下单",

        "PAYMENT":
            "支付",

        "SHIPPING":
            "发货物流",

        "AFTER_SALES":
            "退款退换货",

        "INVOICE":
            "发票",

        "MEMBER":
            "会员与账号",

        "SERVICE":
            "服务与沟通",

        "OTHER":
            "其他"
    }

    # =====================================================
    # 2. Label -> Domain
    # =====================================================

    LABEL_DOMAIN_MAP = {

        # -------------------------------------------------
        # PRODUCT
        # 商品本身相关
        # -------------------------------------------------

        17: "PRODUCT",
        21: "PRODUCT",
        32: "PRODUCT",
        40: "PRODUCT",
        52: "PRODUCT",
        63: "PRODUCT",
        65: "PRODUCT",
        75: "PRODUCT",
        76: "PRODUCT",
        77: "PRODUCT",
        78: "PRODUCT",
        79: "PRODUCT",
        80: "PRODUCT",
        81: "PRODUCT",
        82: "PRODUCT",
        83: "PRODUCT",
        84: "PRODUCT",
        85: "PRODUCT",
        87: "PRODUCT",
        88: "PRODUCT",
        89: "PRODUCT",
        90: "PRODUCT",
        91: "PRODUCT",
        100: "PRODUCT",
        101: "PRODUCT",
        102: "PRODUCT",

        # -------------------------------------------------
        # PROMOTION
        # -------------------------------------------------

        0: "PROMOTION",
        26: "PROMOTION",
        38: "PROMOTION",

        56: "PROMOTION",
        57: "PROMOTION",
        58: "PROMOTION",

        60: "PROMOTION",
        62: "PROMOTION",
        68: "PROMOTION",
        71: "PROMOTION",

        86: "PROMOTION",

        92: "PROMOTION",
        98: "PROMOTION",
        99: "PROMOTION",

        112: "PROMOTION",
        115: "PROMOTION",
        116: "PROMOTION",

        # -------------------------------------------------
        # ORDER
        # -------------------------------------------------

        3: "ORDER",
        4: "ORDER",
        8: "ORDER",
        9: "ORDER",

        16: "ORDER",
        19: "ORDER",

        23: "ORDER",
        25: "ORDER",

        37: "ORDER",

        43: "ORDER",
        45: "ORDER",

        49: "ORDER",

        72: "ORDER",

        # -------------------------------------------------
        # PAYMENT
        # -------------------------------------------------

        35: "PAYMENT",

        44: "PAYMENT",

        64: "PAYMENT",

        94: "PAYMENT",
        96: "PAYMENT",

        # -------------------------------------------------
        # SHIPPING
        # -------------------------------------------------

        11: "SHIPPING",

        20: "SHIPPING",
        24: "SHIPPING",

        29: "SHIPPING",

        42: "SHIPPING",

        50: "SHIPPING",
        51: "SHIPPING",

        53: "SHIPPING",
        54: "SHIPPING",
        55: "SHIPPING",

        61: "SHIPPING",

        66: "SHIPPING",

        69: "SHIPPING",

        73: "SHIPPING",

        93: "SHIPPING",

        97: "SHIPPING",

        111: "SHIPPING",

        113: "SHIPPING",

        # -------------------------------------------------
        # AFTER_SALES
        # -------------------------------------------------

        6: "AFTER_SALES",

        12: "AFTER_SALES",
        13: "AFTER_SALES",

        18: "AFTER_SALES",

        22: "AFTER_SALES",

        36: "AFTER_SALES",

        41: "AFTER_SALES",

        46: "AFTER_SALES",
        48: "AFTER_SALES",

        59: "AFTER_SALES",

        74: "AFTER_SALES",

        95: "AFTER_SALES",

        103: "AFTER_SALES",
        104: "AFTER_SALES",
        105: "AFTER_SALES",
        106: "AFTER_SALES",
        107: "AFTER_SALES",

        108: "AFTER_SALES",
        109: "AFTER_SALES",
        110: "AFTER_SALES",

        114: "AFTER_SALES",

        # -------------------------------------------------
        # INVOICE
        # -------------------------------------------------

        34: "INVOICE",
        67: "INVOICE",

        # -------------------------------------------------
        # MEMBER
        # -------------------------------------------------

        15: "MEMBER",
        47: "MEMBER",
        70: "MEMBER",
        117: "MEMBER",

        # -------------------------------------------------
        # SERVICE
        # -------------------------------------------------

        1: "SERVICE",
        2: "SERVICE",

        5: "SERVICE",

        7: "SERVICE",

        10: "SERVICE",

        14: "SERVICE",

        27: "SERVICE",
        28: "SERVICE",

        30: "SERVICE",
        31: "SERVICE",

        33: "SERVICE",

        39: "SERVICE",

        # -------------------------------------------------
        # OTHER
        # -------------------------------------------------

        # 当前没有必须放 OTHER 的标签
    }

    # =====================================================
    # Init
    # =====================================================

    def __init__(
            self,
            classifier=None
    ):

        if classifier is None:

            classifier = (
                IntentClassifier()
            )

        self.classifier = classifier

        self._validate_mapping()

    # =====================================================
    # 检查 118 类是否全部完成映射
    # =====================================================

    def _validate_mapping(self):

        classifier_labels = set(
            self.classifier
            .label_mapping
            .keys()
        )

        router_labels = set(
            self.LABEL_DOMAIN_MAP
            .keys()
        )

        missing_labels = (
            classifier_labels
            - router_labels
        )

        unknown_labels = (
            router_labels
            - classifier_labels
        )

        if missing_labels:

            missing_info = []

            for label in sorted(
                    missing_labels
            ):

                intent = (
                    self.classifier
                    .label_mapping
                    .get(
                        label,
                        "UNKNOWN"
                    )
                )

                missing_info.append(
                    f"{label}: {intent}"
                )

            raise ValueError(
                "以下 Intent 尚未配置业务域：\n"
                + "\n".join(
                    missing_info
                )
            )

        if unknown_labels:

            raise ValueError(
                "Router 中存在未知 Label："
                f"{sorted(unknown_labels)}"
            )

    # =====================================================
    # 根据 Label 获取 Domain
    # =====================================================

    def get_domain(
            self,
            label
    ):

        domain_code = (
            self.LABEL_DOMAIN_MAP
            .get(
                int(label),
                "OTHER"
            )
        )

        domain_name = (
            self.DOMAIN_NAMES[
                domain_code
            ]
        )

        return {
            "domain_code":
                domain_code,

            "domain_name":
                domain_name
        }

    # =====================================================
    # Router
    # =====================================================

    def route(
            self,
            text,
            top_k=3
    ):

        prediction = (
            self.classifier.predict(
                text=text,
                top_k=top_k
            )
        )

        domain = (
            self.get_domain(
                prediction[
                    "label"
                ]
            )
        )

        # =============================================
        # 根据模型状态决定下一步
        # =============================================

        status = (
            prediction[
                "status"
            ]
        )

        if status == "accepted":

            action = (
                "route"
            )

        elif status == "ambiguous":

            action = (
                "clarify"
            )

        else:

            action = (
                "fallback"
            )

        return {

            "text":
                text,

            "label":
                prediction[
                    "label"
                ],

            "intent":
                prediction[
                    "intent"
                ],

            "domain_code":
                domain[
                    "domain_code"
                ],

            "domain_name":
                domain[
                    "domain_name"
                ],

            "confidence":
                prediction[
                    "confidence"
                ],

            "margin":
                prediction[
                    "margin"
                ],

            "status":
                status,

            "action":
                action,

            "second_intent":
                prediction[
                    "second_intent"
                ],

            "top_k":
                prediction[
                    "top_k"
                ]
        }


# =========================================================
# Test
# =========================================================

def main():

    router = (
        IntentRouter()
    )

    print(
        "Router Mapping:",
        len(
            router.LABEL_DOMAIN_MAP
        )
    )

    test_texts = [

        "什么时候可以发货",

        "我的快递怎么还没有到",

        "帮我修改一下收货地址",

        "这个衣服是什么面料",

        "双十一有没有优惠",

        "这个商品我想退掉",

        "退款什么时候到账",

        "可以开发票吗",

        "怎么加入会员",

        "谢谢亲，麻烦你了"
    ]

    for text in test_texts:

        result = (
            router.route(
                text
            )
        )

        print(
            "\n=============================="
        )

        print(
            "Text       :",
            result[
                "text"
            ]
        )

        print(
            "Intent     :",
            result[
                "intent"
            ]
        )

        print(
            "Domain     :",
            result[
                "domain_name"
            ]
        )

        print(
            "Confidence :",
            result[
                "confidence"
            ]
        )

        print(
            "Margin     :",
            result[
                "margin"
            ]
        )

        print(
            "Status     :",
            result[
                "status"
            ]
        )

        print(
            "Action     :",
            result[
                "action"
            ]
        )

        if (
            result[
                "status"
            ]
            == "ambiguous"
        ):

            print(
                "Second     :",
                result[
                    "second_intent"
                ]
            )


if __name__ == "__main__":
    main()