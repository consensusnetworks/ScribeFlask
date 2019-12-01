<template>
  <div>
        <h1 class="center">Welcome to Scribe!</h1>
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
      email: decoded.identity.email,
      twitteraccounts: []
    }
  },
  components: {
    Accountform,
    Accounttable,
  }
}
</script>

<style scoped>
.center {
 text-align: center
}
</style>