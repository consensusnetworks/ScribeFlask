<template>
  <div id="app">
    <navbar></navbar>
    <router-view/>
  </div>
</template>

<script>
import Navbar from './components/Navbar'
import Home from './components/Home'

export default {
  name: 'App',
  components: {
    'Navbar': Navbar,
    'Home': Home
  },
}

</script>

<style>
html, body {
        height: 100%;
        font-family: 'Roboto', sans-serif;
        
    }
</style>