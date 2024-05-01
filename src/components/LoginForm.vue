<template>
    <div class="d-flex justify-content-center align-items-center">
        <div class="card p-5" style="width: 30rem;">
            <form id="loginForm" @submit.prevent="login">
                <div>
                    <label for="username" class="form-label">Username</label>
                    <input type="text" name="username" class="form-control" />
                </div>
                <div>
                    <label for="password" class="form-label">Password</label>
                    <input type="text" name="password" class="form-control" />
                </div>
                <div class="py-5">
                    <button class="btn btn-success" type="submit" style="width: 24rem;">Login</button>
                </div>

            </form>
        </div>
    </div>
</template>


<script setup>

import { ref, onMounted } from "vue";
import { useRouter } from 'vue-router';

const successMessage = ref('');
const errorMessage = ref('');

let csrf_token = ref("");
let token = ref("")
let router = useRouter();
let userid;

function getCsrfToken() {
    fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            csrf_token.value = data.csrf_token;
        });
}

onMounted(() => {
    getCsrfToken();
    token.value = localStorage.getItem('token');
});

const login = () => {
    const loginForm = document.getElementById('loginForm');
    const formData = new FormData(loginForm);

    fetch("/api/v1/auth/login", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrf_token.value
        }
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    errorMessage.value = data.errors ? Object.values(data.errors) : ['Failed to login'];
                    throw new Error('Failed to login');
                });
            }
            return response.json();
        })
        .then(data => {
            // Display a success message
            successMessage.value = 'User Logged In';
            token.value = data[0].token;
            userid = data[0].id;
            console.log(data);
            localStorage.setItem('token', token.value);
            localStorage.setItem('id', userid);
            console.log(userid)
            router.push("/explore")
        })
        .catch(error => {
            console.error('Error:', error);
        });
};
</script>

<style></style>
