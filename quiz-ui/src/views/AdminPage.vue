<!-- src/views/AdminPage.vue -->
<template>
  <div class="admin">
    <!-- Login si pas de token -->
    <div v-if="!token" class="login">
      <h2>Administration</h2>
      <input
        type="password"
        v-model="password"
        placeholder="Mot de passe"
        @keyup.enter="login"
      />
      <button @click="login" class="button">Connexion</button>
      <p v-if="loginError" class="error">Mauvais mot de passe</p>
    </div>

    <!-- Contenu admin si token présent -->
    <div v-else>
      <header class="topbar">
        <h2>Admininistration</h2>

      </header>

      <section class="content">
        <QuestionsList />
      </section>
      <button class="logout" @click="logout">Déconnexion</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import QuestionsList from "@/components/QuestionsList.vue";
import QuizApiService from "@/services/QuizApiService";

const token = ref(localStorage.getItem("adminToken") || "");
const password = ref("");
const loginError = ref(false);

async function login() {
  loginError.value = false;
  const res = await QuizApiService.call("post", "/login", { password: password.value });
  if (res && res.status === 200 && res.data?.token) {
    token.value = res.data.token;
    localStorage.setItem("adminToken", token.value);
    password.value = "";
  } else {
    loginError.value = true;
  }
}

function logout() {
  token.value = "";
  localStorage.removeItem("adminToken");
  location.href = "/";
}
</script>

<style scoped>
.admin { max-width: 900px; margin: 24px auto; padding: 16px; }

/* Bloc login */
.login { text-align: center; max-width: 360px; margin: 80px auto; }
.login input { width: 100%; padding: 10px; margin: 8px 0; }
.login button { padding: 10px 14px; }
.error { color: #b91c1c; margin-top: 8px; }

.topbar {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 12px;
  margin-bottom: 16px;
}
.topbar h2 { margin: 0; }
.logout { margin-right: 0px; margin-bottom: 40px; padding: 8px 12px; border-radius: 40px; background-color: var(--second-color);}

.content { margin-top: 12px; }
</style>
