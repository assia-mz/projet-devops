<!-- components/QuestionAdminDisplay-->
<template>
  <div class="wrap" v-if="question">
    <div class="actions">
      <button @click="goEdit" class="editer">Éditer</button>
      <button class="danger" @click="deleteQuestion">Supprimer</button>
    </div>

    <h2 class="title">{{ question.title }}</h2>
    <p class="text">{{ question.text }}</p>
    <img v-if="question.image" :src="question.image" alt="" class="image" />

    <ul class="answers">
      <li v-for="ans in question.possibleAnswers" :key="ans.id ?? ans.index">
        <label>
          <input type="radio" :checked="ans.isCorrect" disabled />
          <span>{{ ans.text }}</span>
        </label>
      </li>
    </ul>
  </div>

  <p v-else class="empty">Chargement…</p>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import QuizApiService from "@/services/QuizApiService";

const route = useRoute();
const router = useRouter();

const question = ref(null);

onMounted(async () => {
  const id = route.params.id || route.query.id;
  if (!id) return;
  const res = await QuizApiService.call("get", `/questions/${id}`);
  if (res?.status === 200) question.value = res.data;
});

function goEdit() {
  if (!question.value) return;
  // Redirige vers la page d'édition
  router.push({ path: "/edition", query: { id: question.value.id } });
}

async function deleteQuestion() {
  if (!question.value) return;
  if (!confirm("Supprimer cette question ?")) return;

  const token = localStorage.getItem("adminToken") || "";
  const res = await QuizApiService.call(
    "delete",
    `/questions/${question.value.id}`,
    null,
    token
  );
  if (res && (res.status === 200 || res.status === 204)) {
    // retour à la liste des questions
    router.push("/admin");
  }
}
</script>

<style scoped>
.wrap {
  max-width: 720px;
  margin: 24px auto;
  padding: 16px;
  text-align: center;
}

.actions { display: flex; gap: 8px; justify-content: flex-end; margin-bottom: 12px; }
.danger { background: #f05050; border: 1px solid #ec5353; border-radius: 40px; }
.editer { background-color: var(--second-color); border-radius: 40px; width: 110px; }

.title {
  margin: 0 0 8px;
  font-size: 1.5rem;
  color: #f3f33e;
  font-weight: 700;
}
.text {
  margin: 0 0 16px;
  font-size: 2rem;
  color: #fbfdfd;
  font-weight: 700;
}

.image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,.08);
  margin: 12px 0 20px;
}


.answers {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  justify-items: center;
}
.answers li {
  width: 100%;
}
.answers li label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 12px 14px;
  border-radius: 10px;
  background: #f5f7fb;
  border: 1px solid #e5e8ef;
  color: #1f2937;
  font-weight: 600;
  transition: transform .06s ease, box-shadow .06s ease, background .2s;
  box-shadow: 0 1px 3px rgba(0,0,0,.05);
}
.answers li label:hover {
  background: #bfe17a;
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(0,0,0,.08);
}


/* Chargement */
.empty { text-align: center; margin: 24px 0; }

@media (max-width: 480px) {
  .answers { grid-template-columns: 1fr; }
}
</style>

