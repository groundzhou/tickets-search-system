<template>
  <mdb-container class="mt-5">
    出发地
    <el-select v-model="searchData.dcity" filterable placeholder="北京" @change="handleChange">
      <el-option v-for="item in cities" :key="item.code" :label="item.name" :value="item.code"></el-option>
    </el-select>目的地
    <el-select v-model="searchData.acity" filterable placeholder="昆明" @change="handleChange">
      <el-option v-for="item in cities" :key="item.code" :label="item.name" :value="item.code"></el-option>
    </el-select>出发日期
    <el-date-picker
      v-model="searchData.ddate"
      type="date"
      value-format="yyyy-MM-dd"
      v-loading.fullscreen.lock="loading"
      @change="handleChange"
    ></el-date-picker>
    <section class="demo-section">
      <h4>查询结果</h4>
      <mdb-row class="mt-2" v-for="ticket in tickets" v-bind:key="ticket.id">
        <mdb-col>
          <mdb-card>
            <mdb-card-body>
              <mdb-row>
                <mdb-col sm="3">
                  {{ airlines[ticket.airline_code] }}
                  {{ ticket.flight_num }}
                  <br />
                  {{ ticket.aircraft }}({{ ticket.aircraft_type }})
                </mdb-col>
                <mdb-col sm="2">
                  {{ ticket.ddate }}
                  <br/>
                  {{ ticket.dtime }}
                  <br />
                  {{ airports[ticket.dairport_code] }}
                </mdb-col>
                <mdb-col sm="2">
                  {{ ticket.atime }}
                  <br />
                  {{ airports[ticket.aairport_code] }}
                </mdb-col>
                <mdb-col sm="2">
                  ￥{{ ticket.price }}
                  <br />
                  {{ ticket.class + ticket.discount }}折
                </mdb-col>
                <mdb-col sm="3">
                  <mdb-btn color="primary">详情</mdb-btn>
                </mdb-col>
              </mdb-row>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>
      </mdb-row>
    </section>
  </mdb-container>
</template>

<script>
import {
  mdbContainer,
  mdbRow,
  mdbCard,
  mdbCardBody,
  mdbCol,
  mdbBtn,
} from "mdbvue";

export default {
  name: "TicketsPage",
  components: {
    mdbContainer,
    mdbCard,
    mdbCardBody,
    mdbRow,
    mdbCol,
    mdbBtn,
  },
  data() {
    return {
      searchData: {
        dcity: "BJS",
        acity: "SHA",
        ddate: "2021-05-20",
      },
      cities: [],
      airlines: {},
      airports: {},
      tickets: [],
      loading: false,
    };
  },
  created() {
    if (this.$route.params.dcity != null) {
      this.searchData.dcity = this.$route.params.dcity;
    }
    if (this.$route.params.acity != null) {
      this.searchData.acity = this.$route.params.acity;
    }
    if (this.$route.params.ddate != null) {
      this.searchData.ddate = this.$route.params.ddate;
    } else {
      this.searchData.ddate = new Date().toISOString().slice(0, 10);
    }
    this.getData();
  },
  methods: {
    // 处理查询条件变更
    handleChange() {
      this.loading = true;
      this.searchTickets();
    },

    // 初始化数据
    getData() {
      this.axios.get("/api/cities").then((response) => {
        this.cities = response.data;
      });
      this.axios.get("/api/airlines").then((response) => {
        this.airlines = response.data.dict;
      });
      this.axios.get("/api/airports").then((response) => {
        this.airports = response.data.dict;
      });
      this.searchTickets();
    },

    // 查询后台机票数据
    searchTickets() {
      this.axios
        .get("/api/tickets", {
          params: {
            dcity: this.searchData.dcity,
            acity: this.searchData.acity,
            ddate: this.searchData.ddate,
          },
        })
        .then((response) => {
          this.tickets = response.data;
          this.loading = false;
        });
    },
  },
};
</script>

<style scoped>
h1,
h2 {
  font-weight: normal;
}

.category-page-background {
  width: 100%;
  height: 100%;
  opacity: 0.1;
  background: url("https://mdbootstrap.com/wp-content/uploads/2016/11/mdb-pro-min-1.jpg")
    center;
  background-size: cover;
}

.example-components-list {
  padding-top: 20px;
}

.example-components-list li {
  padding: 10px;
  background-color: white;
  border-bottom: 1px solid #f7f7f7;
  transition: 0.3s;
}

.example-components-list h6 {
  padding: 20px 10px 5px 10px;
  color: grey;
}

.example-components-list li:hover {
  background-color: #fafafa;
}

.example-components-list i {
  float: right;
  padding-top: 3px;
}

.nav-link.navbar-link h5 {
  color: #212529;
}
</style>
