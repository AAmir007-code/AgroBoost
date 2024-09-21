const axios = require('axios')

const request = axios.create({
    baseURL: 'https://challenge.robocontest.uz/api'
})

export default request;
