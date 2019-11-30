<template>
  <div>
    <form novalidate class="md-layout" @submit.prevent="validateUser">
      <md-card class="md-layout-item md-size-50 md-small-size-100">
        <md-card-header>
          <div class="md-title">Please Login</div>
        </md-card-header>

        <md-card-content>
          <div class="md-layout md-gutter">
            <div class="md-layout-item md-small-size-100">
              <md-field :class="getValidationClass('Username')">
                <label for="username">First Name</label>
                <md-input name="username" id="username" autocomplete="username" v-model="form.Username" :disabled="sending" />
                <span class="md-error" v-if="!$v.form.Username.required">The Username is required</span>
                <span class="md-error" v-else-if="!$v.form.Username.minlength">Invalid Username</span>
              </md-field>
            </div>

            <div class="md-layout-item md-small-size-100">
              <md-field :class="getValidationClass('Password')">
                <label for="Password">email</label>
                <md-input name="Password" id="Password" autocomplete="Password" v-model="form.Password" :disabled="sending" />
                <span class="md-error" v-if="!$v.form.Password.required">The Password is required</span>
                <span class="md-error" v-else-if="!$v.form.Password.minlength">Invalid Password</span>
              </md-field>
            </div>
          </div>
        </md-card-content>

        <md-progress-bar md-mode="indeterminate" v-if="sending" />

        <md-card-actions>
          <md-button type="submit" class="md-primary" :disabled="sending">Login</md-button>
        </md-card-actions>
      </md-card>

      <md-snackbar :md-active.sync="userSaved">{{ lastUser }} logged in successfully!</md-snackbar>
    </form>
  </div>
</template>

<script>
  import { validationMixin } from 'vuelidate';
  import {
    required,
    email,
    minLength,
    maxLength
  } from 'vuelidate/lib/validators';
  import axios from 'axios';
  import router from '../router';
  import EventBus from './EventBus';

  export default {
    name: 'FormValidation',
    mixins: [validationMixin],
    data: () => ({
      form: {
        Username: null,
        Password: null,
      },
      userSaved: false,
      sending: false,
      lastUser: null
    }),
    validations: {
      form: {
        Username: {
          required,
          minLength: minLength(3)
        },
        Password: {
          required,
          minLength: minLength(10)
 
        },
      }
    },
    methods: {
      getValidationClass (fieldName) {
        const field = this.$v.form[fieldName]

        if (field) {
          return {
            'md-invalid': field.$invalid && field.$dirty
          }
        }
      },
      clearForm () {
        this.$v.$reset()
        this.form.Username = null
        this.form.Password = null
      },
      login () {
        this.sending = true
        
        // Instead of this timeout, here you can call your API
        window.setTimeout(() => {
          axios.post('/users/login', {
            Username: this.Username,
            Password: this.Password
          }).then(res => {
              localStorage.setItem('usertoken', res.data.token)
          }).catch(err => {
              console.log(err)
          }),
          this.emitMethod()
          this.userSaved = true
          this.sending = false
          this.clearForm()
        }, 1500)
      },
      emitMethod() {
          EventBus.$emit('logged-in', 'loggedin')
      },
      validateUser () {
        this.$v.$touch()

        if (!this.$v.$invalid) {
          this.saveUser()
        }
      }
    }
  }
</script>

<style>
</style>