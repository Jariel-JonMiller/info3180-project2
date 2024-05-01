<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <RouterLink class="navbar-brand lobster-regular" to="/">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-camera-fill"
            viewBox="0 0 16 16">
            <path d="M10.5 8.5a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0" />
            <path
              d="M2 4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-1.172a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 9.172 2H6.828a2 2 0 0 0-1.414.586l-.828.828A2 2 0 0 1 3.172 4zm.5 2a.5.5 0 1 1 0-1 .5.5 0 0 1 0 1m9 2.5a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0" />
          </svg> Photogram
        </RouterLink>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link" :class="{ active: $route.path === '/' }">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink to="/explore" class="nav-link" :class="{ active: $route.path === '/explore' }">Explore
              </RouterLink>
            </li>
            <li class="nav-item">
              <a href="#" class="nav-link" @click.prevent="show">My Profile</a>
            </li>
            <li v-if="!logged" class="nav-item">
              <RouterLink to="/login" class="nav-link">Login</RouterLink>
            </li>
            <li v-else class="nav-item">
              <a href="#" class="nav-link" @click.prevent="logout">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink, useRouter } from "vue-router";
import { ref, onMounted, computed } from 'vue';

const router = useRouter();
const csrf_token = ref("");
const id = localStorage.getItem('id');

onMounted(() => {
  getCsrfToken();
});

const logged = computed(() => {
  return localStorage.getItem('token') !== null;
});

function show() {
  const child = localStorage.getItem('id');
  if (child) {
    router.push(`/users/${child}`);
  } else {
    router.push("/");
  }
}

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    });
}

const logout = () => {
  fetch("/api/v1/auth/logout", {
    method: 'POST',
    headers: {
      'X-CSRF-Token': csrf_token.value,
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    }
  })
    .then(() => {
      localStorage.removeItem('token');
      localStorage.removeItem('id');
      router.push("/");
    })
    .catch(error => {
      console.error('Error:', error);
    });
};
</script>

<style scoped>
.lobster-regular {
  font-family: "Lobster", sans-serif;
  font-weight: 400;
  font-style: normal;
}
</style>
