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
    <mdb-row>
      <mdb-col md="1"></mdb-col>
      <mdb-col md="8">
        <mdb-line-chart
          :data="lineChartData"
          :options="lineChartOptions"
          :width="900"
          :height="300"
        ></mdb-line-chart>
      </mdb-col>
    </mdb-row>
  </mdb-container>
</template>

<script>
import { mdbContainer, mdbRow, mdbCol, mdbLineChart } from "mdbvue";

export default {
  name: "PricesPage",
  components: {
    mdbContainer,
    mdbRow,
    mdbCol,
    mdbLineChart,
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
      lineChartData: {
        labels: [
          "05-24",
          "05-25",
          "05-26",
          "05-27",
          "05-28",
          "05-29",
          "05-30",
          "05-31",
          "06-01",
          "06-02",
          "06-03",
          "06-04",
          "06-05",
          "06-06",
          "06-07",
          "06-08",
          "06-09",
          "06-10",
          "06-11",
          "06-12",
          "06-13",
          "06-14",
          "06-15",
          "06-16",
          "06-17",
          "06-18",
          "06-19",
          "06-20",
          "06-21",
          "06-22",
          "06-23",
          "06-24",
          "06-25",
          "06-26",
          "06-27",
          "06-28",
          "06-29",
          "06-30",
          "07-01",
          "07-02",
          "07-03",
          "07-04",
          "07-05",
          "07-06",
          "07-07",
          "07-08",
          "07-09",
          "07-10",
          "07-11",
          "07-12",
          "07-13",
          "07-14",
          "07-15",
          "07-16",
          "07-17",
          "07-18",
          "07-19",
          "07-20",
          "07-21",
          "07-22",
        ],
        datasets: [
          {
            label: "每日最低价格",
            backgroundColor: "rgba(255, 99, 132, 0.1)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 0.7,
            data: [
              500,
              400,
              400,
              400,
              408,
              400,
              400,
              400,
              400,
              400,
              400,
              400,
              400,
              400,
              400,
              400,
              500,
              650,
              590,
              600,
              593,
              550,
              600,
              600,
              600,
              620,
              600,
              600,
              600,
              600,
              600,
              600,
              600,
              600,
              600,
              600,
              600,
              600,
              670,
              670,
              670,
              670,
              670,
              670,
              670,
              700,
              700,
              700,
              700,
              700,
              700,
              700,
              700,
              700,
              700,
              870,
              700,
              700,
              870,
              700,
            ],
          },
        ],
      },
      lineChartOptions: {
        responsive: false,
        maintainAspectRatio: false,
        scales: {
          xAxes: [
            {
              gridLines: {
                display: true,
                color: "rgba(0, 0, 0, 0.1)",
              },
            },
          ],
          yAxes: [
            {
              gridLines: {
                display: true,
                color: "rgba(0, 0, 0, 0.1)",
              },
            },
          ],
        },
      },
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
