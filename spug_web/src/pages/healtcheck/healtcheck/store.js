import { observable } from "mobx";
import http from 'libs/http';

class Store {
    @observable records = [];
    @observable record = {};
    @observable formVisible = false;
    @observable isFetching = false;
    @observable hostdatas = [];
    fetchRecords = () => {
        this.isFetching = true;
        http.get('/api/host/healtcheck/')
            .then(({data, hostdata}) => {
                this.records = data
                this.hostdatas = hostdata
            })
            .finally(() => this.isFetching = false)
    };
    showForm = (info = {}) => {
        this.formVisible = true;
        this.record = info
    };
}

export default new Store()