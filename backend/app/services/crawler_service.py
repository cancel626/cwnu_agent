import asyncio
import json
import httpx
from typing import List, Dict, Any, Optional
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup
from markdownify import markdownify as md


try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class CrawlerService:
    """爬虫服务：基于 playwright/crawl4ai 获取页面内容，调用默认模型清洗整理"""

    @staticmethod
    def build_url(base_url: str, keyword: str, placeholder: str = "{keyword}") -> str:
        """替换 URL 中的关键词占位符，支持容错"""
        encoded = quote(keyword)
        if placeholder and placeholder in base_url:
            return base_url.replace(placeholder, encoded)
        for p in ["{keyword}", "{q}", "%s", "{query}"]:
            if p in base_url:
                return base_url.replace(p, encoded)
        sep = "&" if "?" in base_url else "?"
        return f"{base_url}{sep}q={encoded}"

    @staticmethod
    async def _call_default_model(db, system_prompt: str, user_content: str) -> str:
        """调用默认模型进行内容处理"""
        from app.models.model_config import ModelConfig
        model_cfg = db.query(ModelConfig).filter(ModelConfig.is_default == True, ModelConfig.is_active == True).first()
        if not model_cfg:
            raise Exception("未设置默认模型或默认模型未启用")

        url = f"{model_cfg.api_base.rstrip('/')}/chat/completions"
        payload = {
            "model": model_cfg.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "stream": False,
            "temperature": model_cfg.temperature or 0.3,
            "max_tokens": model_cfg.max_tokens or 4096
        }
        async with httpx.AsyncClient(timeout=model_cfg.timeout or 60, follow_redirects=True) as client:
            resp = await client.post(
                url,
                headers={"Authorization": f"Bearer {model_cfg.api_key}", "Content-Type": "application/json"},
                json=payload
            )
            resp.raise_for_status()
            result = resp.json()
            choices = result.get("choices", [])
            if choices:
                msg = choices[0].get("message", {})
                return msg.get("content", "")
        return ""

    @staticmethod
    async def _analyze_with_model(db, title: str, content: str) -> Dict[str, Any]:
        """调用模型提取摘要、关键词、实体"""
        system_prompt = (
            "你是一个信息提取助手。请对用户提供的新闻内容进行分析和整理，严格按以下 JSON 格式返回，不要输出任何其他文字：\n"
            "{\n"
            '  "summary": "200字以内的内容摘要",\n'
            '  "keywords": ["关键词1", "关键词2", "关键词3"],\n'
            '  "entities": {\n'
            '    "locations": ["地名1", "地名2"],\n'
            '    "organizations": ["机构1", "机构2"],\n'
            '    "persons": ["人名1", "人名2"],\n'
            '    "others": ["其他重要实体"]\n'
            '  }\n'
            "}\n"
            "要求：summary 必须准确概括全文；keywords 提取 3-8 个核心关键词；entities 中如果没有某类实体则返回空数组。"
        )
        user_content = f"标题：{title}\n\n内容：{content[:4000]}"
        raw = await CrawlerService._call_default_model(db, system_prompt, user_content)
        # 尝试从模型输出中提取 JSON
        text = raw.strip()
        # 去掉可能的 markdown 代码块
        if text.startswith("```"):
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()
        try:
            data = json.loads(text)
            return {
                "summary": data.get("summary", ""),
                "keywords": data.get("keywords", []),
                "entities": data.get("entities", {})
            }
        except Exception:
            # 如果 JSON 解析失败，返回原始内容作为摘要
            return {
                "summary": text[:500] if text else "",
                "keywords": [],
                "entities": {}
            }

    @staticmethod
    async def crawl_with_playwright(url: str) -> Dict[str, Any]:
        """使用 playwright 获取页面内容并转换为 markdown"""
        if not PLAYWRIGHT_AVAILABLE:
            raise Exception("playwright 未安装，请执行 playwright install chromium")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                locale="zh-CN"
            )
            page = await context.new_page()
            try:
                await page.goto(url, wait_until="networkidle", timeout=30000)
                # 等待页面稳定
                await page.wait_for_timeout(2000)
                # 获取页面标题
                title = await page.title()
                # 获取页面 HTML 并转换为 markdown
                html = await page.content()
                markdown = md(html, heading_style="ATX")
                # 同时获取纯文本内容
                text = await page.inner_text("body")
                await browser.close()
                return {
                    "title": title,
                    "markdown": markdown,
                    "text": text,
                    "html": html
                }
            except Exception as e:
                await browser.close()
                raise Exception(f"playwright 爬取失败: {str(e)}")

    @staticmethod
    async def crawl_with_requests(url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """使用 requests 作为 fallback 获取页面内容"""
        headers = params.get("headers", {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9",
        })
        cookies = params.get("cookies", {})
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            resp = await client.get(url, headers=headers, cookies=cookies)
            resp.raise_for_status()
            html = resp.text
            soup = BeautifulSoup(html, "html.parser")
            title = soup.title.string if soup.title else ""
            # 移除 script/style 标签
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            text = soup.get_text(separator="\n", strip=True)
            markdown = md(str(soup), heading_style="ATX")
            return {
                "title": title,
                "markdown": markdown,
                "text": text,
                "html": html
            }

    @staticmethod
    def _extract_links_from_markdown(markdown: str, text: str, base_url: str) -> List[Dict[str, Any]]:
        """从 markdown 和纯文本中提取可能的链接/文章列表"""
        results = []
        # 先用正则提取 markdown 链接 [text](url)
        import re
        md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', markdown)
        seen = set()
        for title, href in md_links:
            title = title.strip()
            if not title or len(title) < 6 or title in seen:
                continue
            # 过滤无意义导航
            skip_words = ["首页", "登录", "注册", "更多", "下一页", "上一页", "搜索", "返回"]
            if any(w in title for w in skip_words):
                continue
            seen.add(title)
            results.append({
                "title": title,
                "url": href if href.startswith("http") else urljoin(base_url, href),
                "content": "",
                "raw_markdown": ""
            })
            if len(results) >= 20:
                break
        return results

    @staticmethod
    async def crawl(source: Any, keyword: str, db: Any) -> List[Dict[str, Any]]:
        """
        根据数据源配置执行爬取。
        优先使用 playwright（渲染 JS 页面），fallback 到 requests。
        获取 markdown 后调用默认模型清洗。
        """
        url = CrawlerService.build_url(source.base_url, keyword, source.keyword_placeholder or "{keyword}")
        params = source.params or {}

        # 1. 获取页面内容
        page_data = None
        use_playwright = PLAYWRIGHT_AVAILABLE
        if use_playwright:
            try:
                page_data = await CrawlerService.crawl_with_playwright(url)
            except Exception as e:
                # fallback 到 requests
                try:
                    page_data = await CrawlerService.crawl_with_requests(url, params)
                except Exception as e2:
                    raise Exception(f"playwright 失败: {e}; requests 也失败: {e2}")
        else:
            page_data = await CrawlerService.crawl_with_requests(url, params)

        if not page_data:
            raise Exception("无法获取页面内容")

        # 2. 提取链接列表（如果是搜索结果页）
        items = CrawlerService._extract_links_from_markdown(
            page_data.get("markdown", ""),
            page_data.get("text", ""),
            url
        )

        # 如果没有提取到链接，将整个页面作为一个条目
        if not items:
            items = [{
                "title": page_data.get("title", ""),
                "url": url,
                "content": page_data.get("text", "")[:2000],
                "raw_markdown": page_data.get("markdown", "")
            }]

        # 3. 对每个条目，调用模型清洗整理
        results = []
        for item in items[:10]:  # 限制处理数量，避免模型调用过多
            raw_md = item.get("raw_markdown", "")
            title = item.get("title", "")
            # 如果没有单独的 markdown，用页面整体内容
            content_for_analysis = raw_md if raw_md else page_data.get("markdown", "")
            if not content_for_analysis:
                content_for_analysis = item.get("content", "")

            try:
                analyzed = await CrawlerService._analyze_with_model(db, title, content_for_analysis)
            except Exception:
                analyzed = {"summary": "", "keywords": [], "entities": {}}

            results.append({
                "title": title,
                "url": item.get("url", url),
                "content": item.get("content", ""),
                "markdown_content": content_for_analysis[:8000],  # 限制长度
                "summary": analyzed.get("summary", ""),
                "keywords": analyzed.get("keywords", []),
                "entities": analyzed.get("entities", {}),
                "source": "crawl"
            })

        return results
