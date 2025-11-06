<template>
  <div>
    <h1>Résultat</h1>
    <p>Score : {{ score }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import ParticipationStorageService from "@/services/ParticipationStorageService";

const score = ref(0);
onMounted(() => {
  const s = ParticipationStorageService.getParticipationScore();
  score.value = Number.isNaN(parseInt(s, 10)) ? 0 : parseInt(s, 10);
});
</script>
