<template>
  <mdb-container>
    <h1>何时飞</h1>
    <mdb-row class="text-center">
      <mdb-col class="col-6">
        出发地
        <el-select
          class="col-8"
          v-model="searchData.dcity"
          filterable
          placeholder="北京"
          @change="handleChange"
        >
          <el-option v-for="item in cities" :key="item.code" :label="item.name" :value="item.code"></el-option>
        </el-select>
      </mdb-col>
      <mdb-col class="col-6">
        目的地
        <el-select
          class="col-8"
          v-model="searchData.acity"
          filterable
          placeholder="昆明"
          @change="handleChange"
        >
          <el-option v-for="item in cities" :key="item.code" :label="item.name" :value="item.code"></el-option>
        </el-select>
      </mdb-col>
    </mdb-row>
    <hr class="mt-4" />
  </mdb-container>
</template>

<script>
import { mdbContainer, mdbRow, mdbCol } from "mdbvue";

export default {
  name: "PricesPage",
  components: {
    mdbContainer,
    mdbRow,
    mdbCol,
  },
  data() {
    return {
      searchData: {
        dcity: "BJS",
        acity: "KMG",
      },
      cities: [],
      airlines: {},
      airports: {},
      prices: [],
    };
  },

  created() {
    this.axios.get("/api/cities").then((response) => {
      this.cities = response.data;
    });
    this.axios.get("/api/airlines").then((response) => {
      this.airlines = response.data.dict;
    });
    this.searchPrices();
  },

  methods: {
    // 处理查询条件变更
    handleChange() {
      this.loading = true;
      this.searchTickets();
    },
    searchPrices() {
      this.axios
        .get("/api/prices", {
          params: {
            dcity: this.searchData.dcity,
            acity: this.searchData.acity,
          },
        })
        .then((response) => {
          console.log(response.data);
        });
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  margin: 50px 0;
}
h1,
h2,
h5 {
  text-align: center;
}
.container > p {
  margin-bottom: 80px;
  text-align: center;
}
section {
  padding-bottom: 40px;
}
section > h2 {
  font-weight: 500;
  margin: 50px 0;
}
section > h5 {
  margin: 30px 0;
}
.media {
  text-align: left;
}
.navbar .dropdown-menu a:hover {
  color: inherit !important;
}
form h5 {
  text-align: left;
}
</style>
