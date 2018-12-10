<style>

  img {
    max-height: 300px;
  }

</style>

<template>

  <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <label>File
        <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
      </label>
      <button v-on:click="submitFile()">Submit</button>
    </div>
    <div class="container">
      <div class="row">
        <div class="col-sm">
          Original image
        </div>
        <div class="col-sm">
          Transformed image
        </div>
      </div>
      <div class="row">
        <div class="col-sm">
          <div class="img"><img :src="originalImage"></div>
        </div>
        <div class="col-sm">
          <div class="img"><img :src="transformedImage"></div>
        </div>
      </div>
    </div>
    <FlashMessage></FlashMessage>
  </div>

</template>

<script>

  import axios from 'axios'

  export default {
    data() {
      return {
        file: '',
        originalImage: '/api/get/logo.png',
        transformedImage: '/api/get/logo.png'
      }
    },

    methods: {
      submitFile() {
        let formData = new FormData();
        formData.append('file', this.file);

        var vm = this;
        axios.post('/api/send-file',
          formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        ).then(function (response) {
          console.log(response);
          vm.originalImage = '/api/get/' + vm.file.name;
          vm.transformedImage = '/api/get/' + vm.file.name + '?transformed=true'
        }).catch(function (error) {
          console.log(error);
          vm.flashMessage.show({
            status: 'error',
            title: 'Oops!',
            message: error['response']['data']
          })
        })
      },
      handleFileUpload() {
        this.file = this.$refs.file.files[0]
      }
    }
  }

</script>
