<template>
  <div id="app">
    <div class="map" ref="map" style="width:100vw; height: 100vh"></div>

    <div class="show_information" v-if="regionInfo" style="zoom: .9;">
      <div class="card container card-body">
        <div v-if="regionInfoLoading" class="d-flex flex-column align-items-center justify-content-center">
          <div class="h2 text-center">Iltimos kuting, Sun'iy intellekt sun'iy yo'ldoshlarni analiz qilyapti 🤖</div>

          <br>
          <div class="loader_div">
            <div class="lds-ellipsis">
              <div></div>
              <div></div>
              <div></div>
              <div></div>
            </div>
          </div>
        </div>

        <div v-else class="row">
          <div class="col-md-12">
            <div class="d-flex align-items-center ">
              <div class="weather_col w-50">
                <div>
                  <b>Zararlangan o'simliklar</b>
                </div>
                <span class="h1" id="total_area">{{ regionInfo.area.toFixed(2) }}</span> km<sup>2</sup>
              </div>

              <div class="weather_col w-50">
                <div>
                  <b>Umumiy maydon</b>
                </div>
                <span class="h1">{{ regionInfo.total_area.toFixed(2) }}</span> km<sup>2</sup>
              </div>


            </div>

            <div class="h4 my-3">
              Kasallanish darajasi
            </div>
            <div class="d-flex"
                 style="height: 32px; width: 100%; background: #ddd; position: relative; border-radius: 5px; overflow: hidden">
              <div class="text-center text-white align-items-center d-flex justify-content-center"
                   style="height: 100%; background: darkred" :style="{width: regionInfo.perc + '%'}">
                <span v-if="regionInfo.perc > 15">{{ regionInfo.perc.toFixed(1) }} %</span>
              </div>

              <div v-if="regionInfo.perc <= 15"
                   class="text-center align-items-center d-flex flex-grow-1 justify-content-center">
                {{ regionInfo.perc.toFixed(1) }} %
              </div>
            </div>

            <div class="h4 my-3">
              1-haftadan keyingi holat
            </div>
            <div class="d-flex"
                 style="height: 32px; width: 100%; background: #ddd; position: relative; border-radius: 5px; overflow: hidden">
              <div class="text-center text-white align-items-center d-flex justify-content-center"
                   style="height: 100%; background: #a24141" :style="{width: (regionInfo.perc * 1.12) + '%'}">
                <span v-if="(regionInfo.perc * 1.12) > 15">{{
                    (Math.min(regionInfo.perc * 1.12, 100)).toFixed(1)
                  }} %</span>
              </div>

              <div v-if="(regionInfo.perc * 1.12) <= 15"
                   class="text-center align-items-center d-flex flex-grow-1 justify-content-center">
                {{ (regionInfo.perc * 1.12).toFixed(1) }} %
              </div>
            </div>

            <div class="d-flex align-content-center align-items-center pt-3">
              <div class="m-1 w-50">
                <b>Original fotosurat</b>
                <img id="imgg" style="width: 100%" class="border" :src="regionInfo.source_img">
              </div>
              <div class="m-1 w-50">
                <b>AI nigohi</b>
                <img id="img_analys" style="width: 100%" class="border" :src="regionInfo.analyzed_img">
              </div>
            </div>

            <div class="drone-list">
              <iframe
                  src="https://sketchfab.com/models/cc7d69c067124bf59efa40d28cd4e129/embed?autostart=1&internal=1&tracking=0&ui_ar=0&ui_infos=0&ui_snapshots=1&ui_stop=0&ui_theatre=1&ui_watermark=0"
                  frameborder="0"></iframe>

              <iframe frameborder="0"
                      src="https://sketchfab.com/models/65733ddf867a4bf2908eb10d26f6dfeb/embed?autostart=1&internal=1&tracking=0&ui_ar=0&ui_infos=0&ui_snapshots=1&ui_stop=0&ui_theatre=1&ui_watermark=0"></iframe>

              <iframe frameborder="0"
                      src="https://sketchfab.com/models/428708deba0e4d288d5e8cf38593f979/embed?autostart=1&internal=1&tracking=0&ui_ar=0&ui_infos=0&ui_snapshots=1&ui_stop=0&ui_theatre=1&ui_watermark=0"></iframe>

              <iframe frameborder="0"
                      src="https://sketchfab.com/models/41e1ea89a3414f94910264f0e3c868d1/embed?autostart=1&internal=1&tracking=0&ui_ar=0&ui_infos=0&ui_snapshots=1&ui_stop=0&ui_theatre=1&ui_watermark=0"></iframe>
            </div>


            <button class="btn btn-block btn-danger margin-top-10" @click="regionInfo=null" id="close">
              Yopish
            </button>
          </div>
        </div><!--ng show -->
      </div>
    </div>
  </div>
