/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import { observable, computed } from "mobx";
import http from 'libs/http';

class Store {
  @observable records = [];
  @observable record = {};
  @observable deploy = {};
  @observable page = 0;
  @observable loading = {};
  @observable isReadOnly = false;
  @observable isFetching = false;
  @observable formVisible = false;
  @observable addVisible = false;
  @observable ext1Visible = false;
  @observable ext2Visible = false;

  @observable f_name;
  @observable f_desc;
  @observable project;
  @observable ns;
  @observable app;
  @observable envname;
  @observable volume;
  // @observable loadings = [];

  fetchRecords = () => {
    this.isFetching = true;
    return http.get('/api/app/deploy/svc')
      .then(res => this.records = res)
      .finally(() => this.isFetching = false)
  };

  // enterLoading = index => {
  //   const newLoadings = [this.loadings];
  //   newLoadings[index] = true;
  //   this.loadings = newLoadings;
  //   setTimeout(() => {
  //     const newLoadings = [this.loadings];
  //     newLoadings[index] = false;
  //     this.loadings = newLoadings;
  //   }, 6000);
  // };
}

export default new Store()
