import Vue from 'vue'
import Router from 'vue-router'
import Gallery from '@/components/Gallery'
import Image from '@/components/Image'
import About from '@/components/About'
import NotFound from '@/components/NotFound'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Image',
      component: Image
    },
    {
      path: '/gallery',
      name: 'Gallery',
      component: Gallery
    },
    {
      path: '/about',
      name: 'About',
      component: About
    },
    {
      path: '*',
      name: 'NotFound',
      component: NotFound
    }
  ]
})
