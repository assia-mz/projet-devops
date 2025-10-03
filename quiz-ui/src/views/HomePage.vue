<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';

onMounted(async () => {
  console.log('Home page mounted');
  registeredScores.value = await quizApiService.getRegisteredScores();
});

const registeredScores = ref([]);
</script>

<style></style>

<template>
  <h1>Home page</h1>
  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>
  <router-link to="/new-quiz">Démarrer le quiz !</router-link>
</template>
