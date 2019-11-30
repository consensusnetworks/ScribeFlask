<template>
  <div>
    <md-toolbar class="md-accent" md-elevation="1">
      <div>
        <h1 class="Text-center">Welcome to Scribe!</h1>
      </div>
    </md-toolbar>
    <p>Username</p>
    <p>{{Username}}</p>
    <p>email</p>
    <p>{{email}}</p>
    <accountform></accountform>
    <accounttable></accounttable>
  </div>
</template>


<script>
import jwtDecode from 'jwt-decode'
import Accountform from './Accountform'
import Accounttable from './Accounttable'
import Navbar from './Navbar'
export default {
  data () {
    const token = localStorage.usertoken
    const decoded = jwtDecode(token)
    return {
      Username: decoded.identity.username,
      email: decoded.identity.email
    }
  },
  components: {
    Accountform,
    Accounttable,
  }
}
</script>