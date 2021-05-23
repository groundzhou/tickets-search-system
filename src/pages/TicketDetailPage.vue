<template>
  <mdb-container>
    <h1>航班详情</h1>
    <section class="text-center">
      <mdb-card>
        <mdb-card-body>
          <mdb-row>
            <mdb-col sm="3">
              {{ airlines[ticket.airline_code] }}
              <br />
              {{ ticket.flight_num }}
              <br />
              <mdb-badge color="primary-color">{{ ticket.aircraft }}({{ ticket.aircraft_type }})</mdb-badge>
            </mdb-col>
            <mdb-col sm="2" class="text-center">
              <p style="font-size:20px" class="mb-0">{{ ticket.ddate }}</p>
              <p style="font-size:30px" class="mb-0">{{ ticket.dtime }}</p>
              <p class="mb-0">{{ airports[ticket.dairport_code] }}</p>
            </mdb-col>
            <div class="mt-3">
              <i class="arrow-oneway"></i>
            </div>
            <mdb-col sm="2" class="text-center">
              <p style="font-size:20px" class="mb-0">{{ ticket.adate }}</p>
              <p style="font-size:30px" class="mb-0">{{ ticket.atime }}</p>
              <p class="mb-0">{{ airports[ticket.aairport_code] }}</p>
            </mdb-col>
            <mdb-col sm="2" class="text-center">
              <p style="font-size:25px" class="mb-1">￥{{ ticket.price }}</p>
              {{ ticket.class + ticket.discount }}折
            </mdb-col>
          </mdb-row>
          <mdb-row class="mt-0">
            <mdb-col sm="1"></mdb-col>
            <mdb-col sm="10">
              <mdb-line-chart :data="lineChartData" :options="lineChartOptions" :height="300" />
            </mdb-col>
          </mdb-row>
        </mdb-card-body>
      </mdb-card>
    </section>
    <!-- /BADGES -->
    <hr class="mt-4" />
  </mdb-container>
</template>

<script>
import {
  mdbContainer,
  mdbBadge,
  mdbCard,
  mdbRow,
  mdbCol,
  mdbLineChart,
  mdbCardBody,
} from "mdbvue";

export default {
  name: "TicketDetailPage",
  components: {
    mdbContainer,
    mdbBadge,
    mdbCard,
    mdbRow,
    mdbCol,
    mdbLineChart,
    mdbCardBody,
  },
  data() {
    return {
      cities: [],
      airlines: {},
      airports: {},
      ticket: {},
      lineChartData: {
        labels: [
          "05-07",
          "05-08",
          "05-09",
          "05-10",
          "05-11",
          "05-12",
          "05-13",
          "05-14",
          "05-15",
          "05-16",
          "05-17",
          "05-18",
          "05-19",
          "05-20",
          "05-21",
          "05-22",
          "05-23",
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
        ],
        datasets: [
          {
            label: "预测购买价格",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: [
              770,
              770,
              770,
              770,
              770,
              680,
              680,
              650,
              650,
              650,
              740,
              740,
              740,
              740,
              740,
              746,
              746,
              746,
              746,
              746,
              746,
              746,
              746,
              746,
              746,
              746,
              746,
              746,
              744,
              744,
              744,
              891,
              891,
              891,
              891,
              891,
              860,
              1080,
              1080,
              1080,
              1080,
              1135,
              1135,
              1230,
              1540,
              1665,
              1665,
              1675,
            ],
          },
        ],
      },
      lineChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        xAxisID: "cdate",
        yAxesID: "price",
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
    this.axios.get("/api/airports").then((response) => {
      this.airports = response.data.dict;
    });
    // 查询机票数据
    this.axios.get("/api/tickets/" + this.$route.params.id).then((response) => {
      this.ticket = response.data;
    });
  },

  methods: {},
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

.arrow-oneway {
  background-position: -136px -200px;
  width: 110px;
  height: 22px;
  display: inline-block;
  vertical-align: middle;
  background-image: url(../assets/ico_sprite.png);
  background-image: -webkit-image-set(
    url(../assets/ico_sprite.png) 1x,
    url(../assets/ico_sprite@2x.png) 2x
  );
  background-repeat: no-repeat;
}
</style>
