<template>
  <div class="container">
    <div id="account-table">
        <md-table md-card md-fixed-header v-model="twitteraccounts">
            <md-table-toolbar>
                <h1>Tracked Twitter Accounts</h1>
            </md-table-toolbar>
            <md-table-row v-for="account in twitteraccounts" v-bind:key="account.id">
                <md-table-cell md-label="Twitter Handle" md-sort-by="handle">{{account.handle}}</md-table-cell>
                <md-table-cell md-label="Twitter ID" md-sort-by="twitterid">{{account.twitterid}}</md-table-cell>
                <md-table-cell md-label="FactomChainid" md-sort-by="chainid">{{account.chainid}}</md-table-cell>
                <md-table-cell md-label="Track"> 
                            <md-button 
                                class="md-raised button-text"
                                > Track
                            </md-button>
                </md-table-cell>
            </md-table-row> 
        </md-table>
    </div>
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
    data: function() {
        return {
            twitteraccounts: [],
        };
    },
    watch: {
        account: function() {
            console.log(this.account)
            this.twitteraccounts.push(this.account)
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
}
.md-label {
    color: black;
}
.md-table-cell {
    text-align: left;
}
.container {
    padding-bottom: 3%;
}
</style>