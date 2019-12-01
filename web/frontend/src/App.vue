<template>
  <div id="app">
    <navbar></navbar>
    <router-view/>
  </div>
</template>

<script>
import Navbar from './components/Navbar'

export default {
  name: 'App',
  components: {
    'Navbar': Navbar
  }
}
</script>

<style>
html, body {
        height: 100%;
        font-family: 'Roboto', sans-serif;
        
    }
</style>