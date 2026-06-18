from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, ForeignKey, Index
from sqlalchemy.sql import func
from app.db.base import Base


class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    friend_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="好友ID")
    status = Column(String(20), default="accepted", comment="状态: pending/accepted/rejected")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    __table_args__ = (
        Index("idx_friendship_pair", "user_id", "friend_id", unique=True),
    )


class ChatGroup(Base):
    __tablename__ = "chat_groups"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="群名称")
    desc = Column(Text, nullable=True, comment="群描述")
    avatar = Column(String(255), nullable=True, comment="群头像")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="群主ID")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")


class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("chat_groups.id"), nullable=False, comment="群ID")
    member_type = Column(String(20), nullable=False, comment="成员类型: user/staff")
    member_id = Column(Integer, nullable=False, comment="成员ID(用户ID或数字员工ID)")
    nickname_in_group = Column(String(50), nullable=True, comment="群内昵称")
    joined_at = Column(DateTime, server_default=func.now(), comment="加入时间")

    __table_args__ = (
        Index("idx_group_member", "group_id", "member_type", "member_id", unique=True),
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    msg_type = Column(String(20), default="text", comment="消息类型: text/image/file/system")
    sender_type = Column(String(20), default="user", comment="发送者类型: user/staff/system")
    sender_id = Column(Integer, nullable=False, comment="发送者ID")
    receiver_id = Column(Integer, nullable=True, comment="接收者ID(私聊)")
    group_id = Column(Integer, ForeignKey("chat_groups.id"), nullable=True, comment="群ID(群聊)")
    content = Column(Text, nullable=False, comment="消息内容")
    at_staff_ids = Column(String(255), nullable=True, comment="@的数字员工ID列表,逗号分隔")
    is_read = Column(Boolean, default=False, comment="是否已读")
    # 内容安全审核结果
    is_scanned = Column(Boolean, default=False, comment="是否已被大模型扫描过")
    audit_status = Column(String(20), default="pending", comment="审核状态: pending/pass/rejected")
    audit_result = Column(JSON, default=dict, comment="审核结果JSON: {is_violation, type, reason, confidence}")
    audited_at = Column(DateTime, nullable=True, comment="审核时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

    __table_args__ = (
        Index("idx_msg_group", "group_id", "created_at"),
        Index("idx_msg_private", "sender_id", "receiver_id", "created_at"),
    )


class QueryConversation(Base):
    __tablename__ = "query_conversations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    staff_id = Column(Integer, ForeignKey("digital_staff.id"), nullable=True, comment="当前会话绑定的数字员工ID")
    title = Column(String(200), nullable=False, comment="会话标题")
    messages = Column(JSON, default=list, comment="会话消息列表JSON")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    __table_args__ = (
        Index("idx_query_conv_user", "user_id", "updated_at"),
    )
