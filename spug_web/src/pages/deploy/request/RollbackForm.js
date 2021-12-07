/**
 * Copyright (c) OpenSpug Organization. https://github.com/openspug/spug
 * Copyright (c) <spug.dev@gmail.com>
 * Released under the AGPL-3.0 License.
 */
import React from 'react';
import { observer } from 'mobx-react';
import { Modal, Form, Input,  message, Button, Select } from 'antd';
import { http, hasPermission,formatDate } from 'libs';

import store from './store';
import './style.css';
import './html.css';
import './annotated.css';
@observer
class RollbackForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      rov: null,
    }
  }

  // componentDidMount() {
  //   if (hostStore.records.length === 0) {
  //     hostStore.fetchRecords()
  //   }
  //   const file = lds.get(store, 'record.extra.1');
  //   if (file) {
  //     file.uid = '0';
  //     this.setState({fileList: [file]})
  //   }
  // }
  handleSubmit = () =>{
    http.post('/api/app/svc/rollback/' + store.tmp_rollid+'/', {"data":{"replicaSetId":this.state.rov}}, {timeout: 120000})
    .then(()=> {
          message.success('回滚成功');
          store.rollVisible = false;
    })
    // .finally(() => this.setState({uploading: false}))
  }


  render() {

    const { Option } = Select;

    return (
      <Modal
        visible
        width={800}
        maskClosable={false}
        title="回滚版本选择"
        onOk={this.handleSubmit}
        onCancel={() => store.rollVisible = false}
        confirmLoading={this.state.loading}
        >
              <Select defaultValue={"请选择....."} onChange={v=> this.setState({rov:v})} style={{ width: 500 }} >
                  {store.rollbackv.map((item,index)=>(
                      <Option key={item["id"]} value={item["id"]}>{item["time"]}</Option>                            
                  ))}
              </Select>
      </Modal>

    )
  }
}

export default Form.create()(RollbackForm)
