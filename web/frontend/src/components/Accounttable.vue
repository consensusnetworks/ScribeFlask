<template>
  <div class="container">
        <li  v-for="account in twitteraccounts" v-bind:key="account.id">
            {{ account }}
        </li>
  </div>
</template>

<script>
  export default {
    name: 'Accounttable',
    props: {
        account: {
            type: Object
        }
    },
    data () {
        return {
            twitteraccounts: [],
        };
    },
    watch: {
        account: function() {
            console.log(this.account)
            this.twitteraccounts.push(this.account)
        }
    }
  }
  
</script>

<style scoped>
.md-button {
    background-color: #f56f12;
  }
.md-title {
    text-align: left;
}
.md-table-cell {
    text-align: left;
}
.container {
    padding-bottom: 3%;
}
</style>