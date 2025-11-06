<template>
  <div v-if="question">
    <p>{{ question.title }}</p>
    <p>{{ question.text }}</p>
    <img v-if="question.image" :src="question.image" />

    <a @click="emit('click-on-answer', 1)">réponse A</a>
    <a @click="emit('click-on-answer', 2)">réponse B</a>
    <a @click="emit('click-on-answer', 3)">réponse C</a>
    <a @click="emit('click-on-answer', 4)">réponse D</a>
  </div>
</template>

<script setup>
defineProps({
  question: Object
});

const emit = defineEmits(['click-on-answer']);
</script>
