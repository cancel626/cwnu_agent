from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
import httpx

from app.db.base import get_db
from app.models.model_config import ModelConfig
from app.schemas.model_config import (
    ModelConfigCreate, ModelConfigUpdate, ModelConfigInDB,
    ModelConfigResponse, ModelTestRequest
)
from app.api.v1.endpoints.admin import get_current_active_superuser

router = APIRouter()


def mask_api_key(key: str) -> str:
    if not key:
        return ""
    if len(key) <= 8:
        return "****"
    return key[:4] + "****" + key[-4:]


def model_to_dict(model: ModelConfig) -> dict:
    d = ModelConfigInDB.model_validate(model).model_dump(mode='json')
    d["api_key_masked"] = mask_api_key(model.api_key)
    return d


@router.get("/list", response_model=ModelConfigResponse, summary="模型配置列表")
def list_models(
    skip: int = 0,
    limit: int = 20,
    keyword: str = "",
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_active_superuser)
):
    query = db.query(ModelConfig)
    if keyword:
        query = query.filter(
            or_(
                ModelConfig.name.contains(keyword),
                ModelConfig.model_name.contains(keyword),
                ModelConfig.provider.contains(keyword)
            )
        )
    total = query.count()
    models = query.offset(skip).limit(limit).all()
    return ModelConfigResponse(
        code=200,
        message="success",
        data={
            "total": total,
            "items": [model_to_dict(m) for m in models]
        }
    )


@router.get("/default", response_model=ModelConfigResponse, summary="获取默认模型")
def get_default_model(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_active_superuser)
):
    model = db.query(ModelConfig).filter(ModelConfig.is_default == True).first()
    if not model:
        raise HTTPException(status_code=404, detail="未设置默认模型")
    return ModelConfigResponse(code=200, message="success", data=model_to_dict(model))


@router.post("/create", response_model=ModelConfigResponse, summary="创建模型配置")
def create_model(
    data: ModelConfigCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_active_superuser)
):
    if data.is_default:
        db.query(ModelConfig).update({ModelConfig.is_default: False})
        db.commit()

    model = ModelConfig(**data.model_dump())
    db.add(model)
    db.commit()
    db.refresh(model)
    return ModelConfigResponse(code=200, message="创建成功", data=model_to_dict(model))


@router.put("/{model_id}", response_model=ModelConfigResponse, summary="更新模型配置")
def update_model(
    model_id: int,
    data: ModelConfigUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_active_superuser)
):
    model = db.query(ModelConfig).filter(ModelConfig.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")

    update_data = data.model_dump(exclude_unset=True)

    if update_data.get("is_default"):
        db.query(ModelConfig).update({ModelConfig.is_default: False})
        db.commit()

    for field, value in update_data.items():
        setattr(model, field, value)
    db.commit()
    db.refresh(model)
    return ModelConfigResponse(code=200, message="更新成功", data=model_to_dict(model))


@router.delete("/{model_id}", response_model=ModelConfigResponse, summary="删除模型配置")
def delete_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_active_superuser)
):
    model = db.query(ModelConfig).filter(ModelConfig.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
    db.delete(model)
    db.commit()
    return ModelConfigResponse(code=200, message="删除成功")


@router.post("/{model_id}/set-default", response_model=ModelConfigResponse, summary="设为默认模型")
def set_default_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_active_superuser)
):
    model = db.query(ModelConfig).filter(ModelConfig.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")

    db.query(ModelConfig).update({ModelConfig.is_default: False})
    db.commit()

    model.is_default = True
    db.commit()
    db.refresh(model)
    return ModelConfigResponse(code=200, message="设置成功", data=model_to_dict(model))


@router.post("/{model_id}/test", response_model=ModelConfigResponse, summary="测试模型连通性")
async def test_model(
    model_id: int,
    req: ModelTestRequest,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_active_superuser)
):
    model = db.query(ModelConfig).filter(ModelConfig.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")

    url = f"{model.api_base.rstrip('/')}/chat/completions"
    payload = {
        "model": model.model_name,
        "messages": [{"role": "user", "content": req.message}],
        "stream": False,
        "temperature": model.temperature or 0.7
    }
    # 部分第三方中转不支持很小的 max_tokens，尝试加入但失败时不强制
    try:
        async with httpx.AsyncClient(timeout=model.timeout or 30, follow_redirects=True) as client:
            resp = await client.post(
                url,
                headers={
                    "Authorization": f"Bearer {model.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            if resp.status_code == 200:
                raw_text = resp.text
                result = {}
                # 兼容部分第三方返回 SSE 流格式（每行 data: {...}）
                if raw_text.strip().startswith("data:"):
                    lines = raw_text.strip().split("\n")
                    for line in lines:
                        line = line.strip()
                        if line.startswith("data:"):
                            json_str = line[5:].strip()
                            if json_str == "[DONE]":
                                continue
                            try:
                                chunk = __import__("json").loads(json_str)
                                delta = chunk.get("choices", [{}])[0].get("delta", {})
                                if delta.get("content"):
                                    result.setdefault("_sse_content", "")
                                    result["_sse_content"] += delta["content"]
                                result = chunk
                            except Exception:
                                pass
                    content = result.get("_sse_content", "")
                    if not content:
                        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                else:
                    try:
                        result = resp.json()
                    except Exception:
                        result = {"_raw_text": raw_text}
                    # 尝试多种格式解析回复内容
                    content = ""
                    try:
                        choices = result.get("choices", [])
                        if choices and isinstance(choices, list):
                            msg = choices[0].get("message", {})
                            if msg:
                                content = msg.get("content", "")
                            else:
                                # 某些中转格式为 choices[0].text
                                content = choices[0].get("text", "")
                        else:
                            # 兜底：直接取 result 里的 content
                            content = result.get("content", "")
                    except Exception:
                        content = ""

                return ModelConfigResponse(
                    code=200,
                    message="测试成功",
                    data={
                        "status": "ok",
                        "response": content or "（收到空回复，但连接正常）",
                        "raw": result,
                        "model": model.model_name
                    }
                )
            else:
                detail = resp.text
                try:
                    err_json = resp.json()
                    detail = err_json.get("error", {}).get("message", resp.text)
                except Exception:
                    pass
                return ModelConfigResponse(
                    code=200,
                    message=f"模型返回错误: HTTP {resp.status_code}",
                    data={
                        "status": "error",
                        "http_code": resp.status_code,
                        "detail": detail,
                        "request_url": url,
                        "request_model": model.model_name
                    }
                )
    except httpx.TimeoutException:
        return ModelConfigResponse(
            code=200,
            message="测试超时，请检查网络或增大超时时间",
            data={"status": "timeout", "request_url": url}
        )
    except Exception as e:
        return ModelConfigResponse(
            code=200,
            message=f"测试失败: {str(e)}",
            data={"status": "error", "detail": str(e), "request_url": url}
        )
