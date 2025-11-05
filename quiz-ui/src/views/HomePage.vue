<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';

onMounted(async () => {
  console.log('Home page mounted');
  registeredScores.value = await quizApiService.getRegisteredScores();
});

const registeredScores = ref([]);
</script>

<template>
  <div class="wrapper double">
    <div class="launch-quiz">
      <h1 class="launch-title">Testez vos connaissances</h1>
      <router-link to="/new-quiz" class="button launch-btn">Démarrer le quiz !</router-link>
    </div>
    <div>
      <img src="../assets/fonds/t-rex.jpg" class="quiz-img"></img>
    </div>
  </div>
  <div class="wrapper double scoreboard">
    <div>
      <h1 class="launch-title">Tableau des scores général</h1>
      <div class="wrapper triple classement">
        <div class="right-text yellow">
          <p>1</p>
          <p>2</p>
          <p>3</p>
        </div>
        <div class="center-text">
          <p>Assia</p>
          <p>Aissatou</p>
          <p>Nolan</p>
        </div>
        <div class="left-text green">
          <p>100</p>
          <p>90</p>
          <p>80</p>
        </div>
      </div>
    </div>
    <div>
      <h1 class="launch-title">Tableau des scores personnels</h1>
      <div class="wrapper triple classement">
        <div class="right-text yellow">
          <p>1</p>
          <p>2</p>
          <p>3</p>
        </div>
        <div class="center-text">
          <p>Nolan</p>
          <p>Nolan</p>
          <p>Nolan</p>
        </div>
        <div class="left-text green">
          <p>80</p>
          <p>70</p>
          <p>60</p>
        </div>
      </div>
    </div>
  </div>
  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>
</template>