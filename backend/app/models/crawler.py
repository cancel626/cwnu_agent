from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class CrawlSource(Base):
    __tablename__ = "crawl_sources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="数据源名称")
    source_type = Column(String(50), default="custom", comment="类型: preset 预设, custom 自定义")
    base_url = Column(Text, nullable=False, comment="基础URL，包含 {keyword} 占位符")
    keyword_placeholder = Column(String(50), default="{keyword}", comment="关键词占位符")
    description = Column(Text, nullable=True, comment="描述")
    # 自定义参数，如 headers、cookies 等
    params = Column(JSON, default=dict, comment="自定义参数")
    # 爬取规则: [{"type": "css|xpath", "selector": "...", "field": "title|content|url|..."}]
    rules = Column(JSON, default=list, comment="爬取规则列表")
    max_depth = Column(Integer, default=1, comment="爬取深度")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")


class CrawlTask(Base):
    __tablename__ = "crawl_tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    source_id = Column(Integer, ForeignKey("crawl_sources.id"), nullable=False, comment="数据源ID")
    keyword = Column(String(255), nullable=False, comment="采集关键词")
    status = Column(String(20), default="pending", comment="状态: pending/running/completed/failed")
    result_count = Column(Integer, default=0, comment="结果数量")
    error_msg = Column(Text, nullable=True, comment="错误信息")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    completed_at = Column(DateTime, nullable=True, comment="完成时间")


class CrawledData(Base):
    __tablename__ = "crawled_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("crawl_tasks.id"), nullable=False, comment="任务ID")
    source_id = Column(Integer, ForeignKey("crawl_sources.id"), nullable=False, comment="数据源ID")
    title = Column(Text, nullable=True, comment="标题")
    content = Column(Text, nullable=True, comment="内容")
    url = Column(Text, nullable=True, comment="来源URL")
    # 原始爬取数据
    raw_data = Column(JSON, default=dict, comment="原始数据")
    # crawl4ai 获取的 markdown 原始内容
    markdown_content = Column(Text, nullable=True, comment="Markdown原始内容")
    # AI 清洗后的摘要
    summary = Column(Text, nullable=True, comment="内容摘要")
    # AI 提取的关键词
    keywords = Column(JSON, default=list, comment="关键词列表")
    # AI 提取的实体（地名、人名、机构等）
    entities = Column(JSON, default=dict, comment="实体信息")
    is_saved = Column(Boolean, default=False, comment="是否已保存到数据仓库")
    # 内容安全审核结果
    audit_status = Column(String(20), default="pending", comment="审核状态: pending/pass/rejected")
    audit_result = Column(JSON, default=dict, comment="审核结果JSON: {is_violation, type, reason, confidence}")
    audited_at = Column(DateTime, nullable=True, comment="审核时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
