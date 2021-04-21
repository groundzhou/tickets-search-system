<template>
  <mdb-container class="mt-5">
    出发地
    <el-select v-model="value" filterable placeholder="北京">
      <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
      </el-option>
    </el-select>
    目的地
    <el-select v-model="value" filterable placeholder="昆明">
      <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value">
      </el-option>
    </el-select>
    出发日期
    <el-date-picker
        v-model="searchData.ddate"
        type="date"
        placeholder="选择出发日期">
    </el-date-picker>

    <section class="demo-section">
      <h4>Basic example</h4>
      <section>
        <mdb-datatable :data="chartData" materialInputs responsive/>
      </section>
    </section>
  </mdb-container>
</template>

<script>
import {
  mdbDatatable,
  mdbContainer
} from 'mdbvue';

const DATA_FROM_BACKEND = {
  columns: [{
    label: "Name",
    field: "name",
    sort: "asc"
  }, {
    label: "Position",
    field: "position",
    sort: "asc"
  }, {
    label: "Office",
    field: "office",
    sort: "asc"
  }],
  rows: [{
    name: "Tiger Nixon",
    position: "System Architect",
    office: "Shanghai"
  }, {
    name: "Garrett Winters",
    position: "Accountant",
    office: "Tokyo",
  }, {
    name: "Ashton Cox",
    position: "Junior Technical Author",
    office: "San Francisco",
  }]
};

export default {
  name: 'TicketsPage',
  components: {
    mdbDatatable,
    mdbContainer
  },
  data() {
    return {
      searchData: {
        ddate: "2021-05-01"
      },
      chartData: {
        columns: [],
        rows: []
      }
    }
  },
  created() {
    this.getData();
  },
  methods: {
    handleChange() {
      this.getData();
    },
    getData() {
      this.chartData = {
        columns: DATA_FROM_BACKEND.columns,
        rows: DATA_FROM_BACKEND.rows
      };
    }
  }
};
</script>

<style scoped>
h1, h2 {
  font-weight: normal;
}

.category-page-background {
  width: 100%;
  height: 100%;
  opacity: 0.1;
  background: url('https://mdbootstrap.com/wp-content/uploads/2016/11/mdb-pro-min-1.jpg') center;
  background-size: cover;
}

.example-components-list {
  padding-top: 20px;
}

.example-components-list li {
  padding: 10px;
  background-color: white;
  border-bottom: 1px solid #f7f7f7;
  transition: .3s;
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
