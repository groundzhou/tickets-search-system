<template>
  <div style="margin-top: -15px; overflow-x: hidden">
    <mdb-edge-header color="teal darken-2">
      <div class="home-page-background"></div>
    </mdb-edge-header>
    <mdb-container class="free-bird">
      <mdb-row>
        <mdb-col md="10" class="mx-auto white z-depth-1 py-2 px-2">
          <mdb-card-body>
            <h2 class="pb-4">
              <strong>机票查询</strong>
            </h2>
            <mdb-row>
              <mdb-col md="2"></mdb-col>
              <mdb-col md="2">
                <img src="../../src/assets/airplane.png" class="img-fluid" />
              </mdb-col>
              <mdb-col md="8">
                <p class="pb-1">
                  基于大数据技术的机票查询及票价预测系统
                  <br />在此输入您的出发地、目的地、出发日期
                </p>
              </mdb-col>
            </mdb-row>
            <mdb-row>
              <mdb-col>
                出发地<br>
                <el-select v-model="searchData.dcity" filterable placeholder="北京">
                  <el-option
                    v-for="item in cities"
                    :key="item.code"
                    :label="item.name"
                    :value="item.code"
                  ></el-option>
                </el-select>
              </mdb-col>
              <mdb-col>
                目的地<br>
                <el-select v-model="searchData.acity" filterable placeholder="昆明">
                  <el-option
                    v-for="item in cities"
                    :key="item.code"
                    :label="item.name"
                    :value="item.code"
                  ></el-option>
                </el-select>
              </mdb-col>
              <mdb-col>
                出发日期<br>
                <el-date-picker v-model="searchData.ddate" type="date" value-format="yyyy-MM-dd"></el-date-picker>
              </mdb-col>
            </mdb-row>
            <mdb-row class="d-flex flex-row justify-content-center">
              <a
                @click="search"
                class="nav-link border indigo-text m-2 font-weight-bold rounded"
                target="_blank"
              >
                <mdb-icon icon="search" class="mr-2" />搜索机票
              </a>
            </mdb-row>
          </mdb-card-body>
        </mdb-col>
      </mdb-row>
    </mdb-container>
    <mdb-container>
      <h2 class="text-center mt-5 font-weight-bold">Why is it so great?</h2>
      <mdb-col md="10" class="mx-auto text-center text-muted mb-5">
        <p>
          Google has designed a Material Design to make the web more beautiful
          and more user-friendly.
          <br />Twitter has created a Bootstrap to support you in faster and easier
          development of responsive and effective websites.
          <br />We present you a framework containing the best features of both of
          them - Material Design for Bootstrap.
        </p>
      </mdb-col>

      <mdb-row>
        <mdb-col md="4" class="mb-5">
          <mdb-card class="animated fadeInLeft">
            <mdb-card-image
              src="https://mdbootstrap.com/wp-content/uploads/2016/08/mdb.jpg"
              alt="Card image cap"
            ></mdb-card-image>
            <mdb-card-body>
              <mdb-card-title>
                <mdb-icon fab icon="css3" class="pink-text" />
                <strong>机票查询</strong>
              </mdb-card-title>
              <mdb-card-text>
                Animations, colors, shadows, skins and many more! Get to know
                all our css styles in one place.
              </mdb-card-text>
              <router-link to="/tickets" class="float-right">
                <mdb-btn color="elegant">More</mdb-btn>
              </router-link>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>
        <mdb-col md="4" class="mb-5">
          <mdb-card class="animated fadeIn">
            <mdb-card-image
              src="https://mdbootstrap.com/img/Marketing/mdb-press-pack/mdb-main.jpg"
              alt="Card image cap"
            ></mdb-card-image>
            <mdb-card-body>
              <mdb-card-title>
                <mdb-icon icon="cubes" class="blue-text" />
                <strong>何时飞</strong>
              </mdb-card-title>
              <mdb-card-text>
                Ready-to-use components that you can use in your applications.
                Both basic and extended versions!
              </mdb-card-text>
              <router-link to="/components" class="float-right">
                <mdb-btn color="elegant">More</mdb-btn>
              </router-link>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>
        <mdb-col md="4" class="mb-5">
          <mdb-card class="animated fadeInRight">
            <mdb-card-image
              src="https://mdbootstrap.com/wp-content/uploads/2018/11/mdb-jquery-free.jpg"
              alt="Card image cap"
            ></mdb-card-image>
            <mdb-card-body>
              <mdb-card-title>
                <mdb-icon icon="code" class="green-text" />
                <strong>飞去哪</strong>
              </mdb-card-title>
              <mdb-card-text>
                Advanced components such as charts, carousels, tooltips and
                popovers. All in Material Design version.
              </mdb-card-text>
              <router-link to="/advanced" class="float-right">
                <mdb-btn color="elegant">More</mdb-btn>
              </router-link>
            </mdb-card-body>
          </mdb-card>
        </mdb-col>
      </mdb-row>
    </mdb-container>
  </div>
</template>

<script>
import {
  mdbContainer,
  mdbCol,
  mdbRow,
  mdbIcon,
  mdbBtn,
  mdbEdgeHeader,
  mdbCard,
  mdbCardImage,
  mdbCardTitle,
  mdbCardText,
  mdbCardBody,
  animateOnScroll,
} from "mdbvue";

export default {
  name: "HomePage",
  components: {
    mdbContainer,
    mdbCol,
    mdbRow,
    mdbIcon,
    mdbBtn,
    mdbEdgeHeader,
    mdbCard,
    mdbCardImage,
    mdbCardTitle,
    mdbCardText,
    mdbCardBody,
  },
  data() {
    return {
      searchData: {
        dcity: "BJS",
        acity: "KMG",
        ddate: "2021-05-24",
      },
      cities: [],
    };
  },
  directives: {
    animateOnScroll,
  },
  created() {
    this.axios.get("/api/cities").then((response) => {
      this.cities = response.data;
    });
    this.searchData.ddate = new Date().toISOString().slice(0, 10);
  },
  methods:{
    search() {
      this.$router.push({
        name: 'TicketsPage',
        params: {
          dcity: this.searchData.dcity,
          acity: this.searchData.acity,
          ddate: this.searchData.ddate,
        }
      })
    }

  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: normal;
}

.home-feature-box {
  padding: 40px 0;
}

.home-feature-box i {
  font-size: 6rem;
}

.home-feature-box span {
  display: block;
  color: black;
  font-size: 20px;
  font-weight: bold;
  padding-top: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

/* li {
  display: inline-block;
} */

a {
  color: #42b983;
}

.home-page-background {
  width: 100%;
  height: 100%;
  opacity: 0.1;
  background: url("https://mdbootstrap.com/wp-content/uploads/2016/11/mdb-pro-min-1.jpg")
    center;
  background-size: cover;
}
</style>
