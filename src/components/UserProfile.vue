<template>
    <div class="px-5">
        <div class="profile-header ">
            <div class="toga">
                <div class="img">
                    <img class="profileimg" :src="`/api/v1/uploads/${user.profile}`" alt="Card image">
                </div>
                <div class="back">
                    <p class="name">{{ user.fullname }}</p>
                    <div class="text-muted">
                        <p class="mb-0">{{ user.location }}</p>
                        <p class="usert">{{ user.joined }}</p>
                        <p class="bio text-secondary">{{ user.biography }}</p>
                    </div>
                </div>
            </div>
            <div class="lel">
                <div class="notif ">
                    <div>
                        <p class="mb-0 h4"> {{ user.posts }} </p>
                        <p class="pow text-muted">Posts</p>
                    </div>
                    <div>
                        <p class="mb-0 h4"> {{ user.follows }} </p>
                        <p class="pow text-muted">Followers</p>
                    </div>
                </div>
                <button class="btn btn-primary" :class="{ 'following': followStatus }" @click="followUser"
                    type="submit">
                    {{ followStatus ? 'Following' : 'Follow' }}
                </button>

            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from 'vue-router';

let csrf_token = ref("");
let user = ref({});
const route = useRoute();
const followStatus = ref(false); // Added a ref for follow status

function getCsrfToken() {
    fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            csrf_token.value = data.csrf_token;
            followUser();
        });
}

function followUser() {
    const requestBody = JSON.stringify({ id: localStorage.getItem('id') });

    fetch(`/api/users/${route.params.user_id}/follow`, {
        method: 'POST',
        body: requestBody,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'X-CSRFToken': csrf_token.value,
        }
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            if (data.message === "you are now following that user.") {
                followStatus.value = true; // Update follow status to true
                user.value.follows += 1; // Increment follower count
            } else if (data.message === "You are already following this user.") {
                followStatus.value = true; // Update follow status to true
                // No need to increment follower count here as it's already increased
            }
        });
}

onMounted(() => {
    getCsrfToken();
    fetch(`/api/user/${route.params.user_id}`, {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
        }
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    errorMessage.value = data.errors ? Object.values(data.errors) : ['Failed to post'];
                    throw new Error('Failed to post', data.errors);
                });
            } else {
                return response.json()
            }
        })
        .then(data => {
            user.value = data;
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
</script>

<style>
.profile-header {
    display: flex;
    width: 100%;
    gap: 20px;
    margin: auto;
    justify-content: space-between;
    border: 1px #ccc solid;
    padding: 10px;
    height: 300px;
    box-shadow: 0px 5px 5px rgba(0, 0, 0, 0.184);
}

.notif {
    display: flex;
    gap: 20px;
    font-weight: 600;
    text-align: center;
    font-size: 16px;
}



.lel {
    display: grid;
    align-items: center;
}

#folly {
    height: 40px;
    width: 200px;
    font-weight: 700;
}

.following {
    background-color: green;
}

.pow {
    font-size: 18px;
}

.name {
    font-weight: 600;
    font-size: 20px;
}




.toga {
    display: flex;
    align-items: center;
}

.img {
    flex: 0 0 auto;
    margin-right: 20px;
}

.profileimg {
    height: 250px;
    width: 200px;
}

.back {
    height: 100%;
    display: grid;
    align-items: center;
}
</style>
