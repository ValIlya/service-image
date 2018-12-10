<template>
  <div>
    <div class="row">
      <div class="col-sm-4" v-for="pic in picList" v-bind:key="pic.id">
        <div class="card">
          <img class="card-img-top" v-bind:src="pic" alt="Transformed image" v-on:click="showPic(pic)">
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
        picList: ["/api/get/logo.png"]
      }
    },
    methods: {
      getPicList() {
        const path = '/api/gallery';
        var vm = this;
        axios.get(path)
          .then(response => {
            this.picList = response.data.picList
          }).catch(function (error) {
            console.log(error);
            vm.flashMessage.show({
              status: 'error',
              title: 'Oops!',
              message: error
            })
        })
      },
      showPic(pic) {
        window.open(pic)
      }
    },
    created() {
      this.getPicList()
    }
  }
</script>

<style>
  .card-img-top {
    width: 100%;
    height: 15vw;
    object-fit: cover;
  }
</style>
