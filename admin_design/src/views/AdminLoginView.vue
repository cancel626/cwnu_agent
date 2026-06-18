<template>
  <div class="min-h-screen cyber-grid relative overflow-hidden flex items-center justify-center">
    <!-- Background Particles -->
    <div class="fixed inset-0 pointer-events-none z-0" ref="matrixRef"></div>

    <!-- Main Container -->
    <div class="relative z-10 w-full max-w-6xl px-8 flex flex-col md:flex-row items-center gap-16">
      <!-- Left Side: Branding/Title -->
      <div class="flex-1 text-left hidden lg:block">
        <div class="inline-block mb-6 border-b-2 border-cyber-cyan pb-2">
          <span class="font-label-md text-cyber-magenta text-xs uppercase tracking-[0.3em]">系统正在初始化...</span>
        </div>
        <h1 class="font-headline-lg text-cyber-cyan glitch-text text-[64px] font-bold leading-none tracking-tighter mb-4">
          西华师范<br/>数智瞭望系统
        </h1>
        <div class="flex items-center gap-4 mt-6">
          <div class="w-20 h-[2px] bg-cyber-magenta"></div>
          <p class="font-label-md text-cyber-cyan/60 text-sm uppercase tracking-widest">管理控制台 V2.0.4</p>
        </div>
        <div class="mt-12 grid grid-cols-2 gap-8 opacity-40">
          <div class="border-l-2 border-cyber-cyan/30 pl-4">
            <div class="text-[10px] font-label-md text-cyber-cyan uppercase">系统负载</div>
            <div class="text-xl font-label-md text-white">0.42ms</div>
          </div>
          <div class="border-l-2 border-cyber-cyan/30 pl-4">
            <div class="text-[10px] font-label-md text-cyber-cyan uppercase">活动节点</div>
            <div class="text-xl font-label-md text-white">128 / 128</div>
          </div>
        </div>
      </div>

      <!-- Right Side: Login Card -->
      <main class="w-full max-w-md">
        <!-- Mobile Header -->
        <div class="lg:hidden text-center mb-10">
          <h1 class="font-headline-lg-mobile text-cyber-cyan glitch-text text-[32px] font-bold leading-tight">
            西华师范数智瞭望系统
          </h1>
          <p class="font-label-md text-cyber-cyan/60 text-[10px] uppercase mt-2">管理控制台 V2.0.4</p>
        </div>

        <div class="cyber-card p-10 relative" :class="{ 'animate-pulse': isError }">
          <!-- Decorative Corners -->
          <div class="pixel-corner corner-tl"></div>
          <div class="pixel-corner corner-tr"></div>
          <div class="pixel-corner corner-bl"></div>
          <div class="pixel-corner corner-br"></div>

          <!-- Logo Area -->
          <div class="flex justify-center mb-10">
            <div class="relative group">
              <div class="absolute inset-0 bg-cyber-cyan/30 blur-2xl rounded-full scale-150 opacity-50 group-hover:opacity-100 transition-opacity"></div>
              <div class="w-24 h-24 border-2 border-dashed border-cyber-cyan flex items-center justify-center p-5 relative bg-cyber-bg/80 backdrop-blur-md">
                <img alt="Logo" class="w-full h-full object-contain filter brightness-125" src="https://lh3.googleusercontent.com/aida/AP1WRLuJqDJhokwYPVDNccTmCNReLCychohGVYddZwIOyriyZ-TtZ7zsqpBFGuOS-xqsbRhq-DgRz4qPKCxtDIeQoYhO6IHgHHqE8aEGhSqgCHr1VLtaF9t4yTgzoEytZDQQYiMst6slgAhdeb8RZsd0YyMSkte-ImnrnI3Snwse0B-cUYK5IeGpEb9CoSU1huFyjqKR2FyhP6n63_tvAJHIX0GsIHuH9Ae0L02DFpGLxY4Y0JmSFxlTOpNBq2JN"/>
                <div class="absolute left-0 top-0 w-full h-[2px] bg-cyber-cyan shadow-[0_0_15px_#00f2ff] animate-[scan_3s_infinite_alternate] z-20"></div>
              </div>
            </div>
          </div>

          <div class="text-center mb-10">
            <h2 class="font-headline-sm text-white text-xl tracking-[0.2em] uppercase">管理员登录</h2>
            <div class="w-16 h-1 bg-cyber-magenta mx-auto mt-3"></div>
          </div>

          <!-- Form -->
          <form class="space-y-6" @submit.prevent="handleLogin">
            <div class="space-y-2">
              <label class="font-label-md text-[11px] text-cyber-cyan/80 block uppercase ml-1 tracking-wider">账号</label>
              <div class="flex items-center cyber-input rounded-none px-4 py-4">
                <span class="material-symbols-outlined text-cyber-cyan text-[22px] mr-4">account_circle</span>
                <input v-model="username" class="w-full bg-transparent border-none outline-none focus:ring-0 font-label-md text-white placeholder:text-cyber-cyan/20 text-sm" placeholder="请输入管理员账号" required type="text"/>
              </div>
            </div>

            <div class="space-y-2">
              <label class="font-label-md text-[11px] text-cyber-cyan/80 block uppercase ml-1 tracking-wider">密码</label>
              <div class="flex items-center cyber-input rounded-none px-4 py-4">
                <span class="material-symbols-outlined text-cyber-cyan text-[22px] mr-4">key</span>
                <input v-model="password" :type="showPassword ? 'text' : 'password'" class="w-full bg-transparent border-none outline-none focus:ring-0 font-label-md text-white placeholder:text-cyber-cyan/20 text-sm" placeholder="请输入密码" required/>
                <button type="button" class="ml-2 text-cyber-cyan/40 hover:text-cyber-cyan transition-colors" @click="togglePassword">
                  <span class="material-symbols-outlined text-[22px]">{{ showPassword ? 'visibility_off' : 'visibility' }}</span>
                </button>
              </div>
            </div>

            <!-- Utilities -->
            <div class="flex items-center justify-between pt-2">
              <label class="flex items-center cursor-pointer group">
                <div class="relative flex items-center">
                  <input v-model="rememberMe" class="peer hidden" type="checkbox"/>
                  <div class="w-5 h-5 border border-cyber-cyan/40 peer-checked:bg-cyber-cyan peer-checked:border-cyber-cyan transition-all flex items-center justify-center">
                    <span class="material-symbols-outlined text-cyber-bg text-[14px] font-bold hidden peer-checked:block">check</span>
                  </div>
                </div>
                <span class="ml-3 font-label-md text-[11px] text-cyber-cyan/60 group-hover:text-cyber-cyan transition-colors uppercase tracking-widest">记住我</span>
              </label>
              <a class="font-label-md text-[11px] text-cyber-cyan/60 hover:text-cyber-magenta transition-colors border-b border-transparent hover:border-cyber-magenta uppercase tracking-widest" href="#">找回密码</a>
            </div>

            <!-- Feedback Area -->
            <div v-if="isError" class="text-cyber-magenta font-label-md text-[12px] flex items-center justify-center gap-3 border border-cyber-magenta/40 bg-cyber-magenta/10 py-3">
              <span class="material-symbols-outlined text-[18px]">warning</span>
              <span>认证失败: 账号或密码错误</span>
            </div>
            <div v-if="isSuccess" class="text-cyber-cyan font-label-md text-[12px] flex items-center justify-center gap-3 border border-cyber-cyan/40 bg-cyber-cyan/10 py-3">
              <span class="material-symbols-outlined text-[18px]">terminal</span>
              <span>会话开始: 正在进入系统...</span>
            </div>

            <!-- Submit Button -->
            <button :disabled="isLoading" class="pixel-btn w-full py-5 text-white font-headline-sm text-lg flex items-center justify-center space-x-3 relative mt-4" type="submit">
              <span v-if="!isLoading" class="relative z-10">执行登录</span>
              <span v-else class="w-6 h-6 border-3 border-white/30 border-t-white rounded-full animate-spin relative z-10"></span>
            </button>
          </form>

          <!-- HUD Details -->
          <div class="mt-10 flex justify-between items-end opacity-40">
            <div class="flex gap-1.5 pb-1">
              <div class="w-1 h-4 bg-cyber-cyan"></div>
              <div class="w-1 h-4 bg-cyber-cyan"></div>
              <div class="w-1 h-4 bg-cyber-cyan"></div>
            </div>
            <div class="text-right">
              <div class="font-label-md text-[9px] text-cyber-cyan/80 uppercase mb-1">系统环境</div>
              <div class="font-label-md text-[10px] text-cyber-cyan">节点 ID: CWNU-SERVER-04</div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <footer class="mt-12 text-center opacity-40">
          <p class="font-label-md text-[11px] text-cyber-cyan uppercase tracking-[0.15em]">
            &copy; 2026 西华师范大学 / 数据加密 256-BIT
          </p>
        </footer>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const rememberMe = ref(false)
