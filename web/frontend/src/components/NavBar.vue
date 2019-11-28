<template>
  <div>
    <md-toolbar class="md-accent" md-elevation="1">
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
  </div>
</template>

<script>
export default {
  name: "NavBar"
}
</script>

<style>

</style>