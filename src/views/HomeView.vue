<template>
  <div class="container my-5 d-flex align-items-center justify-content-center">
    <div class="row w-100">
      <div class="col-md-6 h-50vh">
        <img src="/src/assets/hero.jpg" alt="A beautiful landscape with mountains, a lake, and a clear sky"
          class="img-fluid h-100">
      </div>
      <div class="col-md-6 h-50vh">
        <div id="welcome"
          class="card border shadow p-3 mb-5 bg-white rounded h-100 d-flex flex-column justify-content-center">
          <div class="card-top text-center">
            <div class="d-flex align-items-center justify-content-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" fill="currentColor"
                class="bi bi-camera-fill" viewBox="0 0 16 16">
                <path d="M10.5 8.5a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0" />
                <path
                  d="M2 4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-1.172a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 9.172 2H6.828a2 2 0 0 0-1.414.586l-.828.828A2 2 0 0 1 3.172 4zm.5 2a.5.5 0 1 1 0-1 .5.5 0 0 1 0 1m9 2.5a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0" />
              </svg>
              <h1 class="lobster-regular">Photogram</h1>
            </div>
            <hr>
            <p>{{ welcomeMessage }}</p>
            <div class="py-5 gap-2">
              <router-link to="/register" type="button" class="btn btn-success"
                style="width:18rem;">Register</router-link>
              &nbsp;
              <router-link to="/login" type="button" class="btn btn-primary" style="width:18rem;">Login</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const welcomeMessage = "Share photos of your favourite moments with friends, family and the world.";
</script>

<style>
/* Add any component specific styles here */
.h-50vh {
  height: 50vh;
  object-fit: cover;
}

@import url('https://fonts.googleapis.com/css2?family=Lobster&display=swap');

.lobster-regular {
  font-family: "Lobster", sans-serif;
  font-weight: 400;
  font-style: normal;
}
</style>