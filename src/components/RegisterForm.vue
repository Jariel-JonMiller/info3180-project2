<template>
    <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>
    <!-- Error messages -->
    <div v-if="errorMessage" class="alert alert-danger">
        <ul>
            <li v-for="error in errorMessage" :key="error">{{ error }}</li>
        </ul>
    </div>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <h1>Register</h1>
                <div class="card">
                    <div class="card-body d-flex justify-content-center"> <!-- Added flex utilities -->
                        <form id="registerForm" @submit.prevent="register" style="width: 18rem;">
                            <div class="form-group mb-3">
                                <label for="username" class="form-label">Username</label>
                                <input type="text" name="username" class="form-control" />
                            </div>
                            <div class="form-group mb-3">
                                <label for="password" class="form-label">Password</label>
                                <input type="password" name="password" class="form-control" />
                            </div>
                            <div class="form-group mb-3">
                                <label for="email" class="form-label">Email</label>
                                <input type="email" name="email" class="form-control" />
                            </div>
                            <div class="form-group mb-3">
                                <label for="firstname" class="form-label">Firstname</label>
                                <input type="text" name="firstname"  class="form-control" />
                            </div>
                            <div class="form-group mb-3">
                                <label for="lastname" class="form-label">Lastname</label>
                                <input type="text" name="lastname"  class="form-control" />
                            </div>
                            <div class="form-group mb-3">
                                <label for="location" class="form-label">Location</label>
                                <input type="text" name="location"  class="form-control" />
                            </div>
                            <div class="form-group mb-3">
                                <label for="biography" class="form-label">Biography</label>
                                <input type="text" id="biography" name="biography" 
                                    class="form-control" />
                            </div>
                            <div class="form-group mb-3">
                                <label for="profile" class="form-label">Profile Photo</label>
                                <input type="file" name="photo" class="form-control" />
                            </div>
                            <button type="submit" class="btn btn-success" style="width: 18rem;">Register</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const successMessage = ref('');
const errorMessage = ref('');

let csrf_token = ref("");

function getCsrfToken() {
    fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            csrf_token.value = data.csrf_token;
        });
}

onMounted(() => {
    getCsrfToken();
});

const register = () => {
    const registerForm = document.getElementById('registerForm');
    const formData = new FormData(registerForm);

    fetch("/api/v1/register", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrf_token.value
        }
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    errorMessage.value = data.errors ? Object.values(data.errors) : ['Failed to register'];
                    throw new Error('Failed to register');
                });
            }
            return response.json();
        })
        .then(data => {
            // Display a success message
            successMessage.value = data.message;
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
};
</script>

<style>

</style>
