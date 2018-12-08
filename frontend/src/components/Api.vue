<template>
  <div>
    <p>Home page</p>
    <p>Random number from backend: {{ randomNumber }}</p>
    <button @click="getRandom" class="btn btn-primary">New random number</button>
    <button @click="getAlert">Alert example</button>
    <FlashMessage></FlashMessage>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      randomNumber: 0,
      text: 'Lorem ipsum dolor sit amet'
    }
  },
  methods: {
    getRandom () {
      this.randomNumber = this.getRandomFromBackend()
    },
    getRandomFromBackend () {
      const path = `api/random`
      axios.get(path)
        .then(response => {
          this.randomNumber = response.data.randomNumber
        })
        .catch(error => {
          console.log(error)
        })
    },
    getAlert () {
      this.flashMessage.show({
        status: 'error',
        title: 'Error Message Title',
        message: 'Oh, you broke my heart! Shame on you!'
      })
    },
  },
  created () {
    this.getRandom()
  }
}
</script>
