import asyncio
import uuid

import langfuse
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from sqlalchemy import text
from langfuse import get_client, Langfuse
from langfuse.langchain import CallbackHandler

from backend.agents.resume.state import ResumeState
from backend.agents.resume.nodes import (          # 导入 8 个节点函数
    upload_to_minio_node,
    download_pdf_node,
    extract_text_node,
    extract_structured_node,
    run_six_dimensions_node,
    diagnose_issues_node,
    generate_summary_node,
    save_results_node,
)
from backend.dependencies import AsyncSessionLocal

load_dotenv()


def build_resume_graph():
    builder = StateGraph(ResumeState)

    # 注册节点
    builder.add_node("upload_to_minio", upload_to_minio_node)
    builder.add_node("download_pdf", download_pdf_node)
    builder.add_node("extract_text", extract_text_node)
    builder.add_node("extract_structured", extract_structured_node)
    builder.add_node("run_six_dimensions", run_six_dimensions_node)
    builder.add_node("diagnose_issues", diagnose_issues_node)
    builder.add_node("generate_summary", generate_summary_node)
    builder.add_node("save_results", save_results_node)

    # ② 顺次连边：START → … → END（一条直线，无分支）
    builder.add_edge(START,                 "upload_to_minio")
    builder.add_edge("upload_to_minio",     "download_pdf")
    builder.add_edge("download_pdf",        "extract_text")
    builder.add_edge("extract_text",        "extract_structured")
    builder.add_edge("extract_structured",  "run_six_dimensions")
    builder.add_edge("run_six_dimensions",  "diagnose_issues")
    builder.add_edge("diagnose_issues",     "generate_summary")
    builder.add_edge("generate_summary",    "save_results")
    builder.add_edge("save_results",        END)


    # ③ 编译。不传 checkpointer：一次性任务，不需要断点恢复
    return builder.compile()


if __name__ == '__main__':
    graph = build_resume_graph()
    path = "../../tmp_data/sample_resume_anonymized.pdf"
    student_id = "student01"
    tenant_id = "tenant_default"


    rid = str(uuid.uuid4())

    # langfuse = Langfuse(
    #     public_key="pk-lf-ff50de47-a9ce-4e04-9e73-536891b0450a",
    #     secret_key="sk-lf-ae26e4f8-86de-486e-8d08-388eac352077",
    #     base_url="http://localhost:3000"  # 自托管则换成你的地址
    # )
    langfuse = get_client()
    langfuse_handler = CallbackHandler()

    if langfuse.auth_check():
        print("Langfuse 认证成功")
    else:
        print("认证失败，请检查 key 和 host")


    async def main():

        async with AsyncSessionLocal() as s:  # 先插一条 processing 记录
            sid = (await s.execute(text("SELECT id FROM users WHERE username='student01'"))).scalar()
            await s.execute(text("""INSERT INTO resume_reviews (id, tenant_id, student_id, pdf_minio_path, status)
                                    VALUES (:id, 'tenant_default', :sid, 'resumes/x.pdf', 'processing')"""),
                            {"id": rid, "sid": sid})
            await s.commit()

        state = {
            "messages": [], "student_id": student_id, "tenant_id": tenant_id,
            "review_id": rid, "pdf_minio_path": "", "pdf_local_path": path,
            "raw_text": "", "page_count": 0, "structured": None,
            "dimension_scores": [], "weighted_score": 0.0, "issues": [],
            "summary": None, "fallback_used": False, "structured_output": None,
        }
        await graph.ainvoke(state, config={"callbacks": [langfuse_handler]})

        get_client().flush()


    asyncio.run(main())


