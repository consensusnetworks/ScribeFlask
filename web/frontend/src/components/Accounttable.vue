<template v-model="twitteraccounts">
  <div class="container">
        <li  v-for="(message, index) in twitteraccounts" :item="message" :key="index">
            {{ message }}
        </li>
  </div>
</template>

<script>
  export default {
    name: 'Accounttable',
    props: {
        account: {
            type: Object
        },
    },
    data: function() {
        return {
            twitteraccounts: [],
        };
    },
    watch: {
        account: function() {
            console.log(account)
            this.twitteraccounts.push(account)
        }
    },
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