import { get, post, del, upload } from './request.js'

// 好友管理
export const addFriend = (username) => post('/chat/friend/request', { username })
export const getFriendList = () => get('/chat/friend/list')
export const deleteFriend = (friendId) => del(`/chat/friend/${friendId}`)

// 群聊管理
export const createGroup = (data) => post('/chat/group', data)
export const getGroupList = () => get('/chat/group/list')
export const getGroupMembers = (groupId) => get(`/chat/group/${groupId}/members`)
export const inviteMember = (groupId, data) => post(`/chat/group/${groupId}/invite`, data)

// 消息
export const getPrivateHistory = (friendId) => get(`/chat/message/private/${friendId}`)
export const getGroupHistory = (groupId) => get(`/chat/message/group/${groupId}`)
export const sendMessage = (data) => post('/chat/message/send', data)
export const uploadChatFile = (file) => upload('/chat/upload', file)

// 数字员工列表（用于邀请）
export const getStaffList = () => get('/user/staff')
