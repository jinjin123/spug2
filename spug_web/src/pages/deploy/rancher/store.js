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
  @observable deployForm =false;
  @observable f_name;
  @observable f_desc;
  @observable project;
  @observable ns;
  @observable app;
  @observable envname;
  @observable volume;
  @observable rancherPublish = false;
  @observable addRancherVisible = false;
  // @observable loadings = [];

  fetchRecords = () => {
    this.isFetching = true;
    return http.get('/api/app/deploy/svc')
      .then(res => this.records = res)
      .finally(() => this.isFetching = false)
  };

  showAddForm = () => {
    this.deployForm = true;
  }
  showRancerExtForm = (e, app_id, info, isClone, isReadOnly = false) => {
    if (e) e.stopPropagation();
    this.page = 0;
    this.app_id = app_id;
    this.isReadOnly = isReadOnly
    if (info) {
      if (info.extend === '1') {
        this.ext1Visible = true
      } else {
        this.ext2Visible = true
      }
      isClone && delete info.id;
      this.deploy = info
    } else {
      this.addRancherVisible = true;
      this.rancherPublish = true;
    }
  };

}

export default new Store()
