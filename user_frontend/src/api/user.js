import { get, post, put, del } from './request.js'

export const getUserMe = () => get('/user/me')
export const getUserDashboard = () => get('/user/dashboard')
export const getStaffList = () => get('/user/staff')
export const askStaffQuestion = (data) => post('/user/query/ask', data)

// 智能问数会话
export const createConversation = (data) => post('/user/query/conversation', data)
export const getConversationList = (params = {}) => get('/user/query/conversation/list' + (params.page ? `?page=${params.page}&page_size=${params.page_size || 50}` : ''))
export const getConversation = (id) => get(`/user/query/conversation/${id}`)
export const updateConversation = (id, data) => put(`/user/query/conversation/${id}`, data)
export const deleteConversation = (id) => del(`/user/query/conversation/${id}`)
