<template>
  <div v-if="question" class="question">
    <h2 class="question__title">{{ question.title }}</h2>
    <p class="question__text">{{ question.text }}</p>

    <img
      v-if="question.image"
      :src="question.image"
      alt=""
      class="question__image"
    />

    <div class="answers">
      <a class="answer" @click="emit('click-on-answer', 1)">
        {{ question.possibleAnswers[0].text }}
      </a>
      <a class="answer" @click="emit('click-on-answer', 2)">
        {{ question.possibleAnswers[1].text }}
      </a>
      <a class="answer" @click="emit('click-on-answer', 3)">
        {{ question.possibleAnswers[2].text }}
      </a>
      <a class="answer" @click="emit('click-on-answer', 4)">
        {{ question.possibleAnswers[3].text }}
      </a>
    </div>
  </div>
</template>

<script setup>
defineProps({
  question: Object
});
const emit = defineEmits(['click-on-answer']);
</script>

<style scoped>
.question {
  max-width: 720px;
  margin: 24px auto;
  padding: 16px;
  text-align: center;
}

.question__title {
  margin: 0 0 8px;
  font-size: 1.5rem;
  color: #f3f33e;
  font-weight: 700;
}

.question__text {
  margin: 0 0 16px;
  font-size: 2rem;
  color: #fbfdfd;
  font-weight: 700;
}

.question__image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,.08);
  margin: 12px 0 20px;
}

/* 2 réponses par ligne */
.answers {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  justify-items: center; /* centre chaque tuile dans sa cellule */
}

.answer {
  display: inline-block;
  width: 100%;
  padding: 12px 14px;
  border-radius: 10px;
  background: #f5f7fb;
  border: 1px solid #e5e8ef;
  text-decoration: none;
  color: #1f2937;
  font-weight: 600;
  transition: transform .06s ease, box-shadow .06s ease, background .2s;
  box-shadow: 0 1px 3px rgba(0,0,0,.05);
  cursor: pointer;
}

.answer:hover {
  background: #bfe17a;
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(0,0,0,.08);
}

.answer:active {
  transform: translateY(0);
  box-shadow: 0 1px 3px rgba(0,0,0,.05);
}

/* petit ajustement mobile */
@media (max-width: 480px) {
  .answers {
    grid-template-columns: 1fr; /* une par ligne si l'écran est trop étroit */
  }
}
</style>
