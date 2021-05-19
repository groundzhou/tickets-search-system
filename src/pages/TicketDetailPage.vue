<template>
  <mdb-container>
    <h1>航班详情</h1>

    <hr class="mt-4" />
    <!-- BADGES -->
    <section class="text-center">
      <h2>Badges</h2>
      <mdb-badge color="primary-color">Primary</mdb-badge>
      <mdb-badge color="default-color">Default</mdb-badge>
      <mdb-badge color="success-color">Success</mdb-badge>
      <mdb-badge color="info-color">Info</mdb-badge>
      <mdb-badge color="warning-color">Warning</mdb-badge>
      <h5>Pills with Font Awesome</h5>
      <mdb-badge pill color="primary-color">
        <mdb-icon icon="snowflake-o" />
      </mdb-badge>
      <mdb-badge color="default-color" pill>
        <mdb-icon icon="hand-spock-o" />
      </mdb-badge>
      <mdb-badge color="success-color" pill>
        <mdb-icon icon="image" />
      </mdb-badge>
      <mdb-badge color="info-color" pill>
        <mdb-icon icon="mortar-board" />
      </mdb-badge>
      <mdb-badge color="warning-color" pill>
        <mdb-icon icon="paint-brush" />
      </mdb-badge>
    </section>
    <!-- /BADGES -->
    <hr class="mt-4" />
  </mdb-container>
</template>

<script>
import { mdbContainer, mdbBadge, mdbIcon } from "mdbvue";

export default {
  name: "TicketDetailPage",
  components: {
    mdbContainer,
    mdbBadge,
    mdbIcon,
  },
  data() {
    return {
      cities: [],
      airlines: {},
      airports: {},
      ticket: {},
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
    this.axios
      .get("/api/tickets/" + this.$route.params.id)
      .then((response) => {
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
</style>
