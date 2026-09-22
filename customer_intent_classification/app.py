import streamlit as st

from src.router.intent_router import IntentRouter


# =========================================================
# Page
# =========================================================

st.set_page_config(
    page_title="电商智能客服",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>
.block-container {
    max-width: 1600px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 0.4rem 0.8rem;
    margin-bottom: 0.6rem;
}

[data-testid="stMetric"] {
    border: 1px solid rgba(128, 128, 128, 0.22);
    border-radius: 10px;
    padding: 12px 14px;
}

div[data-testid="stProgress"] {
    margin-bottom: 0.2rem;
}

.analysis-label {
    font-size: 0.8rem;
    opacity: 0.6;
    margin-bottom: 0.2rem;
}

.analysis-value {
    font-size: 1.15rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
}
</style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# Load Model
# =========================================================

@st.cache_resource
def load_router():
    return IntentRouter()


router = load_router()


# =========================================================
# Session
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "您好，我是电商智能客服，请问有什么可以帮您？"
        }
    ]

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None


# =========================================================
# Header
# =========================================================

title_col, clear_col = st.columns([8, 1])

with title_col:
    st.title("🤖 电商智能客服")

    st.caption(
        "基于 Label Semantic MacBERT 的中文电商客服细粒度意图识别系统"
    )

with clear_col:
    st.write("")

    if st.button(
        "清空对话",
        use_container_width=True
    ):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "您好，我是电商智能客服，请问有什么可以帮您？"
            }
        ]

        st.session_state.analysis_result = None

        st.rerun()


st.divider()


# =========================================================
# Main Layout
# =========================================================

chat_col, analysis_col = st.columns(
    [1.7, 1],
    gap="large"
)


# =========================================================
# LEFT：Chat
# =========================================================

with chat_col:

    st.subheader("客服对话")

    chat_container = st.container(
        height=610
    )

    with chat_container:

        for message in st.session_state.messages:

            with st.chat_message(
                message["role"]
            ):
                st.markdown(
                    message["content"]
                )


# =========================================================
# RIGHT：Analysis
# =========================================================

with analysis_col:

    st.subheader("模型实时分析")

    result = st.session_state.analysis_result

    analysis_container = st.container(
        height=610,
        border=True
    )

    with analysis_container:

        # =================================================
        # No Prediction
        # =================================================

        if result is None:

            st.info(
                "发送一条买家消息后，这里会实时显示模型分析结果。"
            )

            st.markdown("### 当前模型")

            st.write(
                "Label Semantic MacBERT"
            )

            st.markdown("### 模型能力")

            st.write(
                "118 类中文电商细粒度意图识别"
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Test Accuracy",
                "82.05%"
            )

            col2.metric(
                "Test Macro-F1",
                "76.45%"
            )

            st.caption(
                "Independent Test · 2000 samples"
            )

        # =================================================
        # Prediction
        # =================================================

        else:

            # ---------------------------------------------
            # Intent
            # ---------------------------------------------

            st.caption(
                "FINE-GRAINED INTENT"
            )

            st.markdown(
                f"### {result['intent']}"
            )

            st.divider()

            # ---------------------------------------------
            # Domain
            # ---------------------------------------------

            st.caption(
                "BUSINESS DOMAIN"
            )

            st.markdown(
                f"### {result['domain_name']}"
            )

            st.divider()

            # ---------------------------------------------
            # Metrics
            # ---------------------------------------------

            col1, col2 = st.columns(2)

            col1.metric(
                "Confidence",
                f"{result['confidence']:.4f}"
            )

            col2.metric(
                "Top1-Top2 Margin",
                f"{result['margin']:.4f}"
            )

            # ---------------------------------------------
            # Decision
            # ---------------------------------------------

            st.markdown("### 系统决策")

            status = result["status"]

            if status == "accepted":

                st.success(
                    "✓ ACCEPTED\n\n"
                    "高置信度预测，可以进入业务路由。"
                )

            elif status == "ambiguous":

                st.error(
                    "⚠ AMBIGUOUS\n\n"
                    "Top1 与 Top2 过于接近，需要进一步澄清。"
                )

            else:

                st.warning(
                    "△ UNCERTAIN\n\n"
                    "当前预测置信度不足，暂不自动执行。"
                )

            # ---------------------------------------------
            # Meta
            # ---------------------------------------------

            col1, col2 = st.columns(2)

            with col1:
                st.caption("LABEL")
                st.write(
                    f"**{result['label']}**"
                )

            with col2:
                st.caption("ACTION")
                st.write(
                    f"**{result['action'].upper()}**"
                )

            st.divider()

            # ---------------------------------------------
            # Top-K
            # ---------------------------------------------

            st.markdown("### Top-K 候选意图")

            for index, item in enumerate(
                result["top_k"],
                start=1
            ):

                confidence = float(
                    item["confidence"]
                )

                # Top1 单独突出
                if index == 1:
                    prefix = "🥇"
                elif index == 2:
                    prefix = "🥈"
                elif index == 3:
                    prefix = "🥉"
                else:
                    prefix = f"{index}."

                st.write(
                    f"{prefix} **{item['intent']}**"
                )

                st.progress(
                    min(
                        max(
                            confidence,
                            0.0
                        ),
                        1.0
                    )
                )

                st.caption(
                    f"Confidence {confidence:.4f}"
                )


# =========================================================
# Input
# =========================================================

prompt = st.chat_input(
    "请输入买家咨询内容，例如：我的快递怎么还没有到"
)


# =========================================================
# Prediction
# =========================================================

if prompt:

    # User
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Model
    result = router.route(
        prompt,
        top_k=5
    )

    st.session_state.analysis_result = result

    status = result["status"]

    # =====================================================
    # Demo Response
    # =====================================================

    if status == "accepted":

        response = (
            f"已识别您的问题属于「{result['domain_name']}」业务，"
            f"具体意图为「{result['intent']}」。"
        )

    elif status == "ambiguous":

        response = (
            f"我理解您的问题可能与"
            f"「{result['intent']}」或"
            f"「{result['second_intent']}」有关，"
            f"请问您具体想咨询哪一种？"
        )

    else:

        response = (
            f"我初步判断您的问题可能是"
            f"「{result['intent']}」，"
            f"但当前置信度不足，"
            f"暂不自动执行后续业务操作。"
        )

    # Assistant
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    st.rerun()