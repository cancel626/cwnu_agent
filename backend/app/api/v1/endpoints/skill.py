from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
import httpx
import json

from app.db.base import get_db
from app.models.skill import Skill
from app.models.model_config import ModelConfig
from app.schemas.skill import SkillCreate, SkillUpdate, SkillInDB, SkillResponse, SkillAIGenerateRequest, StaffSystemPromptRequest
from app.api.v1.endpoints.admin import get_current_admin

router = APIRouter()


def get_default_model_config(db: Session):
    return db.query(ModelConfig).filter(ModelConfig.is_default == True, ModelConfig.is_active == True).first()


async def call_default_model(db: Session, messages: list, temperature: float = 0.7):
    model = get_default_model_config(db)
    if not model:
        raise HTTPException(status_code=500, detail="未设置默认模型")
    async with httpx.AsyncClient(timeout=model.timeout or 60) as client:
        resp = await client.post(
            f"{model.api_base.rstrip('/')}/chat/completions",
            headers={
                "Authorization": f"Bearer {model.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model.model_name,
                "messages": messages,
                "temperature": temperature,
                "stream": False
            }
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail=f"模型调用失败: {resp.text}")
        result = resp.json()
        content = ""
        try:
            choices = result.get("choices", [])
            if choices:
                msg = choices[0].get("message", {})
                content = msg.get("content", "")
            else:
                content = result.get("content", "")
        except Exception:
            pass
        return content


@router.get("/list", response_model=SkillResponse, summary="技能列表")
def skill_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    keyword: str = Query(""),
    skill_type: str = Query(""),
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    query = db.query(Skill)
    if keyword:
        query = query.filter(or_(Skill.name.contains(keyword), Skill.description.contains(keyword)))
    if skill_type:
        query = query.filter(Skill.type == skill_type)
    total = query.count()
    items = query.order_by(Skill.created_at.desc()).offset(skip).limit(limit).all()
    return SkillResponse(code=200, message="success", data={"total": total, "items": [SkillInDB.model_validate(i).model_dump(mode='json') for i in items]})


@router.get("/{skill_id}", response_model=SkillResponse, summary="技能详情")
def skill_detail(
    skill_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    item = db.query(Skill).filter(Skill.id == skill_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="技能不存在")
    return SkillResponse(code=200, message="success", data=SkillInDB.model_validate(item).model_dump(mode='json'))


@router.post("/create", response_model=SkillResponse, summary="创建技能")
def skill_create(
    data: SkillCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    item = Skill(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return SkillResponse(code=200, message="创建成功", data=SkillInDB.model_validate(item).model_dump(mode='json'))


@router.put("/{skill_id}", response_model=SkillResponse, summary="更新技能")
def skill_update(
    skill_id: int,
    data: SkillUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    item = db.query(Skill).filter(Skill.id == skill_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="技能不存在")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return SkillResponse(code=200, message="更新成功", data=SkillInDB.model_validate(item).model_dump(mode='json'))


@router.delete("/{skill_id}", response_model=SkillResponse, summary="删除技能")
def skill_delete(
    skill_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    item = db.query(Skill).filter(Skill.id == skill_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="技能不存在")
    db.delete(item)
    db.commit()
    return SkillResponse(code=200, message="删除成功")


@router.post("/ai-generate", response_model=SkillResponse, summary="AI生成技能参数")
async def skill_ai_generate(
    req: SkillAIGenerateRequest,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    type_desc = {
        "functioncall": "Python函数，在沙箱中执行",
        "mcp": "MCP服务调用",
        "skill": "skill.md描述文件"
    }
    prompt = f"""请根据以下描述，生成一个{type_desc.get(req.skill_type, req.skill_type)}技能的配置参数。

用户描述：{req.description}
技能类型：{req.skill_type}

请严格按照以下JSON格式输出，不要包含任何其他文字：
{{
  "name": "技能名称",
  "description": "技能功能描述",
  "config": {{}},
  "content": ""
}}

其中：
- config 根据类型填写所需参数
- content 填写对应类型的内容代码或文档

对于 functioncall 类型，config 示例：{{"function_name":"calculate","params":[{{"name":"a","type":"int","desc":"第一个数"}}],"timeout":30}}，content 填写 Python 函数实现代码。
对于 mcp 类型，config 示例：{{"server_url":"http://localhost:8000/sse","tool_name":"search"}}，content 可留空或填写额外配置。
对于 skill 类型，config 示例：{{"category":"数据处理"}}，content 填写 skill.md 格式的文档内容。
"""

    try:
        content = await call_default_model(db, [{"role": "user", "content": prompt}], temperature=0.3)
        # 提取 JSON
        json_str = content.strip()
        if json_str.startswith("```json"):
            json_str = json_str[7:]
        if json_str.startswith("```"):
            json_str = json_str[3:]
        if json_str.endswith("```"):
            json_str = json_str[:-3]
        json_str = json_str.strip()
        result = json.loads(json_str)
        return SkillResponse(code=200, message="生成成功", data=result)
    except Exception as e:
        return SkillResponse(code=500, message=f"生成失败: {str(e)}", data={"raw": content if 'content' in dir() else ""})


@router.post("/generate-system-prompt", response_model=SkillResponse, summary="根据技能生成系统提示词")
async def generate_system_prompt(
    req: StaffSystemPromptRequest,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    skills_info = ""
    if req.skill_ids:
        skills = db.query(Skill).filter(Skill.id.in_(req.skill_ids)).all()
        for s in skills:
            skills_info += f"- 技能名称: {s.name}\n  类型: {s.type}\n  描述: {s.description or '无'}\n"

    prompt = f"""请根据以下技能信息，生成一段专业的系统提示词（System Prompt），用于配置一个数字员工（AI Agent）。

{skills_info}

额外描述：{req.extra_desc or '无'}

要求：
1. 用中文输出
2. 明确数字员工的职责和工作方式
3. 提及需要使用的技能
4. 语气专业、清晰
5. 直接输出提示词内容，不要包含任何解释性文字
"""

    try:
        content = await call_default_model(db, [{"role": "user", "content": prompt}], temperature=0.5)
        return SkillResponse(code=200, message="生成成功", data={"system_prompt": content.strip()})
    except Exception as e:
        return SkillResponse(code=500, message=f"生成失败: {str(e)}")
