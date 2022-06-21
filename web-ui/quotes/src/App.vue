<template>
  <Layout>
      <!-- <h2 class="mb-8 text-4xl font-bold text-center capitalize">
        News Section : <span class="text-green-700">{{ section }}</span>
      </h2> -->
    <quotesFilter v-model="section" :fetch="fetchNews" />
    <quotesList :posts="posts" />
  </Layout>
</template>

<script>
import Layout from "./components/Layout.vue"
import quotesFilter from "./components/quotesFilter.vue"
import quotesList from "./components/quotesList.vue"
import quotesCard from "./components/quotesCard.vue"

import axios from "axios"

export default {
  components: {
    Layout,
    quotesFilter,
    quotesList,
    quotesCard,
  },
  data() {
    return {
      // section: "home",
      posts:[],
    }
  },
  methods: {
    // Helper function for extracting a nested image object
    async fetchNews() {
      try {
        const url = 'http://3.6.86.239:49160/all/book1'
        const response = await axios.get(url)
        const results = response.data
        console.log(results[0])
        this.posts = results.map(post => ({
          author: post.author,
          likes: post.likes,
          tags: post.tags,
          text: post.text,
          title: post.title,  
          _id: post._id
        }))
      } catch (err) {
        if (err.response) {
          // client received an error response (5xx, 4xx)
          console.log("Server Error:", err)
        } else if (err.request) {
          // client never received a response, or request never left
          console.log("Network Error:", err)
        } else {
          console.log("Client Error:", err)
        }
      }
    },
  },
  mounted() {
    this.fetchNews()
  },
}
</script>