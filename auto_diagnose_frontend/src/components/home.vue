<template>
  <div class="min-h-screen w-full flex flex-col items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600 px-4 py-12">
    <div class="max-w-2xl w-full relative">
      <!-- Animated Background Shapes -->
      <div class="absolute inset-0 overflow-hidden pointer-events-none">
        <div 
          class="absolute -top-20 -right-20 w-96 h-96 bg-white/10 rounded-full blur-3xl animate-blob"
          style="animation-delay: 0.2s"
        ></div>
        <div 
          class="absolute -bottom-20 -left-20 w-96 h-96 bg-white/10 rounded-full blur-3xl animate-blob"
          style="animation-delay: 0.4s"
        ></div>
      </div>
      <!-- Main Content Card -->
      <div 
        class="relative bg-white/20 backdrop-blur-lg border border-white/20 rounded-2xl shadow-2xl p-10 text-center transform transition-all duration-500 hover:scale-[1.02]"
      >
        <div class="flex justify-center mb-6">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            class="h-20 w-20 text-white animate-pulse"
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path 
              stroke-linecap="round" 
              stroke-linejoin="round" 
              stroke-width="2" 
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </div>
        <h1 
          class="text-5xl font-extrabold mb-4 text-white"
        >
          Cybersecurity Diagnostic
        </h1>
        
        <p class="text-lg text-white mb-8 leading-relaxed">
          Conduct a comprehensive assessment of your organization's cybersecurity posture. Identify vulnerabilities, evaluate risk, and receive actionable insights.
        </p>
        
        <button
          @click="$router.push('/questions')"
          class="group relative w-full py-4 px-6 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-lg shadow-lg hover:shadow-xl transition duration-300 transform hover:-translate-y-1 active:scale-95"
        >
          <span class="flex items-center justify-center gap-3">
            Start Diagnostic
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              class="h-6 w-6 transition-transform group-hover:translate-x-1" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="2" 
                d="M13 7l5 5m0 0l-5 5m5-5H6"
              />
            </svg>
          </span>
        </button>
      </div>
      <!-- Footer -->
      <div class="mt-8 text-center text-white text-sm flex items-center justify-center gap-2">
        <span>Powered by</span>
        <span class="font-bold text-white">
          CCC-Network
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CybersecurityDiagnostic',
  methods: {
    startDiagnostic() {
      this.$router.push('/questions');
    }
  }
}
</script>

<style scoped>
/* Custom Animations */
@keyframes blob {
  0%, 100% { transform: scale(1) translate(0, 0); }
  50% { transform: scale(1.1) translate(10px, 20px); }
}
@keyframes gradient-x {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
.animate-blob {
  animation: blob 10s infinite ease-in-out;
}
</style>