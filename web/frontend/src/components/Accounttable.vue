<template>
  <div class="container">
        <div id="account-table">
            <p v-if="twitteraccounts.length < 1" class="empty-table">
                No account
            </p>
            <md-table v-model="twitteraccounts" md-card md-fixed-header v-else>
                <md-table-toolbar>
                        <h1 class="md-title">Tracked Twitter Accounts</h1>
                </md-table-toolbar>

                <md-table-row slot="md-table-row" slot-scope="{ item }">
                    <md-table-cell md-label="ID" md-sort-by="id" md-numeric>{{ item.id }}</md-table-cell>
                    <md-table-cell md-label="Twitter Handle" md-sort-by="handle"> {{item.handle}}</md-table-cell>
                    <md-table-cell md-label="Twitter ID" md-sort-by="twitterid"> {{item.twitterid}}</md-table-cell>
                    <md-table-cell md-label="Chain ID" md-sort-by="chainid"> {{item.chainid}}</md-table-cell>
                    <md-table-cell md-label="Stop Tracking"> 
                        <md-button 
                            class="md-raised"
                            @click="$emit('delete:twitteraccount', item.id)"
                            > Delete
                        </md-button>
                    </md-table-cell>

                </md-table-row>

            </md-table>
        </div>
  </div>
</template>

<script>
  export default {
    name: 'AccountTable',
    props: {
        twitteraccounts: Array,
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