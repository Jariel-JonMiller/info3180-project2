<template>
    <div class="container justify-content-center d-grid">
        <h3>New Post</h3>
        <PostForm />
    </div>
</template>

<script>
import PostForm from '@/components/PostForm.vue';

export default {
    components: {
        PostForm,
    },
};
</script>

<style>
/* Add any component specific styles here */
</style>
