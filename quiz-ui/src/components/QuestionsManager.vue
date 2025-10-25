<template>
  <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
  <QuestionDisplay :question="currentQuestion" @click-on-answer="answerClickedHandler" />
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import QuestionDisplay from "../components/QuestionDisplay.vue";
import QuizApiService from "@/services/QuizApiService";
import ParticipationStorageService from "@/services/ParticipationStorageService";

const router = useRouter();

const currentQuestionPosition = ref(1);
const totalNumberOfQuestion = ref(0);
const currentQuestion = ref(null);
const selectedAnswer = ref([]); // ids des choix sélectionnés

onMounted(async () => {
  const playerName = ParticipationStorageService.getPlayerName();
  if (!playerName) {
    router.push("/new-quiz");
    return;
  }

  const info = await QuizApiService.getQuizInfo();
  totalNumberOfQuestion.value = info.data.totalQuestions;

  await loadQuestionByPosition(currentQuestionPosition.value);
});

async function loadQuestionByPosition(pos) {
  const response = await QuizApiService.getQuestion(pos);
  if (response && response.data) {
    currentQuestion.value = response.data;
  } else {
    currentQuestion.value = null;
  }
}

async function answerClickedHandler(choiceId) {
  selectedAnswer.value.push(choiceId);

  if (currentQuestionPosition.value >= totalNumberOfQuestion.value) {
    await endQuiz();
  } else {
    currentQuestionPosition.value = currentQuestionPosition.value + 1;
    await loadQuestionByPosition(currentQuestionPosition.value);
  }
}

async function endQuiz() {
  const player = {
    playerName: ParticipationStorageService.getPlayerName(),
    answers: selectedAnswer.value,
  };

  const response = await QuizApiService.postParticipation(player);

    ParticipationStorageService.saveParticipationScore(response.data.score);

  router.push("/result");
}
</script>
