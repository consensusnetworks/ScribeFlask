<template>
  <div class="container md-layout md-gutter">
    <div class= "md-layout-item"></div>
    <div id="account-table" class="md-layout-item">
        <md-table md-card md-fixed-header v-model="twitteraccounts">
            <md-table-toolbar>
                <h1 class="md-title">Tracked Twitter Accounts</h1>
            </md-table-toolbar>
            <md-table-row v-for="account in twitteraccounts" v-bind:key="account.id">
                <md-table-cell md-label="Twitter Handle" md-sort-by="handle">{{account.handle}}</md-table-cell>
                <md-table-cell md-label="Twitter ID" md-sort-by="twitterid">{{account.twitterid}}</md-table-cell>
                <md-table-cell md-label="FactomChainid" md-sort-by="chainid">{{account.chainid}}</md-table-cell>
            </md-table-row> 
        </md-table>
    </div>
    <div class= "md-layout-item"></div>
  </div>
</template>

<script>
  export default {
    name: 'Accounttable',
    props: {
        account: {
            type: Object,
            default: {}
        }
    },
    data: function() {
        return {
            twitteraccounts: [],
        };
    },
    watch: {
        account: function() {
            console.log(this.account)
            this.twitteraccounts = [...this.twitteraccounts, this.account]
            console.log(this.twitteraccounts)
        }
    }
  }
  
</script>

<style scoped>
.button-text {
    color: white;
}
.md-button {
    background-color: #f56f12;
  }
.md-title {
    text-align: left;
    color: white;
}
.md-table-cell {
    text-align: left;
}
.container {
    padding-bottom: 3%;
}
.md-table-toolbar {
  background-color: #29b6f6;
}
.md-layout-item {
     height: 40px;

      width: 100%;
      height: 100%;
      display: block;
      content: " ";
  }
</style>