const isLoading = ref(false)
const isError = ref(false)
const isSuccess = ref(false)
const matrixRef = ref(null)

function togglePassword() {
  showPassword.value = !showPassword.value
}

function createMatrix() {
  const container = matrixRef.value
  if (!container) return
  const count = 45
  for (let i = 0; i < count; i++) {
    const stream = document.createElement('div')
    stream.className = 'data-stream'
    stream.style.left = Math.random() * 100 + 'vw'
    stream.style.animationDuration = (Math.random() * 3 + 2) + 's'
    stream.style.animationDelay = Math.random() * 5 + 's'
    container.appendChild(stream)
  }
}

async function handleLogin() {
  isError.value = false
  isSuccess.value = false
  isLoading.value = true

  try {
    const res = await fetch('http://localhost:8000/api/v1/admin/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })
    const result = await res.json()

    isLoading.value = false

    if (!res.ok || result.code !== 200) {
      isError.value = true
      return
    }

    isSuccess.value = true
    // 保存 token
    localStorage.setItem('admin_token', result.data.access_token)
    localStorage.setItem('admin_info', JSON.stringify(result.data.admin))

    // 登录成功后跳转到管理后台
    setTimeout(() => {
      window.location.href = '/admin/'
    }, 1500)
  } catch (err) {
    isLoading.value = false
    isError.value = true
    console.error('登录请求失败:', err)
  }
}

onMounted(() => {
  createMatrix()
})
</script>

<style scoped>
.cyber-grid {
  background-image:
    linear-gradient(rgba(0, 242, 255, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 242, 255, 0.05) 1px, transparent 1px);
  background-size: 30px 30px;
  background-color: #0a0a2e;
}

.glitch-text {
  position: relative;
  text-shadow: 0.05em 0 0 #ff00ff, -0.05em -0.025em 0 #00f2ff;
  animation: glitch 2s infinite;
}

@keyframes glitch {
  0% { text-shadow: 0.05em 0 0 #ff00ff, -0.05em -0.025em 0 #00f2ff; }
  14% { text-shadow: 0.05em 0 0 #ff00ff, -0.05em -0.025em 0 #00f2ff; }
  15% { text-shadow: -0.05em -0.025em 0 #ff00ff, 0.025em 0.025em 0 #00f2ff; }
  49% { text-shadow: -0.05em -0.025em 0 #ff00ff, 0.025em 0.025em 0 #00f2ff; }
  50% { text-shadow: 0.025em 0.05em 0 #ff00ff, 0.05em 0 0 #00f2ff; }
  99% { text-shadow: 0.025em 0.05em 0 #ff00ff, 0.05em 0 0 #00f2ff; }
  100% { text-shadow: -0.025em 0 0 #ff00ff, -0.025em -0.025em 0 #00f2ff; }
}

.cyber-card {
  background: rgba(10, 10, 46, 0.7);
  backdrop-filter: blur(25px);
  border: 2px solid #00f2ff;
  box-shadow: 0 0 30px rgba(0, 242, 255, 0.2), inset 0 0 20px rgba(0, 242, 255, 0.1);
  clip-path: polygon(0 0, 100% 0, 100% calc(100% - 30px), calc(100% - 30px) 100%, 0 100%);
}

.cyber-input {
  background: rgba(0, 242, 255, 0.03);
  border: 1px solid rgba(0, 242, 255, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.cyber-input:focus-within {
  border-color: #00f2ff;
  box-shadow: 0 0 12px rgba(0, 242, 255, 0.3);
  background: rgba(0, 242, 255, 0.08);
}

.pixel-btn {
  background: #ff00ff;
  color: white;
  text-transform: uppercase;
  letter-spacing: 3px;
  position: relative;
  overflow: hidden;
  border: none;
  clip-path: polygon(8% 0, 100% 0, 100% 70%, 92% 100%, 0 100%, 0 30%);
  transition: all 0.2s ease;
}

.pixel-btn:hover:not(:disabled) {
  transform: scale(1.02);
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.5);
}

.pixel-btn::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  animation: scan 2.5s infinite;
}

@keyframes scan {
  0% { left: -100%; }
  100% { left: 100%; }
}

.data-stream {
  position: absolute;
  width: 1px;
  height: 150px;
  background: linear-gradient(to bottom, transparent, #00f2ff, transparent);
  animation: drop 4s infinite linear;
  opacity: 0.3;
}

@keyframes drop {
  0% { transform: translateY(-300px); opacity: 0; }
  20% { opacity: 0.6; }
  80% { opacity: 0.6; }
  100% { transform: translateY(110vh); opacity: 0; }
}

.pixel-corner {
  position: absolute;
  width: 12px;
  height: 12px;
  border-style: solid;
  border-color: #ff00ff;
  z-index: 20;
}

.corner-tl { top: -3px; left: -3px; border-width: 3px 0 0 3px; }
.corner-tr { top: -3px; right: -3px; border-width: 3px 3px 0 0; }
.corner-bl { bottom: -3px; left: -3px; border-width: 0 0 3px 3px; }
.corner-br { bottom: -3px; right: -3px; border-width: 0 3px 3px 0; }
</style>
