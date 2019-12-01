<template>
  <div>
    <md-toolbar v-if="auth=='loggedin'" class="md-accent" md-elevation="1">
      <h3>
          <router-link :to="{ name: 'Home'}" class="md-title" style="flex: 1">
            Scribe
          </router-link>
      </h3>
        <md-button v-on:click="logout">Logout</md-button>
    </md-toolbar>
      <md-toolbar v-if="auth===''" class="md-accent" md-elevation="1">
        <md-button>
          <router-link :to="{ name: 'Login'}" class="button-text">
            Login
          </router-link>
        </md-button>
        <md-button>
          <router-link :to="{ name: 'Register'}" class="button-text">
            Register
          </router-link>
        </md-button>
      </md-toolbar>
  </div>
</template>

<script>
import EventBus from './EventBus'
import router from '../router'

EventBus.$on('logged-in', test => {
  console.log(test)
})
export default {
  data() {
    return {
      auth: '',
      user: ''
    }
  },

  methods: {
    logout() {
        localStorage.removeItem('usertoken')
        this.emitMethod()
        router.push({ name: 'Login'})
      },
     emitMethod() {
          EventBus.$emit('logged-in', '')
      },
  },
  mounted() {
    EventBus.$on('logged-in', status => {
      this.auth = status
    })
  }
}
</script>

<style scoped>
.button-text {
    color: white;
}
.md-toolbar {
  background-color: #29b6f6  !important;
}
.md-button {
  color: white;
}
.md-menu-item {
    background-color: #29b6f6;
}
.md-title {
    font-weight: bold;
    font-size: 130%;
    color: white;
}
.md-title:hover {
    color: #f56f12 !important;
}
</style>