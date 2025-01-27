<template>
  <div class="min-h-screen w-full flex flex-col items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600 text-white p-4">
    <!-- Navigation -->
    <nav class="absolute top-6 left-6 w-full max-w-2xl">
      <button
        @click="$router.push('/')"
        class="flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg shadow-lg transition-colors"
        aria-label="Back to Home"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        Home
      </button>
    </nav>

    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col items-center justify-center space-y-4">
      <div class="animate-spin rounded-full h-12 w-12 border-t-4 border-white"></div>
      <p class="text-xl">Loading diagnostic questions...</p>
    </div>

    <!-- Questions Section -->
    <div
      v-else-if="currentQuestionIndex < questions.length"
      class="w-full max-w-2xl bg-white/10 backdrop-blur-lg rounded-xl shadow-2xl text-white p-8 border border-white/20 animate-fade-in"
    >
      <div class="mb-6">
        <h2 class="text-2xl font-bold mb-2 text-blue-200">
          Question {{ currentQuestionIndex + 1 }} of {{ questions.length }}
        </h2>
        <div class="h-1 w-full bg-gray-700 rounded-full overflow-hidden">
          <div
            class="h-full bg-blue-500 transition-all duration-300"
            :style="{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }"
          ></div>
        </div>
      </div>

      <p class="text-lg mb-6 text-gray-100">{{ questions[currentQuestionIndex].text }}</p>

      <!-- Options -->
      <div class="space-y-4">
        <button
          v-for="(option, index) in questions[currentQuestionIndex].options"
          :key="index"
          @click="selectAnswer(option.text)"
          :class="[
            'block w-full text-left px-4 py-3 rounded-lg border-2 transition-all duration-300',
            selectedAnswers[currentQuestionIndex] === option.text
              ? 'bg-blue-600 border-blue-400 text-white ring-2 ring-blue-300'
              : 'bg-white/10 border-white/20 hover:bg-white/20 hover:border-white/40'
          ]"
        >
          {{ option.text }}
        </button>
      </div>

      <!-- Navigation Buttons -->
      <div class="flex justify-between items-center mt-8">
        <button
          v-if="currentQuestionIndex > 0"
          @click="prevQuestion"
          class="flex items-center gap-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-white transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 17l-5-5m0 0l5-5m-5 5h18" />
          </svg>
          Previous
        </button>

        <div class="flex gap-4">
          <button
            v-if="currentQuestionIndex < questions.length - 1"
            @click="nextQuestion"
            class="flex items-center gap-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg text-white transition-colors"
            :disabled="!selectedAnswers[currentQuestionIndex]"
          >
            Next
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </button>

          <button
            v-if="currentQuestionIndex === questions.length - 1"
            @click="submitAnswers"
            class="flex items-center gap-2 px-4 py-2 bg-green-500 hover:bg-green-600 rounded-lg text-white transition-colors"
            :disabled="!selectedAnswers[currentQuestionIndex]"
          >
            Submit
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Results Section -->
    <div v-else class="text-center max-w-2xl w-full animate-fade-in">
      <div class="bg-white/10 backdrop-blur-lg rounded-xl p-8 border border-white/20 shadow-2xl">
        <h2 class="text-3xl font-bold mb-4 text-blue-200">Diagnostic Results</h2>

        <!-- Overall Percentage -->
        <div class="text-5xl font-bold text-blue-300 mb-6">
          {{ percentageScore ? `${percentageScore}%` : '--' }}
        </div>

        <!-- Category Breakdown -->
        <h3 class="text-2xl font-semibold mb-4 text-blue-100">Category Breakdown</h3>
        <ul class="text-left text-lg text-gray-100 space-y-2">
          <li
            v-for="(categoryScore, category) in categoryScores"
            :key="category"
            class="flex justify-between"
          >
            <span>{{ category }}</span>
            <span>{{ categoryScore }}/{{ categoryMaxScores[category] }}</span>
          </li>
        </ul>

        <!-- Recommendations -->
        <p class="text-lg mt-6 text-gray-100">{{ recommendations }}</p>

        <!-- Restart Button -->
        <button
          @click="restart"
          class="px-6 py-3 bg-blue-500 hover:bg-blue-600 rounded-lg text-white flex items-center gap-2 mx-auto transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Restart Diagnostic
        </button>

        <button
          @click="generatePDF"
          class="px-6 py-3 bg-purple-500 hover:bg-purple-600 rounded-lg text-white flex items-center gap-2 mx-auto transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 9l-7 7-7-7"
            />
          </svg>
          Download PDF
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CyberDiagnostic",
  data() {
    return {
      questions: [],
      currentQuestionIndex: 0,
      selectedAnswers: {},
      loading: true,
      percentageScore: null,
      recommendations: "",
      categoryScores: {},
      categoryMaxScores: {},
    };
  },
  methods: {
    async generatePDF() {
      try {
          const payload = {
              answers: Object.values(this.selectedAnswers), // Convert answers to array
              category_scores: this.categoryScores, // Scores per category
              category_max_scores: this.categoryMaxScores, // Max scores per category
              recommendations: this.recommendations, // Recommendations
          };

          const response = await axios.post(
              "http://127.0.0.1:5000/api/generate-pdf",
              payload,
              { responseType: "blob" } // Ensures response is treated as a file
          );

          // Create a downloadable link for the PDF
          const blob = new Blob([response.data], { type: "application/pdf" });
          const link = document.createElement("a");
          link.href = window.URL.createObjectURL(blob);
          link.download = "diagnostic_report.pdf";
          link.click();
      } catch (error) {
          console.error("Error generating PDF:", error.response?.data || error.message);
      }
    },
    async fetchQuestions() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/questions");
        this.questions = response.data;
        this.loading = false;
      } catch (error) {
        console.error("Error fetching questions:", error);
        this.loading = false;
      }
    },
    selectAnswer(answer) {
      this.selectedAnswers[this.currentQuestionIndex] = answer;
    },
    prevQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--;
      }
    },
    nextQuestion() {
      if (
        this.currentQuestionIndex < this.questions.length - 1 &&
        this.selectedAnswers[this.currentQuestionIndex]
      ) {
        this.currentQuestionIndex++;
      }
    },
    async submitAnswers() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/api/submit", {
          answers: Object.values(this.selectedAnswers),
        });
        this.percentageScore = response.data.percentage_score || 0;
        this.categoryScores = response.data.category_scores;
        this.categoryMaxScores = response.data.category_max_scores;
        this.recommendations = response.data.recommendations;
        this.currentQuestionIndex++;
      } catch (error) {
        console.error("Error submitting answers:", error);
      }
    },
    restart() {
      this.currentQuestionIndex = 0;
      this.selectedAnswers = {};
      this.percentageScore = null;
      this.recommendations = "";
      this.categoryScores = {};
    },
  },
  created() {
    this.fetchQuestions();
  },
};
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.animate-fade-in {
  animation: fade-in 0.5s ease-out;
}
</style>
