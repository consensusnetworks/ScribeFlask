<template>

  <div id="account-form" class= "md-layout md-gutter" >
    <div class = "md-layout-item"></div>
    <div class="md-layout-item">
      <form @submit.prevent="validateAccount">
        <md-card class="md-layout-item md-alignment-center">
            <md-card-header>
              <div class="md-title">Add Accounts</div>
            </md-card-header>

            <md-card-content>
              <md-field :class="getValidationClass('handle')">
                <label for="handle">Twitter Handle</label>
                <md-input id ="handle"
                          name="handle"
                          v-model="twitteraccount.handle"
                          :disabled="submitting">
                </md-input>
                <span class="md-error" v-if="!$v.twitteraccount.handle.required">Twitter Handle is Required</span>
               
              </md-field>

              <md-field :class="getValidationClass('twitterid')">
                <label for="twitterid">Twitter ID</label>
                <md-input id="twitterid"
                          name="twitterid"
                          v-model="twitteraccount.twitterid"
                          :disabled="submitting">
                </md-input>
                <span class="md-error" v-if="!$v.twitteraccount.twitterid.required">Twitter ID is Required</span>
              </md-field>
            </md-card-content>

              <md-card-actions>
                <md-button type="submit" class="md-raised button-text" :disabled="submitting">Track Account</md-button>
              </md-card-actions>
          </md-card>

          <md-snackbar :md-duration="10000" :md-active.sync="success" md-persistent>
            This Account is now being tracked! We will notify you when their tweets are being Factomized!
          </md-snackbar>
      </form> 
    </div>
    <div class="md-layout-item"></div>
  </div>

</template>


<script>
  import axios from 'axios'
  import EventBus from './EventBus'
  import { validationMixin } from 'vuelidate'
  import {
    required,
    minLength
  } from 'vuelidate/lib/validators'
  export default {
    name: "Accountform",
    mixins: [validationMixin],
    data() {
      return {
        submitting: false,
        error: false,
        success: false,
        twitteraccount: {
          handle: '',
          twitterid: '',
          chainid: ''
        },
      }
    },
    validations: {
      twitteraccount: {
          handle: {
            required,
            minLength: minLength(1)
          },
          twitterid: {
            required,
            minLength: minLength(1)
          }
      }
    },
    computed: {
        invalidHandle() {
            return this.twitteraccount.handle === ''
        },
        invalidTwitterID() {
            return this.twitteraccount.twitterid === ''
        },
    },
    methods: {
        addAccount() {
            this.submitting = true
            window.setTimeout(() => {
                axios.post('http://localhost:8000/users/twitteraccounts', {
                  handle: `${this.twitteraccount.handle}`,
                  twitterid: `${this.twitteraccount.twitterid}`
                }).then(res => {
                    console.log(res.data)
                    this.twitteraccount.chainid = res.data.chainid
                    console.log(this.twitteraccount)
                    this.$emit('addAccount', this.twitteraccount)
                    console.log(this.twitteraccount)
                    this.twitteraccount = {
                      handle: '',
                      twitterid: '',
                      chainid: ''

                    }

                }).catch(err => {
                    console.log(err)
                }),
                this.clearStatus()
              }, 1500)
            if (this.invalidHandle || this.invalidTwitterID) {
            this.error = true
            return
            }
            this.error = false
            this.success = true
            this.submitting = false
         },
        getValidationClass (fieldName) {
          const field = this.$v.twitteraccount[fieldName]
          if (field) {
            return {
              'md-invalid': field.$invalid && field.$dirty
            }
          }
        },
        clearStatus() {
            this.success = false
            this.error = false
        },
        validateAccount () {
          this.$v.$touch()
          if (!this.$v.$invalid) {
            this.addAccount()
          }
        }
    }
  }
</script>

<style scoped>
  form {
    margin-bottom: 2rem;
  }
  [class*='-message'] {
    font-weight: 500;
  }
  .button-text {
    color: white;
}
  .error-message {
    color: #d33c40;
  }
  .success-message {
    color: #32a95d;
  }
  .md-button {
    background-color: #f56f12;
  }
  .md-title {
    color: white;
    text-align: left;
  }
  .md-card-header {
    background-color: #29b6f6;
  }
  .md-error {
    color: red; 
  }
  .md-snackbar {
    background-color: #f56f12;
    color: white;
  }
  .md-layout-item {
     height: 40px;

      width: 100%;
      height: 100%;
      display: block;
      content: " ";
  }
</style>