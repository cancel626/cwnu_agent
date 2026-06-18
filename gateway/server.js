const express = require('express')
const path = require('path')
const { createProxyMiddleware } = require('http-proxy-middleware')

const app = express()
const PORT = process.env.PORT || 3000

// API 代理：统一转发到后端
app.use('/api/v1', createProxyMiddleware({
  target: 'http://localhost:8000',
  changeOrigin: true,
  logLevel: 'debug'
}))

// 静态文件（登录页等）
app.use(express.static(path.join(__dirname, 'public')))

// Admin 前端静态文件 + SPA fallback
app.use('/admin', express.static(path.join(__dirname, '..', 'admin_frontend', 'dist')))
app.get('/admin/*', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'admin_frontend', 'dist', 'index.html'))
})

// User 前端静态文件 + SPA fallback
app.use('/user', express.static(path.join(__dirname, '..', 'user_frontend', 'dist')))
app.get('/user/*', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'user_frontend', 'dist', 'index.html'))
})

// Admin Design 登录页静态文件 + SPA fallback
app.use('/admin-login', express.static(path.join(__dirname, '..', 'admin_design', 'dist')))
app.get('/admin-login/*', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'admin_design', 'dist', 'index.html'))
})

// User Design 注册/登录页
app.use('/user-login', express.static(path.join(__dirname, '..', 'user_design')))
app.get('/user-login/*', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'user_design', 'index.html'))
})

// 登录入口页
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'))
})

app.listen(PORT, () => {
  console.log(`Gateway running at http://localhost:${PORT}`)
  console.log(`  Admin       -> http://localhost:${PORT}/admin/`)
  console.log(`  User        -> http://localhost:${PORT}/user/`)
  console.log(`  Admin Login -> http://localhost:${PORT}/admin-login/`)
  console.log(`  User Login  -> http://localhost:${PORT}/user-login/`)
})
