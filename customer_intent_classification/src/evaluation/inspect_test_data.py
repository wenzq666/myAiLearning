import json

from src.config import Config


config = Config()


def main():

    test_path = config.test_datapath

    print("Test Path:")
    print(test_path)

    # =============================================
    # JSON Lines 格式
    # 每一行是一个独立 JSON
    # =============================================

    data = []

    with open(
            test_path,
            "r",
            encoding="utf-8"
    ) as f:

        for line_num, line in enumerate(
                f,
                start=1
        ):

            line = line.strip()

            if not line:
                continue

            try:

                item = json.loads(
                    line
                )

                data.append(
                    item
                )

            except json.JSONDecodeError as e:

                print(
                    f"第 {line_num} 行解析失败："
                )

                print(line)

                raise e

    # =============================================
    # Basic Info
    # =============================================

    print(
        "\n===== Basic Info ====="
    )

    print(
        "Samples:",
        len(data)
    )

    if not data:

        print(
            "测试集为空"
        )

        return

    print(
        "Sample Type:",
        type(data[0])
    )

    # =============================================
    # First 5 Samples
    # =============================================

    print(
        "\n===== First 5 Samples ====="
    )

    for i, item in enumerate(
            data[:5]
    ):

        print(
            f"\nSample {i}:"
        )

        print(
            item
        )

        if isinstance(
                item,
                dict
        ):

            print(
                "Keys:",
                list(
                    item.keys()
                )
            )

    # =============================================
    # 所有字段
    # =============================================

    all_keys = set()

    for item in data:

        if isinstance(
                item,
                dict
        ):

            all_keys.update(
                item.keys()
            )

    print(
        "\n===== All Keys ====="
    )

    print(
        sorted(
            all_keys
        )
    )


if __name__ == "__main__":
    main()