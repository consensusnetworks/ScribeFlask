<template>
  <div>
    <md-toolbar v-if="auth=='logged-in'" class="md-accent" md-elevation="1">

      <md-menu md-direction="bottom-end">
        <md-button class="md-icon-button" md-menu-trigger>
            <md-icon>settings</md-icon>
        </md-button>
        <md-menu-content>
            <md-menu-item>
                <router-link
                    :to="{ name: 'Home' }"
                    class="button-text"
                    >Home
                </router-link>
            </md-menu-item>
            <md-menu-item>
                <a  class="button-text" href="/logout">Logout</a>
            </md-menu-item>
        </md-menu-content>
      </md-menu>
      <md-badge md-content="1">
          <md-button class="md-icon-button">
              <md-icon>notifications</md-icon>
          </md-button>
      </md-badge>

    </md-toolbar>
      <md-toolbar v-if="auth==''" class="md-accent" md-elevation="1">
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
      }
  },
  mounted() {
    EventBus.$on('logged-in', status => {
      this.auth = status
    })
  }
}
</script>

<style>

</style>