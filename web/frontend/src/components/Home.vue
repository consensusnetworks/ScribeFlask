<template>
  <div>
        <h1 class="center">Welcome to Scribe!</h1>
        <accountform @addAccount="updateMessage" />
        <accounttable :account="childData"/>
  </div>
</template>


<script>
import jwtDecode from 'jwt-decode'
import Accountform from './Accountform'
import Accounttable from './Accounttable'
import Navbar from './Navbar'
export default {
  data: function () {
    const token = localStorage.usertoken
    const decoded = jwtDecode(token)
    return {
      Username: decoded.identity.username,
      email: decoded.identity.email,
      childData: "",
    }
  },
  components: {
    Accountform,
    Accounttable,
  },
  methods: {
    updateMessage(variable) {
      this.childData=variable;
      console.log(this.childData)


    }
  }
}
</script>

<style scoped>
.center {
 text-align: center
}
</style>