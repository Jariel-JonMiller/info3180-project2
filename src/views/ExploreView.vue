<template>
    <div class="container">
        <div class="row">
            <div class="col-6">
                <div class="post">
                    <div v-for="post in posts" :key="post.id">
                        <div class="card" style="width: 36rem;">
                            <RouterLink :to='"/users/" + post.user_id' class="madness">
                                <div class="card-header d-inline-block">
                                    <img :src="`/api/v1/uploads/${post.profile}`" alt="user_profile" class="avatar">
                                    &nbsp;
                                    <p class="d-inline-block text-dark">{{ post.username }}</p>
                                </div>
                            </RouterLink>
                            <div class="card-img-top">
                                <img :src="`/api/v1/uploads/${post.photo}`" alt="Post" class="img-fluid img-post">
                            </div>
                            <div class="card-body">
                                <p class="card-text">{{ post.caption }}</p>
                            </div>
                            <div class=" d-flex justify-content-between align-items-end px-3">
                                <p class="clicker" @click="like(post.id)"><svg xmlns="http://www.w3.org/2000/svg"
                                        width="16" height="16" fill="currentColor" class="bi bi-heart"
                                        viewBox="0 0 16 16">
                                        <path
                                            d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.09.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15" />
                                    </svg> {{ post.likes }} Likes</p>
                                <p>{{ formatDate(post.created_on)}}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-6">
                <RouterLink to="/posts/new">
                    <button class="btn btn-primary">New Post</button>
                </RouterLink>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { RouterLink } from 'vue-router';

let posts = ref([]);
let likes = ref();
let csrf_token = ref("");

const fetchPosts = () => {
    fetch("/api/v1/posts", {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
        }
    })
        .then(response => response.json())
        .then(data => {
            posts.value = data.posts;
            console.log(posts);
        })
        .catch(error => {
            console.error('Error fetching posts:', error);
        });
};

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

function like(post_id) {
    const requestBody = JSON.stringify({ user_id: localStorage.getItem("id") });
    const postIndex = posts.value.findIndex(post => post.id === post_id);
    const poster = posts.value[postIndex];

    fetch(`/api/v1/posts/${post_id}/like`, {
        method: 'POST',
        body: requestBody,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'X-CSRFToken': csrf_token.value,
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Post liked!") {
                poster.likes = data.Likes; // Update the likes count directly from the response
            }
        })
        .catch(error => {
            console.error('Error fetching posts:', error);
        });
}

function formatDate(dateString) {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = months[date.getMonth()];
    const year = String(date.getFullYear()).slice(-2);
    return `${day} ${month} ${year}`;
}

fetchPosts();
</script>
<style scoped>
.post {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 30px;
}

.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
}

.img-post {
    
    width: 1080px;
    object-fit: cover;
}

button {
    display: block;
    width: 100%;
    min-width: 200px;
    padding: 10px;
    margin: 20px auto;
    border: none;
    color: #fff;
    border-radius: 5px;
    cursor: pointer;
}







.clicker {
    cursor: pointer;
}
</style>