</template>

<script>
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import request from "@/request";
import './style.css'

export default {
  name: 'App',

  data() {
    return {
      map: null,
      selectedTile: null,
      regionInfo: null,
      regionInfoLoading: false
    }
  },


  mounted() {
    this.setupMap();
  },

  methods: {
    setupMap() {
      this.map = L.map(this.$refs.map, {
        center: [41.309604, 69.241050],
        zoom: 13,
      });

      const googleMap = L.tileLayer('https://mt0.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
        maxZoom: 21
      });
      const greenMap = L.tileLayer('http://challenge.robocontest.uz/api/map/{z}/{x}/{y}', {
        maxZoom: 21
      });

      const NASAGIBS_ViirsEarthAtNight2012 = L.tileLayer('http://map1.vis.earthdata.nasa.gov/wmts-webmerc/VIIRS_CityLights_2012/default/{time}/{tilematrixset}{maxZoom}/{z}/{y}/{x}.{format}', {
        minZoom: 1,
        maxZoom: 8,
        format: 'jpg',
        time: '',
        tilematrixset: 'GoogleMapsCompatible_Level'
      });

      const NASAGIBS_CO2 = L.tileLayer('http://map1.vis.earthdata.nasa.gov/wmts-webmerc/AIRS_L3_Carbon_Dioxide_IR_Monthly/default/{time}/{tilematrixset}{maxZoom}/{z}/{y}/{x}.{format}', {
        minZoom: 1,
        maxZoom: 8,
        format: 'jpg',
        time: '2020-04-18T00:00:00Z',
        tilematrixset: 'GoogleMapsCompatible_Level'
      });


      L.control.layers({
        'NASA map': googleMap,
        //'NASA CO2 map': NASAGIBS_CO2,
        'NASA Night map': NASAGIBS_ViirsEarthAtNight2012,
        'AI map': greenMap
      }).addTo(this.map);

      googleMap.addTo(this.map)

      this.map.on('click', (e) => {
        const latlng = e.latlng;
        const map = this.map;

        const pixelPoint = map.project(latlng, map.getZoom()).floor();
        const coords = {
          x: Math.floor(pixelPoint.x / 256),
          y: Math.floor(pixelPoint.y / 256),
          z: map.getZoom()
        };

        if (map.getZoom() < 1) {
          return
        }

        function tile2long(x, z) {
          return (x / Math.pow(2, z) * 360 - 180);
        }

        function tile2lat(y, z) {
          const n = Math.PI - 2 * Math.PI * y / Math.pow(2, z);

          return (180 / Math.PI * Math.atan(0.5 * (Math.exp(n) - Math.exp(-n))));
        }

        const bounds = [
          [tile2lat(coords.y, coords.z), tile2long(coords.x, coords.z)],
          [tile2lat(coords.y + 1, coords.z), tile2long(coords.x + 1, coords.z)]
        ];

        this.selectedTile = L.rectangle(bounds, {color: '#09f', weight: 1});
        this.selectedTile.addTo(map);

        this.loadSelectedTileInfo({x: coords.x, y: coords.y, z: coords.z, lat: latlng.lat, lng: latlng.lng})
      });
    },

    /**
     * @param {{x: number, y: number, z: number, lat: number, lng: number}} details
     */
    async loadSelectedTileInfo(details) {
      try {
        this.regionInfoLoading = true;

        const response = await request({
          method: "POST",
          url: '/loadByXYZ',
          data: details,
        })

        this.regionInfo = response.data
      } finally {
        this.regionInfoLoading = false;
      }
    }
  },

  watch: {
    selectedTile(current, old) {
      if (old)
        this.map.removeLayer(old)
    }
  }
}
</script>

<style>
html, body {
  padding: 0;
  margin: 0;
}

.leaflet-control-attribution {
  display: none;
}

.drone-list > * {
  width: 50%;
}
</style>
