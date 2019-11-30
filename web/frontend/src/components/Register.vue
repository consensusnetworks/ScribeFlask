<template>
  <div>
    <form novalidate class="md-layout" @submit.prevent="validateUser">
      <md-card class="md-layout-item md-size-50 md-small-size-100">
        <md-card-header>
          <div class="md-title">Please Register</div>
        </md-card-header>

        <md-card-content>
          <div class="md-layout md-gutter">
            <div class="md-layout-item md-small-size-100">
              <md-field :class="getValidationClass('Username')">
                <label for="username">Username</label>
                <md-input name="username" id="username" autocomplete="username" v-model="form.Username" :disabled="sending" />
                <span class="md-error" v-if="!$v.form.Username.required">The Username is required</span>
                <span class="md-error" v-else-if="!$v.form.Username.minlength">Invalid Username</span>
              </md-field>
            </div>

            <div class="md-layout-item md-small-size-100">
              <md-field :class="getValidationClass('Password')">
                <label for="Password">Password</label>
                <md-input name="Password" id="Password" autocomplete="Password" v-model="form.Password" :disabled="sending" />
                <span class="md-error" v-if="!$v.form.Password.required">The Password is required</span>
                <span class="md-error" v-else-if="!$v.form.Password.minlength">Invalid Password</span>
              </md-field>
            </div>
          </div>

          <md-field :class="getValidationClass('email')">
            <label for="email">Email</label>
            <md-input type="email" name="email" id="email" autocomplete="email" v-model="form.email" :disabled="sending" />
            <span class="md-error" v-if="!$v.form.email.required">The email is required</span>
            <span class="md-error" v-else-if="!$v.form.email.email">Invalid email</span>
          </md-field>
        </md-card-content>

        <md-progress-bar md-mode="indeterminate" v-if="sending" />

        <md-card-actions>
          <md-button type="submit" class="md-primary" :disabled="sending">Register</md-button>
        </md-card-actions>
      </md-card>

      <md-snackbar :md-active.sync="userSaved">The user {{ lastUser }} was saved with success!</md-snackbar>
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

  export default {
    name: 'FormValidation',
    mixins: [validationMixin],
    data: () => ({
      form: {
        Username: null,
        Password: null,
        email: null,
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
          minLength: minLength(5)
 
        },
        email: {
          required,
          email
        }
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
        this.form.email = null
      },
      saveUser () {
        this.sending = true

        // Instead of this timeout, here you can call your API
        window.setTimeout(() => {
          axios.post('/users/register', {
            Username: `${this.form.Username}`,
            Password: `${this.form.Password}`,
            email: `${this.form.email}`
          }).then(res => {
              this.Username = ''
              this.email = ''
              this.Password = ''
              router.push({ name: 'Login'})

          }).catch(err => {
              console.log(err)
          }),
          this.userSaved = true
          this.sending = false
          this.clearForm()
        }, 1500)
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