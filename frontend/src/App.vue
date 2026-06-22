<template>
  <router-view />
  <ToastHost />
</template>

<style>
/* Un peu de style global pour que ce soit propre */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f4f7f6;
}
</style>
<script setup>
import ToastHost from './components/ToastHost.vue';
</script>